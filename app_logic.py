"""Logic nghiệp vụ trung tâm của hệ thống quản lý thư viện.

Lớp LogicApp đóng gói toàn bộ các quy trình nghiệp vụ và sử dụng
HashTable / List tự cài đặt từ custom_structures.
"""

import json
import os
import re
from models import (
    Book, BookCondition,
    Reader, Gender,
    TrackBook, TrackStatus,
    Fine, FineReason,
)
from custom_structures import HashTable, List


# ─────────────────────────────────────────────────────────────────
#  Hằng số toàn cục
# ─────────────────────────────────────────────────────────────────

MAX_BORROW_PER_READER = 5      # Số sách mượn đồng thời tối đa
FINE_PER_DAY          = 5_000.0   # VND / ngày trễ
FINE_DAMAGE           = 100_000.0  # VND phạt hư hỏng
FINE_LOST             = 300_000.0  # VND phạt mất sách


# ─────────────────────────────────────────────────────────────────
# Xác thực dữ liệu đầu vào
# ─────────────────────────────────────────────────────────────────

class Validator:
    """Tập hợp các hàm xác thực dữ liệu đầu vào."""

    _DATE_RE  = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    _ID_RE    = re.compile(r"^[A-Za-z0-9_\-]+$")
    _PHONE_RE = re.compile(r"^0\d{9}$")

    @staticmethod
    def is_valid_date(date_str: str) -> bool:
        """Kiểm tra định dạng YYYY-MM-DD và tính hợp lệ của ngày."""
        if not Validator._DATE_RE.match(date_str):
            return False
        try:
            y, m, d = map(int, date_str.split("-"))
            if not (1 <= m <= 12 and 1 <= d <= 31):
                return False
            if m in (4, 6, 9, 11) and d > 30:
                return False
            if m == 2:
                is_leap = (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)
                if d > (29 if is_leap else 28):
                    return False
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_id(id_str: str) -> bool:
        """Mã ID chỉ chứa chữ, số, gạch ngang, gạch dưới; không rỗng."""
        return bool(id_str) and bool(Validator._ID_RE.match(id_str))

    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """Số điện thoại Việt Nam 10 chữ số, bắt đầu bằng 0."""
        return bool(Validator._PHONE_RE.match(phone))

    @staticmethod
    def is_positive_int(value) -> bool:
        return isinstance(value, int) and value >= 0


# ─────────────────────────────────────────────────────────────────
#  Hàm tiện ích I/O
# ─────────────────────────────────────────────────────────────────

