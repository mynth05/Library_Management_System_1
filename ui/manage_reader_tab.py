"""Giao diện quản lí bạn đọc — thêm, sửa, xóa, tìm kiếm, lọc."""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models import Reader, Gender
from ui.widgets import (
    nhap_chuoi, nhap_ngay, chon_menu, xac_nhan,
    in_tieu_de, in_bang_ban_doc,
)


# ─────────────────────────────────────────────────────────────────
#  Màn hình chính — Quản lí Bạn Đọc
# ─────────────────────────────────────────────────────────────────

def man_hinh_quan_li_ban_doc(app) -> None:
    """Vòng lặp giao diện quản lí bạn đọc."""
    MENU = [
        "Thêm bạn đọc mới",
        "Cập nhật thông tin bạn đọc",
        "Xóa bạn đọc",
        "Tìm bạn đọc",
        "Lọc bạn đọc (giới tính)",
        "Xem tất cả bạn đọc",
        "Quay lại",
    ]

    while True:
        in_tieu_de("QUẢN LÍ BẠN ĐỌC")
        lua_chon = chon_menu(MENU)

        if lua_chon == 1:
            _them_ban_doc(app)
        elif lua_chon == 2:
            _cap_nhat_ban_doc(app)
        elif lua_chon == 3:
            _xoa_ban_doc(app)
        elif lua_chon == 4:
            _tim_ban_doc(app)
        elif lua_chon == 5:
            _loc_ban_doc(app)
        elif lua_chon == 6:
            _xem_tat_ca(app)
        elif lua_chon == 7:
            break


# ─────────────────────────────────────────────────────────────────
#  Chức năng con
# ─────────────────────────────────────────────────────────────────

def _chon_gioi_tinh() -> Gender:
    print("Giới tính: 1. Nam   2. Nữ   3. Khác")
    c = chon_menu(["Nam", "Nữ", "Khác"])
    return {1: Gender.MALE, 2: Gender.FEMALE, 3: Gender.OTHER}[c]


def _them_ban_doc(app) -> None:
    in_tieu_de("THÊM BẠN ĐỌC MỚI")
    from app_logic import Validator
    while True:
        ma_ban_doc = nhap_chuoi("Mã bạn đọc: ")
        if not Validator.is_valid_id(ma_ban_doc):
            print("Mã bạn đọc không hợp lệ (chỉ chứa chữ, số, gạch ngang, gạch dưới). Vui lòng nhập lại!")
            continue
        if app.tim_doc_gia(ma_ban_doc) is not None:
            print("Mã bạn đọc đã tồn tại trên hệ thống. Vui lòng nhập mã bạn đọc khác!")
        else:
            break

    ho_ten        = nhap_chuoi("Họ tên: ")
    ngay_sinh     = nhap_ngay("Ngày sinh (YYYY-MM-DD): ")
    gioi_tinh     = _chon_gioi_tinh()
    dia_chi       = nhap_chuoi("Địa chỉ: ")
    so_dien_thoai = nhap_chuoi("Số điện thoại (10 số, bắt đầu 0): ")

    doc_gia = Reader(ma_ban_doc, ho_ten, ngay_sinh, gioi_tinh, dia_chi, so_dien_thoai)
    if app.them_doc_gia(doc_gia):
        print(f"\nĐã thêm bạn đọc '{ho_ten}' thành công.")
        app.luu_du_lieu("data/readers.json")
    else:
        print("\nThêm bạn đọc thất bại. Lỗi dữ liệu không hợp lệ.")
    input("\nNhấn Enter để tiếp tục...")


