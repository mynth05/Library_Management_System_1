# -*- coding: utf-8 -*-
"""Giao diện quản lí sách — thêm, sửa, xóa, tìm kiếm, lọc, sắp xếp."""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models import Book, BookCondition
from ui.widgets import nhap_chuoi, nhap_so_nguyen, chon_menu, xac_nhan, in_tieu_de, in_bang_sach


# ─────────────────────────────────────────────────────────────────
#  Màn hình chính — Quản lí Sách
# ─────────────────────────────────────────────────────────────────

def man_hinh_quan_li_sach(app) -> None:
    """Vòng lặp giao diện quản lí sách."""
    MENU = [
        "Thêm sách mới",
        "Cập nhật thông tin sách",
        "Xóa sách",
        "Tìm sách",
        "Lọc sách (thể loại / tình trạng / NXB)",
        "Sắp xếp danh sách sách",
        "Xem tất cả sách",
        "Quay lại",
    ]

    while True:
        in_tieu_de("QUẢN LÍ SÁCH")
        lua_chon = chon_menu(MENU)

        if lua_chon == 1:
            _them_sach(app)
        elif lua_chon == 2:
            _cap_nhat_sach(app)
        elif lua_chon == 3:
            _xoa_sach(app)
        elif lua_chon == 4:
            _tim_kiem_sach(app)
        elif lua_chon == 5:
            _loc_sach(app)
        elif lua_chon == 6:
            _sap_xep_sach(app)
        elif lua_chon == 7:
            _xem_tat_ca(app)
        elif lua_chon == 8:
            break


# ─────────────────────────────────────────────────────────────────
#  Chức năng con
# ─────────────────────────────────────────────────────────────────

def _them_sach(app) -> None:
    in_tieu_de("THÊM SÁCH MỚI")
    from app_logic import Validator
    while True:
        ma_sach = nhap_chuoi("Mã sách (chữ/số/gạch ngang, gõ 'q' để hủy): ")
        if ma_sach.lower() == 'q':
            return
        if not Validator.is_valid_id(ma_sach):
            print("Mã sách không hợp lệ (chỉ chứa chữ, số, gạch ngang, gạch dưới). Vui lòng nhập lại!")
            continue
        if app.tim_sach(ma_sach) is not None:
            print("Mã sách đã tồn tại trên hệ thống. Vui lòng nhập mã sách khác!")
        else:
            break

    ten_sach     = nhap_chuoi("Tên sách: ")
    tac_gia      = nhap_chuoi("Tác giả: ")
    the_loai     = nhap_chuoi("Thể loại: ")
    nha_xuat_ban = nhap_chuoi("Nhà xuất bản: ")
    so_luong     = nhap_so_nguyen("Số lượng (≥ 0): ", min_val=0)

    print("Tình trạng:  1. Mới (new)   2. Đã dùng (used)")
    tuy_chon = chon_menu(["Mới", "Đã dùng"])
    tinh_trang = BookCondition.NEW if tuy_chon == 1 else BookCondition.USED

    sach = Book(ma_sach, ten_sach, tac_gia, the_loai, nha_xuat_ban, so_luong, tinh_trang)
    if app.them_sach(sach):
        print(f"\nĐã thêm sách '{ten_sach}' thành công.")
        app.luu_du_lieu("data")
    else:
        print("\nThêm sách thất bại. Lỗi dữ liệu không hợp lệ.")
    input("\nNhấn Enter để tiếp tục...")


def _cap_nhat_sach(app) -> None:
    in_tieu_de("CẬP NHẬT THÔNG TIN SÁCH")
    ma_sach = nhap_chuoi("Nhập mã sách cần cập nhật: ")
    sach = app.tim_sach(ma_sach)
    if sach is None:
        print("✘ Không tìm thấy sách.")
        input("\nNhấn Enter để tiếp tục...")
        return

    print(f"\nThông tin hiện tại: {sach}")
    print("\nChọn trường cần cập nhật:")
    TRUONG_MENU = ["ten_sach", "tac_gia", "the_loai", "nha_xuat_ban", "so_luong", "tinh_trang", "Xong"]
    while True:
        lua_chon = chon_menu(TRUONG_MENU)
        if lua_chon == len(TRUONG_MENU):  # Xong
            break
        ten_truong = TRUONG_MENU[lua_chon - 1]
        try:
            if ten_truong == "so_luong":
                gia_tri = nhap_so_nguyen("Số lượng mới (≥ 0): ", min_val=0)
            elif ten_truong == "tinh_trang":
                print("1. Mới (new)   2. Đã dùng (used)")
                c = chon_menu(["Mới", "Đã dùng"])
                gia_tri = BookCondition.NEW if c == 1 else BookCondition.USED
            else:
                gia_tri = nhap_chuoi(f"Giá trị mới cho '{ten_truong}': ")
            app.cap_nhat_sach(ma_sach, **{ten_truong: gia_tri})
            print(f"Đã cập nhật '{ten_truong}'.")
            app.luu_du_lieu("data")
        except (KeyError, ValueError) as e:
            print(f"Lỗi: {e}")
    input("\nNhấn Enter để tiếp tục...")


