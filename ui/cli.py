# -*- coding: utf-8 -*-
"""
cli.py — Điểm vào giao diện dòng lệnh (CLI) của hệ thống quản lý thư viện.

Chức năng:
  - Tải dữ liệu khi khởi động
  - Hiển thị menu chính
  - Điều hướng đến các màn hình con
  - Lưu dữ liệu khi thoát
"""

import os
import sys

# Đảm bảo thư mục gốc dự án nằm trong sys.path
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from app_logic import LogicApp
from ui.widgets import chon_menu, in_tieu_de, xoa_man_hinh
from ui.quan_li_sach      import man_hinh_quan_li_sach
from ui.quan_li_ban_doc   import man_hinh_quan_li_ban_doc
from ui.quan_li_muon_tra  import man_hinh_quan_li_muon_tra
from ui.bao_cao_thong_ke  import man_hinh_bao_cao_thong_ke
from ui.quan_li_phat      import man_hinh_quan_li_phat

DATA_DIR = os.path.join(_ROOT, "data")

MENU_CHINH = [
    "Quản lí Sách",
    "Quản lí Bạn Đọc",
    "Quản lí Mượn Trả",
    "Báo Cáo Thống Kê",
    "Quản lí Phạt",
    "Thoát",
]


def _khoi_dong(app: LogicApp) -> None:
    """Tải dữ liệu từ thư mục data/ khi khởi động."""
    os.makedirs(DATA_DIR, exist_ok=True)
    ket_qua = app.tai_du_lieu(DATA_DIR)
    if ket_qua:
        print(f"Đã tải dữ liệu từ '{DATA_DIR}'.")
    else:
        print(f"Không thể tải dữ liệu (có thể chưa có file). Bắt đầu với cơ sở dữ liệu trống.")
    input("Nhấn Enter để vào hệ thống...")


def _luu_va_thoat(app: LogicApp) -> None:
    """Lưu dữ liệu và thoát chương trình."""
    xoa_man_hinh()
    print("Đang lưu dữ liệu...")
    if app.luu_du_lieu(DATA_DIR):
        print(f"✔ Dữ liệu đã được lưu vào '{DATA_DIR}'.")
    else:
        print("✘ Lưu dữ liệu thất bại!")
    print("\nCảm ơn bạn đã sử dụng Hệ thống Quản lý Thư viện. Tạm biệt! 👋")
    sys.exit(0)


def run_app() -> None:
    """Hàm chính: khởi động và chạy vòng lặp menu chính."""
    app = LogicApp()

    xoa_man_hinh()
    print("=" * 60)
    print("   HỆ THỐNG QUẢN LÝ THƯ VIỆN".center(60))
    print("=" * 60)
    _khoi_dong(app)

    while True:
        in_tieu_de("MENU CHÍNH")
        lua_chon = chon_menu(MENU_CHINH)

        if lua_chon == 1:
            man_hinh_quan_li_sach(app)
        elif lua_chon == 2:
            man_hinh_quan_li_ban_doc(app)
        elif lua_chon == 3:
            man_hinh_quan_li_muon_tra(app)
        elif lua_chon == 4:
            man_hinh_bao_cao_thong_ke(app)
        elif lua_chon == 5:
            man_hinh_quan_li_phat(app)
        elif lua_chon == 6:
            _luu_va_thoat(app)


if __name__ == "__main__":
    run_app()
