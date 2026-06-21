"""
Widgets — các hàm nhập liệu và in ấn dùng chung cho toàn bộ giao diện CLI.
"""

import os
import sys

# Thêm thư mục hiện tại vào sys.path để đảm bảo các import hoạt động trơn tru
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app_logic import Validator


# ─────────────────────────────────────────────────────────────────
#  Tiện ích giao diện
# ─────────────────────────────────────────────────────────────────

def xoa_man_hinh() -> None:
    """Xóa màn hình console (cross-platform)."""
    os.system("cls" if os.name == "nt" else "clear")


def in_tieu_de(tieu_de: str) -> None:
    """In tiêu đề màn hình có đường viền."""
    xoa_man_hinh()
    do_rong = 60
    print("=" * do_rong)
    print(f"  {tieu_de}".center(do_rong))
    print("=" * do_rong)
    print()


def in_phan_cach(ky_tu: str = "-", do_rong: int = 60) -> None:
    """In dòng phân cách."""
    print(ky_tu * do_rong)


# ─────────────────────────────────────────────────────────────────
#  Hàm nhập liệu
# ─────────────────────────────────────────────────────────────────

def nhap_chuoi(prompt: str, cho_phep_trong: bool = False) -> str:
    """Nhập chuỗi không rỗng (trừ khi cho_phep_trong=True)."""
    while True:
        gia_tri = input(prompt).strip()
        if gia_tri or cho_phep_trong:
            return gia_tri
        print("  ✘ Không được để trống. Vui lòng nhập lại.")


def nhap_so_nguyen(prompt: str, min_val: int = 0, max_val: int = None, default: int = None) -> int:
    """Nhập số nguyên trong khoảng [min_val, max_val] (tùy chọn).
    
    Nếu người dùng nhấn Enter và có giá trị default, trả về default.
    """
    while True:
        raw = input(prompt).strip()
        if raw == "" and default is not None:
            return default
        try:
            gia_tri = int(raw)
        except ValueError:
            print("  Vui lòng nhập số nguyên hợp lệ.")
            continue
        if gia_tri < min_val:
            print(f"  Giá trị phải ≥ {min_val}.")
            continue
        if max_val is not None and gia_tri > max_val:
            print(f"  Giá trị phải ≤ {max_val}.")
            continue
        return gia_tri


def nhap_ngay(prompt: str) -> str:
    """Nhập ngày theo định dạng YYYY-MM-DD."""
    while True:
        ngay = input(prompt).strip()
        if Validator.is_valid_date(ngay):
            return ngay
        print("  Ngày không hợp lệ. Định dạng: YYYY-MM-DD (VD: 2026-06-20).")


def chon_menu(danh_sach: list) -> int:
    """Hiển thị menu và trả về chỉ số (1-based) của lựa chọn."""
    for i, muc in enumerate(danh_sach, 1):
        print(f"  {i:>2}. {muc}")
    print()
    return nhap_so_nguyen(f"Nhập lựa chọn (1-{len(danh_sach)}): ",
                          min_val=1, max_val=len(danh_sach))


def xac_nhan(prompt: str) -> bool:
    """Hỏi xác nhận y/n."""
    while True:
        tra_loi = input(prompt).strip().lower()
        if tra_loi in ("y", "yes", "có", "co"):
            return True
        if tra_loi in ("n", "no", "không", "khong"):
            return False
        print("  Vui lòng nhập 'y' (có) hoặc 'n' (không).")


# ─────────────────────────────────────────────────────────────────
#  Hàm in bảng dữ liệu
# ─────────────────────────────────────────────────────────────────

