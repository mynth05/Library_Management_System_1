"""Các lớp đối tượng nghiệp vụ cho hệ thống quản lý thư viện."""

from enum import Enum
from custom_structures import List, HashTable


# ─────────────────────────── Enums ───────────────────────────

class BookCondition(Enum):
    NEW    = "new"
    USED   = "used"


class Gender(Enum):
    MALE   = "male"
    FEMALE = "female"
    OTHER  = "other"


class FineReason(Enum):
    OVERDUE = "overdue"
    DAMAGED = "damaged"
    LOST    = "lost"


class TrackStatus(Enum):
    BORROWING = "borrowing"
    RETURNED  = "returned"
    OVERDUE   = "overdue"


# ─────────────────────────── Book ───────────────────────────

class Book:
    def __init__(
        self,
        ma_sach: str,
        ten_sach: str,
        tac_gia: str,
        the_loai: str,
        nha_xuat_ban: str,
        so_luong: int,
        tinh_trang: BookCondition = BookCondition.NEW,
    ):
        self.ma_sach      = ma_sach
        self.ten_sach     = ten_sach
        self.tac_gia      = tac_gia
        self.the_loai     = the_loai
        self.nha_xuat_ban = nha_xuat_ban
        self.so_luong     = so_luong
        self.tinh_trang   = tinh_trang

    def to_dict(self) -> dict:
        return {
            "ma_sach":      self.ma_sach,
            "ten_sach":     self.ten_sach,
            "tac_gia":      self.tac_gia,
            "the_loai":     self.the_loai,
            "nha_xuat_ban": self.nha_xuat_ban,
            "so_luong":     self.so_luong,
            "tinh_trang":   self.tinh_trang.value,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Book":
        return cls(
            ma_sach      = d["ma_sach"],
            ten_sach     = d["ten_sach"],
            tac_gia      = d["tac_gia"],
            the_loai     = d["the_loai"],
            nha_xuat_ban = d["nha_xuat_ban"],
            so_luong     = int(d["so_luong"]),
            tinh_trang   = BookCondition(d["tinh_trang"]),
        )

    def __str__(self):
        return (
            f"[Sách] {self.ma_sach} | {self.ten_sach} | "
            f"Tác giả: {self.tac_gia} | Thể loại: {self.the_loai} | "
            f"NXB: {self.nha_xuat_ban} | SL: {self.so_luong} | "
            f"Tình trạng: {self.tinh_trang.value}"
        )


# ─────────────────────────── Reader ───────────────────────────

class Reader:
    def __init__(
        self,
        ma_ban_doc: str,
        ho_ten: str,
        ngay_sinh: str,
        gioi_tinh: Gender,
        dia_chi: str,
        so_dien_thoai: str,
    ):
        self.ma_ban_doc    = ma_ban_doc
        self.ho_ten        = ho_ten
        self.ngay_sinh     = ngay_sinh
        self.gioi_tinh     = gioi_tinh
        self.dia_chi       = dia_chi
        self.so_dien_thoai = so_dien_thoai

    def to_dict(self) -> dict:
        return {
            "ma_ban_doc":    self.ma_ban_doc,
            "ho_ten":        self.ho_ten,
            "ngay_sinh":     self.ngay_sinh,
            "gioi_tinh":     self.gioi_tinh.value,
            "dia_chi":       self.dia_chi,
            "so_dien_thoai": self.so_dien_thoai,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Reader":
        return cls(
            ma_ban_doc    = d["ma_ban_doc"],
            ho_ten        = d["ho_ten"],
            ngay_sinh     = d["ngay_sinh"],
            gioi_tinh     = Gender(d["gioi_tinh"]),
            dia_chi       = d["dia_chi"],
            so_dien_thoai = d["so_dien_thoai"],
        )

    def __str__(self):
        return (
            f"Mã bạn đọc: {self.ma_ban_doc} | Họ tên: {self.ho_ten} | "
            f"Ngày sinh: {self.ngay_sinh} | Giới tính: {self.gioi_tinh.value} | "
            f"Địa chỉ: {self.dia_chi} | Số điện thoại: {self.so_dien_thoai}"
        )


# ─────────────────────────── TrackBook ───────────────────────────

class TrackBook:
    MAX_RENEW = 3

    def __init__(
        self,
        ma_phieu: str,
        ma_sach: str,
        ma_ban_doc: str,
        ngay_muon: str,
        han_tra: str,
        ngay_tra_thuc_te: str = "",
        trang_thai: TrackStatus = TrackStatus.BORROWING,
        so_lan_gia_han: int = 0,
    ):
        self.ma_phieu         = ma_phieu
        self.ma_sach          = ma_sach
        self.ma_ban_doc       = ma_ban_doc
        self.ngay_muon        = ngay_muon
        self.han_tra          = han_tra
        self.ngay_tra_thuc_te = ngay_tra_thuc_te
        self.trang_thai       = trang_thai
        self.so_lan_gia_han   = so_lan_gia_han

    # ── helpers ──────────────────────────────────────────────

    @staticmethod
    def _parse_date(date_str: str):
        parts = date_str.split("-")
        return int(parts[0]), int(parts[1]), int(parts[2])

    @staticmethod
    def _days_between(d1: str, d2: str) -> int:
        def to_jdn(y, m, d):
            a  = (14 - m) // 12
            y2 = y + 4800 - a
            m2 = m + 12 * a - 3
            return d + (153 * m2 + 2) // 5 + 365 * y2 + y2 // 4 - y2 // 100 + y2 // 400 - 32045

        y1, mo1, da1 = TrackBook._parse_date(d1)
        y2, mo2, da2 = TrackBook._parse_date(d2)
        return to_jdn(y2, mo2, da2) - to_jdn(y1, mo1, da1)

    # ── business methods ─────────────────────────────────────

    def isOverdue(self, today: str) -> bool:
        if self.trang_thai == TrackStatus.RETURNED:
            return False
        return self._days_between(self.han_tra, today) > 0

    def soNgayTre(self, today: str) -> int:
        ref  = self.ngay_tra_thuc_te if self.trang_thai == TrackStatus.RETURNED else today
        late = self._days_between(self.han_tra, ref)
        return max(0, late)

    def updateStatus(self, today: str) -> None:
        if self.trang_thai == TrackStatus.RETURNED:
            return
        self.trang_thai = TrackStatus.OVERDUE if self.isOverdue(today) else TrackStatus.BORROWING

    # ── serialization ─────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "ma_phieu":         self.ma_phieu,
            "ma_sach":          self.ma_sach,
            "ma_ban_doc":       self.ma_ban_doc,
            "ngay_muon":        self.ngay_muon,
            "han_tra":          self.han_tra,
            "ngay_tra_thuc_te": self.ngay_tra_thuc_te,
            "trang_thai":       self.trang_thai.value,
            "so_lan_gia_han":   self.so_lan_gia_han,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "TrackBook":
        return cls(
            ma_phieu         = d["ma_phieu"],
            ma_sach          = d["ma_sach"],
            ma_ban_doc       = d["ma_ban_doc"],
            ngay_muon        = d["ngay_muon"],
            han_tra          = d["han_tra"],
            ngay_tra_thuc_te = d.get("ngay_tra_thuc_te", ""),
            trang_thai       = TrackStatus(d["trang_thai"]),
            so_lan_gia_han   = d.get("so_lan_gia_han", 0),
        )

    def __str__(self):
        tra = self.ngay_tra_thuc_te or "chưa trả"
        return (
            f"[Phiếu mượn] {self.ma_phieu} | Sách: {self.ma_sach} | "
            f"Độc giả: {self.ma_ban_doc} | Mượn: {self.ngay_muon} | "
            f"Hạn trả: {self.han_tra} | Trả thực tế: {tra} | "
            f"Trạng thái: {self.trang_thai.value} | Gia hạn: {self.so_lan_gia_han} lần"
        )

# ─────────────────────────── Fine ───────────────────────────

class Fine:
    FINE_PER_DAY = 5_000.0
    FINE_DAMAGED = 100_000.0
    FINE_LOST    = 300_000.0

    def __init__(
        self,
        ma_phat: str,
        ma_phieu: str,
        ly_do: FineReason,
        so_ngay_tre: int = 0,
        tien_phat_ngay: float = 0.0,
        tien_phat_sach: float = 0.0,
        da_thanh_toan: bool = False,
    ):
        self.ma_phat        = ma_phat
        self.ma_phieu       = ma_phieu
        self.ly_do          = ly_do
        self.so_ngay_tre    = so_ngay_tre
        self.tien_phat_ngay = tien_phat_ngay
        self.tien_phat_sach = tien_phat_sach
        self.tong_tien_phat = tien_phat_ngay + tien_phat_sach
        self.da_thanh_toan  = da_thanh_toan

    @classmethod
    def tu_phieu_muon(cls, ma_phat: str, track: TrackBook, today: str) -> "Fine":
        so_ngay    = track.soNgayTre(today)
        phat_ngay  = so_ngay * cls.FINE_PER_DAY
        return cls(
            ma_phat        = ma_phat,
            ma_phieu       = track.ma_phieu,
            ly_do          = FineReason.OVERDUE,
            so_ngay_tre    = so_ngay,
            tien_phat_ngay = phat_ngay,
            tien_phat_sach = 0.0,
        )

    def thanhToan(self) -> None:
        if self.da_thanh_toan:
            raise ValueError(f"Fine {self.ma_phat!r} đã được thanh toán trước đó.")
        self.da_thanh_toan = True

    # ── serialization ─────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "ma_phat":        self.ma_phat,
            "ma_phieu":       self.ma_phieu,
            "ly_do":          self.ly_do.value,
            "so_ngay_tre":    self.so_ngay_tre,
            "tien_phat_ngay": self.tien_phat_ngay,
            "tien_phat_sach": self.tien_phat_sach,
            "tong_tien_phat": self.tong_tien_phat,
            "da_thanh_toan":  self.da_thanh_toan,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Fine":
        return cls(
            ma_phat        = d["ma_phat"],
            ma_phieu       = d["ma_phieu"],
            ly_do          = FineReason(d["ly_do"]),
            so_ngay_tre    = int(d["so_ngay_tre"]),
            tien_phat_ngay = float(d["tien_phat_ngay"]),
            tien_phat_sach = float(d["tien_phat_sach"]),
            da_thanh_toan  = bool(d["da_thanh_toan"]),
        )

    def __str__(self):
        trang_thai = "Đã thanh toán" if self.da_thanh_toan else "Chưa thanh toán"
        return (
            f"[Phiếu phạt] {self.ma_phat} | Phiếu mượn: {self.ma_phieu} | "
            f"Lý do: {self.ly_do.value} | Trễ: {self.so_ngay_tre} ngày | "
            f"Phạt ngày: {self.tien_phat_ngay:,.0f}đ | "
            f"Phạt sách: {self.tien_phat_sach:,.0f}đ | "
            f"Tổng: {self.tong_tien_phat:,.0f}đ | {trang_thai}"
        )