def _save_json(path: str, data: list) -> None:
    with open(path, "w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)


def _load_json(path: str) -> list:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as fp:
        return json.load(fp)


# ─────────────────────────────────────────────────────────────────
#  Lớp LogicApp
# ─────────────────────────────────────────────────────────────────

class LogicApp:
    """Lớp nghiệp vụ trung tâm của hệ thống quản lý thư viện."""

    def __init__(self):
        self._books:   HashTable = HashTable()
        self._readers: HashTable = HashTable()
        self._tracks:  HashTable = HashTable()
        self._fines:   HashTable = HashTable()

    # ═══════════════════════════════════════════════════════════
    #  SÁCH — CRUD + Tìm kiếm
    # ═══════════════════════════════════════════════════════════

    def them_sach(self, sach: Book) -> bool:
        """Thêm sách mới. False nếu mã không hợp lệ, đã tồn tại hoặc sl < 0."""
        if not Validator.is_valid_id(sach.ma_sach):
            return False
        if self._books.contains(sach.ma_sach):
            return False
        if not Validator.is_positive_int(sach.so_luong):
            return False
        self._books.put(sach.ma_sach, sach)
        return True

    def xoa_sach(self, ma_sach: str) -> bool:
        """Xóa sách. False nếu không tìm thấy hoặc đang có người mượn."""
        if not self._books.contains(ma_sach):
            return False
        for _, t in self._tracks.items():
            if t.ma_sach == ma_sach and t.trang_thai != TrackStatus.RETURNED:
                return False
        return self._books.remove(ma_sach)

    def tim_sach(self, ma_sach: str):
        """Tìm sách theo mã. Trả None nếu không có."""
        return self._books.get(ma_sach)

    # Nhóm 1 — cập nhật
    def cap_nhat_sach(self, ma_sach: str, **fields) -> bool:
        """Cập nhật thông tin sách.

        Các trường hợp lệ: ten_sach, tac_gia, the_loai, nha_xuat_ban,
                           so_luong, tinh_trang.
        Raises:
            KeyError   – không tìm thấy sách
            ValueError – trường không hợp lệ / giá trị sai kiểu
        """
        sach = self._books.get(ma_sach)
        if sach is None:
            raise KeyError(f"Khong tim thay sach '{ma_sach}'.")
        ALLOWED = {"ten_sach", "tac_gia", "the_loai", "nha_xuat_ban",
                   "so_luong", "tinh_trang"}
        for field, value in fields.items():
            if field not in ALLOWED:
                raise ValueError(f"Truong '{field}' khong duoc phep cap nhat.")
            if field == "so_luong" and not Validator.is_positive_int(value):
                raise ValueError("so_luong phai la so nguyen khong am.")
            if field == "tinh_trang" and not isinstance(value, BookCondition):
                raise ValueError("tinh_trang phai la BookCondition.")
            setattr(sach, field, value)
        return True

    def lay_tat_ca_sach(self) -> List:
        result = List()
        for _, b in self._books.items():
            result.append(b)
        return result

    @staticmethod
    def _match(text: str, keyword: str) -> bool:
        return keyword.lower() in text.lower()

    def tim_sach_theo_ten(self, keyword: str) -> List:
        result = List()
        for _, b in self._books.items():
            if self._match(b.ten_sach, keyword):
                result.append(b)
        return result

    def tim_sach_theo_the_loai(self, keyword: str) -> List:
        result = List()
        for _, b in self._books.items():
            if self._match(b.the_loai, keyword):
                result.append(b)
        return result

    def loc_sach(self, the_loai: str = None, tinh_trang: BookCondition = None, nha_xuat_ban: str = None) -> List:
        """Lọc sách theo thể loại, tình trạng hoặc nhà xuất bản."""
        result = List()
        for _, b in self._books.items():
            match_the_loai = True
            match_tinh_trang = True
            match_nxb = True
            
            if the_loai is not None and not self._match(b.the_loai, the_loai):
                match_the_loai = False
            if tinh_trang is not None and b.tinh_trang != tinh_trang:
                match_tinh_trang = False
            if nha_xuat_ban is not None and not self._match(b.nha_xuat_ban, nha_xuat_ban):
                match_nxb = False
                
            if match_the_loai and match_tinh_trang and match_nxb:
                result.append(b)
        return result

    def sap_xep_sach(self, tieu_chi: str = "ten_sach", giam_dan: bool = False) -> List:
        """Sắp xếp sách theo tiêu chí (ten_sach, so_luong, tac_gia) bằng Insertion Sort."""
        result = self.lay_tat_ca_sach()
        n = len(result)
        if n <= 1:
            return result
            
        for i in range(1, n):
            key = result[i]
            j = i - 1
            
            while j >= 0:
                curr = result[j]
                val_key = getattr(key, tieu_chi)
                val_curr = getattr(curr, tieu_chi)
                
                if isinstance(val_key, str) and isinstance(val_curr, str):
                    val_key = val_key.lower()
                    val_curr = val_curr.lower()
                
                should_move = False
                if giam_dan:
                    if val_curr < val_key:
                        should_move = True
                else:
                    if val_curr > val_key:
                        should_move = True
                        
                if should_move:
                    result[j + 1] = curr
                    j -= 1
                else:
                    break
            result[j + 1] = key
            
        return result

    # ═══════════════════════════════════════════════════════════
    #  ĐỘC GIẢ — CRUD + Tìm kiếm
    # ═══════════════════════════════════════════════════════════

    def them_doc_gia(self, doc_gia: Reader) -> bool:
        if not Validator.is_valid_id(doc_gia.ma_ban_doc):
            return False
        if self._readers.contains(doc_gia.ma_ban_doc):
            return False
        self._readers.put(doc_gia.ma_ban_doc, doc_gia)
        return True

    def xoa_doc_gia(self, ma_ban_doc: str) -> bool:
        if not self._readers.contains(ma_ban_doc):
            return False
        for _, t in self._tracks.items():
            if t.ma_ban_doc == ma_ban_doc and t.trang_thai != TrackStatus.RETURNED:
                return False
        return self._readers.remove(ma_ban_doc)

    def tim_doc_gia(self, ma_ban_doc: str):
        return self._readers.get(ma_ban_doc)

    # Nhóm 1 — cập nhật
    def cap_nhat_doc_gia(self, ma_ban_doc: str, **fields) -> bool:
        """Cập nhật thông tin độc giả.

        Các trường hợp lệ: ho_ten, ngay_sinh, gioi_tinh, dia_chi, so_dien_thoai.
        Raises: KeyError, ValueError
        """
        doc_gia = self._readers.get(ma_ban_doc)
        if doc_gia is None:
            raise KeyError(f"Khong tim thay doc gia '{ma_ban_doc}'.")
        ALLOWED = {"ho_ten", "ngay_sinh", "gioi_tinh", "dia_chi", "so_dien_thoai"}
        for field, value in fields.items():
            if field not in ALLOWED:
                raise ValueError(f"Truong '{field}' khong duoc phep cap nhat.")
            if field == "ngay_sinh" and not Validator.is_valid_date(value):
                raise ValueError("ngay_sinh phai theo dinh dang YYYY-MM-DD.")
            if field == "so_dien_thoai" and not Validator.is_valid_phone(value):
                raise ValueError("so_dien_thoai khong hop le.")
            if field == "gioi_tinh" and not isinstance(value, Gender):
                raise ValueError("gioi_tinh phai la Gender.")
            setattr(doc_gia, field, value)
        return True

    def lay_tat_ca_doc_gia(self) -> List:
        result = List()
        for _, r in self._readers.items():
            result.append(r)
        return result

    def tim_doc_gia_theo_ten(self, keyword: str) -> List:
        result = List()
        for _, r in self._readers.items():
            if self._match(r.ho_ten, keyword):
                result.append(r)
        return result

    def loc_doc_gia(self, gioi_tinh: Gender = None) -> List:
        result = List()
        for _, r in self._readers.items():
            match_gioi_tinh = True

            
            if gioi_tinh is not None and r.gioi_tinh != gioi_tinh:
                match_gioi_tinh = False
                
            if match_gioi_tinh:
                result.append(r)
        return result

    # ═══════════════════════════════════════════════════════════
    #  MƯỢN SÁCH
    # ═══════════════════════════════════════════════════════════

    def muon_sach(self, ma_phieu: str, ma_sach: str, ma_ban_doc: str,
                  ngay_muon: str, han_tra: str) -> int:
        """Tạo phiếu mượn.

        Return codes:
            0 = OK
            1 = Ma phieu khong hop le hoac da ton tai
            2 = Khong tim thay sach
            3 = Het sach
            4 = Khong tim thay doc gia
            5 = Vuot gioi han muon
            6 = Ngay khong hop le
            7 = Han tra phai sau ngay muon
        """
        if not Validator.is_valid_id(ma_phieu) or self._tracks.contains(ma_phieu):
            return 1
        if not Validator.is_valid_date(ngay_muon) or not Validator.is_valid_date(han_tra):
            return 6
        if TrackBook._days_between(ngay_muon, han_tra) <= 0:
            return 7

        sach = self._books.get(ma_sach)
        if sach is None:
            return 2
        if sach.so_luong <= 0:
            return 3

        doc_gia = self._readers.get(ma_ban_doc)
        if doc_gia is None:
            return 4

        dang_muon = sum(
            1 for _, t in self._tracks.items()
            if t.ma_ban_doc == ma_ban_doc and t.trang_thai != TrackStatus.RETURNED
        )
        if dang_muon >= MAX_BORROW_PER_READER:
            return 5

        sach.so_luong -= 1
        self._tracks.put(ma_phieu, TrackBook(
            ma_phieu=ma_phieu, ma_sach=ma_sach, ma_ban_doc=ma_ban_doc,
            ngay_muon=ngay_muon, han_tra=han_tra,
        ))
        return 0

    # ═══════════════════════════════════════════════════════════
    #  TRẢ SÁCH
    # ═══════════════════════════════════════════════════════════

    def tra_sach(self, ma_phieu: str, ngay_tra: str) -> int:
        """Trả sách và tự tạo phiếu phạt nếu trễ.

        Return codes:
            0 = OK
            1 = Khong tim thay phieu
            2 = Da tra roi
            3 = Ngay khong hop le
        """
        if not Validator.is_valid_date(ngay_tra):
            return 3
        track = self._tracks.get(ma_phieu)
        if track is None:
            return 1
        if track.trang_thai == TrackStatus.RETURNED:
            return 2

        track.ngay_tra_thuc_te = ngay_tra
        so_ngay_tre = track.soNgayTre(ngay_tra)
        track.trang_thai = TrackStatus.RETURNED

        sach = self._books.get(track.ma_sach)
        if sach:
            sach.so_luong += 1

        if so_ngay_tre > 0:
            fine = Fine(
                ma_phat=f"FINE_{ma_phieu}",
                ma_phieu=ma_phieu,
                ly_do=FineReason.OVERDUE,
                so_ngay_tre=so_ngay_tre,
                tien_phat_ngay=so_ngay_tre * FINE_PER_DAY,
            )
            self._fines.put(fine.ma_phat, fine)
        return 0

    def tim_phieu_muon(self, ma_phieu: str):
        return self._tracks.get(ma_phieu)

    def lay_phieu_muon_theo_doc_gia(self, ma_ban_doc: str) -> List:
        result = List()
        for _, t in self._tracks.items():
            if t.ma_ban_doc == ma_ban_doc:
                result.append(t)
        return result

    def lay_tat_ca_phieu_muon(self) -> List:
        result = List()
        for _, t in self._tracks.items():
            result.append(t)
        return result

    def cap_nhat_trang_thai_phieu(self, ngay_hien_tai: str) -> None:
        """Duyệt và cập nhật trạng thái tất cả phiếu theo ngày hôm nay."""
        for _, t in self._tracks.items():
            t.updateStatus(ngay_hien_tai)

    # ═══════════════════════════════════════════════════════════
    #  Nhóm 2 — GIA HẠN MƯỢN SÁCH
    # ═══════════════════════════════════════════════════════════

    def gia_han_muon(self, ma_phieu: str, han_tra_moi: str) -> int:
        """Gia hạn hạn trả sách.

        Điều kiện: phiếu chưa trả, chưa vượt MAX_RENEW, hạn mới > hạn cũ.

        Return codes:
            0 = OK
            1 = Khong tim thay phieu
            2 = Phieu da tra
            3 = Vuot so lan gia han toi da
            4 = Han moi phai sau han hien tai
            5 = Ngay khong hop le
        """
        if not Validator.is_valid_date(han_tra_moi):
            return 5
        track = self._tracks.get(ma_phieu)
        if track is None:
            return 1
        if track.trang_thai == TrackStatus.RETURNED:
            return 2
        if track.so_lan_gia_han >= TrackBook.MAX_RENEW:
            return 3
        if TrackBook._days_between(track.han_tra, han_tra_moi) <= 0:
            return 4

        track.han_tra         = han_tra_moi
        track.so_lan_gia_han += 1
        track.trang_thai      = TrackStatus.BORROWING  # reset neu dang OVERDUE
        return 0

    # ═══════════════════════════════════════════════════════════
    #  Nhóm 3 — BÁO MẤT / HƯ HỎNG SÁCH
    # ═══════════════════════════════════════════════════════════

    def bao_mat_sach(self, ma_phieu: str, ngay_bao: str) -> int:
        """Báo mất sách: đánh dấu RETURNED, KHÔNG hoàn soluong, tạo phạt LOST.

        Return codes:
            0 = OK
            1 = Khong tim thay phieu
            2 = Phieu da tra roi
            3 = Ngay khong hop le
            4 = Da co phieu phat cho phieu nay
        """
        if not Validator.is_valid_date(ngay_bao):
            return 3
        track = self._tracks.get(ma_phieu)
        if track is None:
            return 1
        if track.trang_thai == TrackStatus.RETURNED:
            return 2
        ma_phat = f"LOST_{ma_phieu}"
        if self._fines.contains(ma_phat):
            return 4

        track.ngay_tra_thuc_te = ngay_bao
        track.trang_thai = TrackStatus.RETURNED
        # Không hoàn so_luong vì sách mất

        so_ngay_tre = max(0, track.soNgayTre(ngay_bao))
        fine = Fine(
            ma_phat=ma_phat, ma_phieu=ma_phieu,
            ly_do=FineReason.LOST,
            so_ngay_tre=so_ngay_tre,
            tien_phat_ngay=so_ngay_tre * FINE_PER_DAY,
            tien_phat_sach=FINE_LOST,
        )
        self._fines.put(fine.ma_phat, fine)
        return 0

    def bao_hu_sach(self, ma_phieu: str, ngay_bao: str) -> int:
        """Báo hư hỏng sách: RETURNED, hoàn so_luong, cập nhật USED, tạo phạt DAMAGE.

        Return codes:
            0 = OK
            1 = Khong tim thay phieu
            2 = Phieu da tra roi
            3 = Ngay khong hop le
            4 = Da co phieu phat cho phieu nay
        """
        if not Validator.is_valid_date(ngay_bao):
            return 3
        track = self._tracks.get(ma_phieu)
        if track is None:
            return 1
        if track.trang_thai == TrackStatus.RETURNED:
            return 2
        ma_phat = f"DMG_{ma_phieu}"
        if self._fines.contains(ma_phat):
            return 4

        track.ngay_tra_thuc_te = ngay_bao
        track.trang_thai = TrackStatus.RETURNED

        sach = self._books.get(track.ma_sach)
        if sach:
            sach.so_luong  += 1
            sach.tinh_trang = BookCondition.USED

        so_ngay_tre = max(0, track.soNgayTre(ngay_bao))
        fine = Fine(
            ma_phat=ma_phat, ma_phieu=ma_phieu,
            ly_do=FineReason.DAMAGED,
            so_ngay_tre=so_ngay_tre,
            tien_phat_ngay=so_ngay_tre * FINE_PER_DAY,
            tien_phat_sach=FINE_DAMAGE,
        )
        self._fines.put(fine.ma_phat, fine)
        return 0

    # ═══════════════════════════════════════════════════════════
    #  Nhóm 4 — TÌM KIẾM / LỌC NÂNG CAO
    # ═══════════════════════════════════════════════════════════

    def lay_phieu_theo_trang_thai(self, trang_thai: TrackStatus) -> List:
        """Lọc phiếu mượn theo trạng thái."""
        result = List()
        for _, t in self._tracks.items():
            if t.trang_thai == trang_thai:
                result.append(t)
        return result

    def lay_phieu_qua_han(self) -> List:
        """Danh sách phiếu đang quá hạn."""
        return self.lay_phieu_theo_trang_thai(TrackStatus.OVERDUE)

    def lay_phat_theo_doc_gia(self, ma_ban_doc: str) -> List:
        """Phiếu phạt của một độc giả."""
        ma_phieu_set = {
            t.ma_phieu
            for _, t in self._tracks.items()
            if t.ma_ban_doc == ma_ban_doc
        }
        result = List()
        for _, f in self._fines.items():
            if f.ma_phieu in ma_phieu_set:
                result.append(f)
        return result

    def lay_phat_chua_thanh_toan(self) -> List:
        result = List()
        for _, f in self._fines.items():
            if not f.da_thanh_toan:
                result.append(f)
        return result

    # ═══════════════════════════════════════════════════════════
    #  PHẠT — CRUD
    # ═══════════════════════════════════════════════════════════

    def them_phieu_phat(self, fine: Fine) -> bool:
        if not fine.ma_phat or self._fines.contains(fine.ma_phat):
            return False
        self._fines.put(fine.ma_phat, fine)
        return True

    def tim_phieu_phat(self, ma_phat: str):
        return self._fines.get(ma_phat)

    def thanh_toan_phat(self, ma_phat: str) -> bool:
        fine = self._fines.get(ma_phat)
        if fine is None or fine.da_thanh_toan:
            return False
        fine.thanhToan()
        return True

    def lay_tat_ca_phat(self) -> List:
        result = List()
        for _, f in self._fines.items():
            result.append(f)
        return result

    # ═══════════════════════════════════════════════════════════
    #  Nhóm 5 — LƯU / TẢI DỮ LIỆU JSON
    # ═══════════════════════════════════════════════════════════

    def luu_du_lieu(self, thu_muc: str = ".") -> bool:
        """Lưu 4 file JSON vào thu_muc: books, readers, tracks, fines."""
        try:
            os.makedirs(thu_muc, exist_ok=True)
            _save_json(os.path.join(thu_muc, "books.json"),
                       [b.to_dict() for _, b in self._books.items()])
            _save_json(os.path.join(thu_muc, "readers.json"),
                       [r.to_dict() for _, r in self._readers.items()])
            _save_json(os.path.join(thu_muc, "tracks.json"),
                       [t.to_dict() for _, t in self._tracks.items()])
            _save_json(os.path.join(thu_muc, "fines.json"),
                       [f.to_dict() for _, f in self._fines.items()])
            return True
        except OSError:
            return False

    def tai_du_lieu(self, thu_muc: str = ".") -> bool:
        """Tải dữ liệu từ 4 file JSON trong thu_muc. Dữ liệu cũ bị xóa."""
        try:
            self._books   = HashTable()
            self._readers = HashTable()
            self._tracks  = HashTable()
            self._fines   = HashTable()

            for d in _load_json(os.path.join(thu_muc, "books.json")):
                b = Book.from_dict(d); self._books.put(b.ma_sach, b)
            for d in _load_json(os.path.join(thu_muc, "readers.json")):
                r = Reader.from_dict(d); self._readers.put(r.ma_ban_doc, r)
            for d in _load_json(os.path.join(thu_muc, "tracks.json")):
                t = TrackBook.from_dict(d); self._tracks.put(t.ma_phieu, t)
            for d in _load_json(os.path.join(thu_muc, "fines.json")):
                f = Fine.from_dict(d); self._fines.put(f.ma_phat, f)
            return True
        except (OSError, KeyError, ValueError):
            return False

    # ═══════════════════════════════════════════════════════════
    #  Nhóm 6 — THỐNG KÊ
    # ═══════════════════════════════════════════════════════════

    # -- cơ bản --
    def tong_dau_sach(self)     -> int: return len(self._books)
    def tong_doc_gia(self)      -> int: return len(self._readers)
    def tong_phieu_muon(self)   -> int: return len(self._tracks)
    def tong_phieu_phat(self)   -> int: return len(self._fines)

    def tong_dang_muon(self) -> int:
        return sum(1 for _, t in self._tracks.items()
                   if t.trang_thai in (TrackStatus.BORROWING, TrackStatus.OVERDUE))

    def tong_qua_han(self) -> int:
        return sum(1 for _, t in self._tracks.items()
                   if t.trang_thai == TrackStatus.OVERDUE)

    def tong_tien_phat_chua_thu(self) -> float:
        return sum(f.tong_tien_phat for _, f in self._fines.items()
                   if not f.da_thanh_toan)

    # -- nâng cao --
    def top_sach_duoc_muon_nhieu(self, n: int = 5) -> List:
        """Top N sách được mượn nhiều nhất. Trả List of (Book, int)."""
        dem: dict = {}
        for _, t in self._tracks.items():
            dem[t.ma_sach] = dem.get(t.ma_sach, 0) + 1

        pairs = [(self._books.get(ma), cnt)
                 for ma, cnt in dem.items() if self._books.get(ma)]

        # Insertion sort giảm dần
        for i in range(1, len(pairs)):
            key = pairs[i]; j = i - 1
            while j >= 0 and pairs[j][1] < key[1]:
                pairs[j + 1] = pairs[j]; j -= 1
            pairs[j + 1] = key

        result = List()
        for item in pairs[:n]:
            result.append(item)
        return result

    def top_doc_gia_muon_nhieu(self, n: int = 5) -> List:
        """Top N độc giả mượn nhiều nhất. Trả List of (Reader, int)."""
        dem: dict = {}
        for _, t in self._tracks.items():
            dem[t.ma_ban_doc] = dem.get(t.ma_ban_doc, 0) + 1

        pairs = [(self._readers.get(ma), cnt)
                 for ma, cnt in dem.items() if self._readers.get(ma)]

        for i in range(1, len(pairs)):
            key = pairs[i]; j = i - 1
            while j >= 0 and pairs[j][1] < key[1]:
                pairs[j + 1] = pairs[j]; j -= 1
            pairs[j + 1] = key

        result = List()
        for item in pairs[:n]:
            result.append(item)
        return result