def in_bang_sach(danh_sach, tieu_de: str = "Danh sách sách") -> None:
    """In danh sách sách dưới dạng bảng."""
    print(f"\n  ── {tieu_de} ──")
    if len(danh_sach) == 0:
        print("  (Không có kết quả)")
        return

    header = f"  {'Mã sách':<10} {'Tên sách':<30} {'Tác giả':<20} {'Thể loại':<10} {'NXB':<15} {'SL':>4} {'T.Trạng':<8}"
    print(header)
    print("  " + "-" * (len(header) - 2))
    for sach in danh_sach:
        ten   = sach.ten_sach[:28]  + ".." if len(sach.ten_sach)  > 28 else sach.ten_sach
        tac   = sach.tac_gia[:18]   + ".." if len(sach.tac_gia)   > 18 else sach.tac_gia
        loai  = sach.the_loai[:8]  + ".." if len(sach.the_loai)  > 8 else sach.the_loai
        nxb   = sach.nha_xuat_ban[:13] + ".." if len(sach.nha_xuat_ban) > 13 else sach.nha_xuat_ban
        print(f"  {sach.ma_sach:<10} {ten:<30} {tac:<20} {loai:<10} {nxb:<15} {sach.so_luong:>4} {sach.tinh_trang.value:<8}")
    print(f"\n  Tổng: {len(danh_sach)} sách\n")


def in_bang_ban_doc(danh_sach, tieu_de: str = "Danh sách bạn đọc") -> None:
    """In danh sách bạn đọc dưới dạng bảng."""
    print(f"\n  ── {tieu_de} ──")
    if len(danh_sach) == 0:
        print("  (Không có kết quả)")
        return

    header = f"  {'Mã BD':<10} {'Họ tên':<25} {'Ngày sinh':<12} {'Giới tính':<10} {'Địa chỉ':<20} {'SĐT':<13}"
    print(header)
    print("  " + "-" * (len(header) - 2))
    for r in danh_sach:
        ten  = r.ho_ten[:23]  + ".." if len(r.ho_ten)  > 23 else r.ho_ten
        dc   = r.dia_chi[:18] + ".." if len(r.dia_chi) > 18 else r.dia_chi
        print(f"  {r.ma_ban_doc:<10} {ten:<25} {r.ngay_sinh:<12} {r.gioi_tinh.value:<10} {dc:<20} {r.so_dien_thoai:<13}")
    print(f"\n  Tổng: {len(danh_sach)} bạn đọc\n")


def in_bang_phieu_muon(danh_sach, tieu_de: str = "Danh sách phiếu mượn") -> None:
    """In danh sách phiếu mượn dưới dạng bảng."""
    print(f"\n  ── {tieu_de} ──")
    if len(danh_sach) == 0:
        print("  (Không có kết quả)")
        return

    header = f"  {'Mã phiếu':<12} {'Mã sách':<10} {'Mã BD':<10} {'Ngày mượn':<12} {'Hạn trả':<12} {'Ngày trả':<12} {'T.Thái':<12} {'Gia hạn':>7}"
    print(header)
    print("  " + "-" * (len(header) - 2))
    for t in danh_sach:
        ngay_tra = t.ngay_tra_thuc_te if t.ngay_tra_thuc_te else "Chưa trả"
        print(
            f"  {t.ma_phieu:<12} {t.ma_sach:<10} {t.ma_ban_doc:<10} "
            f"{t.ngay_muon:<12} {t.han_tra:<12} {ngay_tra:<12} "
            f"{t.trang_thai.value:<12} {t.so_lan_gia_han:>7}"
        )
    print(f"\n  Tổng: {len(danh_sach)} phiếu\n")


def in_bang_phat(danh_sach, tieu_de: str = "Danh sách phiếu phạt") -> None:
    """In danh sách phiếu phạt dưới dạng bảng."""
    print(f"\n  ── {tieu_de} ──")
    if len(danh_sach) == 0:
        print("  (Không có kết quả)")
        return

    header = (
        f"  {'Mã phạt':<16} {'Mã phiếu':<14} {'Lý do':<10} "
        f"{'Trễ(ngày)':>10} {'Phạt ngày':>14} {'Phạt sách':>14} "
        f"{'Tổng':>14} {'Trạng thái':<14}"
    )
    print(header)
    print("  " + "-" * (len(header) - 2))
    for f in danh_sach:
        trang_thai = "Đã TT" if f.da_thanh_toan else "Chưa TT"
        print(
            f"  {f.ma_phat:<16} {f.ma_phieu:<14} {f.ly_do.value:<10} "
            f"{f.so_ngay_tre:>10} {f.tien_phat_ngay:>14,.0f} {f.tien_phat_sach:>14,.0f} "
            f"{f.tong_tien_phat:>14,.0f} {trang_thai:<14}"
        )
    print(f"\n  Tổng: {len(danh_sach)} phiếu phạt\n")