def _cap_nhat_ban_doc(app) -> None:
    in_tieu_de("CẬP NHẬT THÔNG TIN BẠN ĐỌC")
    ma_ban_doc = nhap_chuoi("Nhập mã bạn đọc cần cập nhật: ")
    doc_gia = app.tim_doc_gia(ma_ban_doc)
    if doc_gia is None:
        print("Không tìm thấy bạn đọc.")
        input("\nNhấn Enter để tiếp tục...")
        return

    print(f"\nThông tin hiện tại: {doc_gia}")
    TRUONG_MENU = ["ho_ten", "ngay_sinh", "gioi_tinh", "dia_chi", "so_dien_thoai", "Xong"]
    while True:
        lua_chon = chon_menu(TRUONG_MENU)
        if lua_chon == len(TRUONG_MENU):
            break
        ten_truong = TRUONG_MENU[lua_chon - 1]
        try:
            if ten_truong == "ngay_sinh":
                gia_tri = nhap_ngay("Ngày sinh mới (YYYY-MM-DD): ")
            elif ten_truong == "gioi_tinh":
                gia_tri = _chon_gioi_tinh()
            else:
                gia_tri = nhap_chuoi(f"Giá trị mới cho '{ten_truong}': ")
            app.cap_nhat_doc_gia(ma_ban_doc, **{ten_truong: gia_tri})
            print(f"Đã cập nhật '{ten_truong}'.")
            app.luu_du_lieu("data/readers.json")
        except (KeyError, ValueError) as e:
            print(f"Lỗi: {e}")
    input("\nNhấn Enter để tiếp tục...")


def _xoa_ban_doc(app) -> None:
    in_tieu_de("XÓA BẠN ĐỌC")
    ma_ban_doc = nhap_chuoi("Nhập mã bạn đọc cần xóa: ")
    doc_gia = app.tim_doc_gia(ma_ban_doc)
    if doc_gia is None:
        print("Không tìm thấy bạn đọc.")
    elif not xac_nhan(f"Bạn có chắc muốn xóa bạn đọc '{doc_gia.ho_ten}'? (y/n): "):
        print("Đã hủy.")
    elif app.xoa_doc_gia(ma_ban_doc):
        print("Đã xóa bạn đọc thành công.")
        app.luu_du_lieu("data/readers.json")
    else:
        print("Không thể xóa. Bạn đọc đang có sách mượn chưa trả.")
    input("\nNhấn Enter để tiếp tục...")


def _tim_ban_doc(app) -> None:
    in_tieu_de("TÌM BẠN ĐỌC")
    print("Chọn phương thức tìm kiếm:")
    lua_chon = chon_menu(["Tìm theo mã bạn đọc", "Tìm theo tên bạn đọc"])

    if lua_chon == 1:
        ma_ban_doc = nhap_chuoi("Nhập mã bạn đọc: ")
        doc_gia = app.tim_doc_gia(ma_ban_doc)
        if doc_gia:
            print(f"\n{doc_gia}")
        else:
            print("Không tìm thấy bạn đọc.")
    elif lua_chon == 2:
        keyword = nhap_chuoi("Nhập từ khóa họ tên: ")
        ket_qua = app.tim_doc_gia_theo_ten(keyword)
        in_bang_ban_doc(ket_qua, f"Kết quả tìm kiếm: '{keyword}'")

    input("\nNhấn Enter để tiếp tục...")


def _loc_ban_doc(app) -> None:
    in_tieu_de("LỌC BẠN ĐỌC")
    print("Lọc theo giới tính: 1. Nam  2. Nữ  3. Khác  4. Tất cả")
    c = chon_menu(["Nam", "Nữ", "Khác", "Tất cả"])
    gioi_tinh = {1: Gender.MALE, 2: Gender.FEMALE, 3: Gender.OTHER, 4: None}[c]

    ket_qua = app.loc_doc_gia(gioi_tinh=gioi_tinh)
    in_bang_ban_doc(ket_qua, "Kết quả lọc")
    input("\nNhấn Enter để tiếp tục...")


def _xem_tat_ca(app) -> None:
    in_tieu_de("DANH SÁCH TẤT CẢ BẠN ĐỌC")
    tat_ca = app.lay_tat_ca_doc_gia()
    in_bang_ban_doc(tat_ca, "Tất cả bạn đọc")
    input("\nNhấn Enter để tiếp tục...")

