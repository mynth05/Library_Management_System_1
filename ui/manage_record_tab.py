"""Giao diện báo cáo thống kê — tổng quan, top sách, top độc giả."""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ui.widgets import nhap_chuoi, nhap_ngay, nhap_so_nguyen, chon_menu, in_tieu_de


# ─────────────────────────────────────────────────────────────────
#  Màn hình chính — Báo Cáo Thống Kê
# ─────────────────────────────────────────────────────────────────

def man_hinh_bao_cao_thong_ke(app) -> None:
    """Vòng lặp giao diện báo cáo thống kê."""
    MENU = [
        "Tổng quan hệ thống",
        "Top sách được mượn nhiều nhất",
        "Top bạn đọc mượn nhiều nhất",
        "Quay lại",
    ]

    while True:
        in_tieu_de("BÁO CÁO THỐNG KÊ")
        lua_chon = chon_menu(MENU)

        if lua_chon == 1:
            _tong_quan(app)
        elif lua_chon == 2:
            _top_sach(app)
        elif lua_chon == 3:
            _top_ban_doc(app)
        elif lua_chon == 4:
            break


# ─────────────────────────────────────────────────────────────────
#  Chức năng con
# ─────────────────────────────────────────────────────────────────

def _tong_quan(app) -> None:
    in_tieu_de("TỔNG QUAN HỆ THỐNG")
    print(f"   Tổng đầu sách        : {app.tong_dau_sach():>6}")
    print(f"   Tổng bạn đọc         : {app.tong_doc_gia():>6}")
    print(f"   Tổng phiếu mượn      : {app.tong_phieu_muon():>6}")
    print(f"   Phiếu đang mượn      : {app.tong_dang_muon():>6}")
    print(f"   Phiếu quá hạn        : {app.tong_qua_han():>6}")
    print(f"   Tổng phiếu phạt      : {app.tong_phieu_phat():>6}")
    tong = app.tong_tien_phat_chua_thu()
    print(f"   Tiền phạt chưa thu   : {tong:>12,.0f} đ")
    input("\nNhấn Enter để tiếp tục...")


def _top_sach(app) -> None:
    in_tieu_de("TOP SÁCH ĐƯỢC MƯỢN NHIỀU NHẤT")
    n = nhap_so_nguyen("Hiển thị bao nhiêu sách? (mặc định 5): ", min_val=1, default=5)
    top = app.top_sach_duoc_muon_nhieu(n)

    if len(top) == 0:
        print("Chưa có dữ liệu mượn.")
        input("\nNhấn Enter để tiếp tục...")
        return

    print(f"\n  {'#':<4} {'Mã sách':<10} {'Tên sách':<35} {'Lượt mượn':>10}")
    print("  " + "-" * 63)
    for i, (sach, luot) in enumerate(top, 1):
        ten = sach.ten_sach[:33] + ".." if len(sach.ten_sach) > 33 else sach.ten_sach
        print(f"  {i:<4} {sach.ma_sach:<10} {ten:<35} {luot:>10}")
    input("\nNhấn Enter để tiếp tục...")


def _top_ban_doc(app) -> None:
    in_tieu_de("TOP BẠN ĐỌC MƯỢN NHIỀU NHẤT")
    n = nhap_so_nguyen("Hiển thị bao nhiêu bạn đọc? (mặc định 5): ", min_val=1, default=5)
    top = app.top_doc_gia_muon_nhieu(n)

    if len(top) == 0:
        print("Chưa có dữ liệu mượn.")
        input("\nNhấn Enter để tiếp tục...")
        return

    print(f"\n  {'#':<4} {'Mã bạn đọc':<12} {'Họ tên':<30} {'Lượt mượn':>10}")
    print("  " + "-" * 60)
    for i, (doc_gia, luot) in enumerate(top, 1):
        ten = doc_gia.ho_ten[:28] + ".." if len(doc_gia.ho_ten) > 28 else doc_gia.ho_ten
        print(f"  {i:<4} {doc_gia.ma_ban_doc:<12} {ten:<30} {luot:>10}")
    input("\nNhấn Enter để tiếp tục...")