def _xoa_sach(app) -> None:
    in_tieu_de("XÓA SÁCH")
    ma_sach = nhap_chuoi("Nhập mã sách cần xóa: ")
    sach = app.tim_sach(ma_sach)
    if sach is None:
        print("✘ Không tìm thấy sách.")
    elif not xac_nhan(f"Bạn có chắc muốn xóa sách '{sach.ten_sach}'? (y/n): "):
        print("Đã hủy.")
    elif app.xoa_sach(ma_sach):
        print("Đã xóa sách thành công.")
        app.luu_du_lieu("data")
    else:
        print("Không thể xóa. Sách đang được mượn.")
    input("\nNhấn Enter để tiếp tục...")


def _tim_kiem_sach(app) -> None:
    in_tieu_de("TÌM SÁCH")
    print("Chọn phương thức tìm kiếm:")
    lua_chon = chon_menu(["Tìm theo mã sách", "Tìm theo tên sách"])

    if lua_chon == 1:
        ma_sach = nhap_chuoi("Nhập mã sách: ")
        sach = app.tim_sach(ma_sach)
        if sach:
            print(f"\n{sach}")
        else:
            print("Không tìm thấy sách.")
    elif lua_chon == 2:
        keyword = nhap_chuoi("Nhập từ khóa tên sách: ")
        ket_qua = app.tim_sach_theo_ten(keyword)
        in_bang_sach(ket_qua, f"Kết quả tìm kiếm: '{keyword}'")

    input("\nNhấn Enter để tiếp tục...")

def _loc_sach(app) -> None:
    in_tieu_de("LỌC SÁCH")
    the_loai = input("Thể loại (Enter để bỏ qua): ").strip() or None
    print("Tình trạng: 1. Mới  2. Đã dùng  3. Tất cả")
    c = chon_menu(["Mới", "Đã dùng", "Tất cả"])
    tinh_trang = {1: BookCondition.NEW, 2: BookCondition.USED, 3: None}[c]
    nha_xuat_ban = input("Nhà xuất bản (Enter để bỏ qua): ").strip() or None

    ket_qua = app.loc_sach(the_loai=the_loai, tinh_trang=tinh_trang, nha_xuat_ban=nha_xuat_ban)
    in_bang_sach(ket_qua, "Kết quả lọc")
    input("\nNhấn Enter để tiếp tục...")


def _sap_xep_sach(app) -> None:
    in_tieu_de("SẮP XẾP SÁCH")
    print("Sắp xếp theo: 1. Tên sách  2. Tác giả  3. Số lượng")
    c = chon_menu(["Tên sách", "Tác giả", "Số lượng"])
    tieu_chi = {1: "ten_sach", 2: "tac_gia", 3: "so_luong"}[c]
    print("Thứ tự: 1. Tăng dần  2. Giảm dần")
    giam_dan = chon_menu(["Tăng dần", "Giảm dần"]) == 2
    ket_qua = app.sap_xep_sach(tieu_chi=tieu_chi, giam_dan=giam_dan)
    in_bang_sach(ket_qua, f"Danh sách sách (sắp xếp theo {tieu_chi})")
    input("\nNhấn Enter để tiếp tục...")


def _xem_tat_ca(app) -> None:
    in_tieu_de("DANH SÁCH TẤT CẢ SÁCH")
    tat_ca = app.lay_tat_ca_sach()
    in_bang_sach(tat_ca, "Tất cả sách trong thư viện")
    input("\nNhấn Enter để tiếp tục...")
