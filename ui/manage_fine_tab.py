# -*- coding: utf-8 -*-
"""Giao diện quản lí phạt — xem, thanh toán, tìm kiếm phiếu phạt."""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ui.widgets import nhap_chuoi, chon_menu, xac_nhan, in_tieu_de, in_bang_phat


# ─────────────────────────────────────────────────────────────────
#  Màn hình chính — Quản lí Phạt
# ─────────────────────────────────────────────────────────────────

def man_hinh_quan_li_phat(app) -> None:
    """Vòng lặp giao diện quản lí phạt."""
    MENU = [
        "Tìm phiếu phạt theo mã",
        "Thanh toán phiếu phạt",
        "Lọc phiếu phạt",
        "Quay lại",
    ]

    while True:
        in_tieu_de("QUẢN LÍ PHẠT")
        lua_chon = chon_menu(MENU)

        if lua_chon == 1:
            _tim_theo_ma(app)
        elif lua_chon == 2:
            _thanh_toan(app)
        elif lua_chon == 3:
            _loc_phieu_phat(app)
        elif lua_chon == 4:
            break


# ─────────────────────────────────────────────────────────────────
#  Chức năng phụ trợ
# ─────────────────────────────────────────────────────────────────

def _nhap_ma_phat_hop_le(app, prompt: str) -> str:
    """Yêu cầu người dùng nhập đúng mã phiếu phạt mới cho qua."""
    while True:
        ma_phat = nhap_chuoi(prompt)
        if ma_phat.lower() == 'q':
            return None
        phieu = app.tim_phieu_phat(ma_phat)
        if phieu is None:
            print("✘ Không tìm thấy mã phiếu phạt này trong hệ thống. Vui lòng nhập lại (hoặc gõ 'q' để hủy)!")
        else:
            return ma_phat


# ─────────────────────────────────────────────────────────────────
#  Chức năng con
# ─────────────────────────────────────────────────────────────────

def _tim_theo_ma(app) -> None:
    in_tieu_de("TÌM PHIẾU PHẠT THEO MÃ")
    ma_phat = nhap_chuoi("Nhập mã phiếu phạt: ")
    phieu = app.tim_phieu_phat(ma_phat)
    if phieu:
        print(f"\n{phieu}")
    else:
        print("Không tìm thấy phiếu phạt.")
    input("\nNhấn Enter để tiếp tục...")


def _thanh_toan(app) -> None:
    in_tieu_de("THANH TOÁN PHIẾU PHẠT")
    ma_phat = _nhap_ma_phat_hop_le(app, "Mã phiếu phạt: ")
    if not ma_phat:
        return
        
    phieu = app.tim_phieu_phat(ma_phat)
    if phieu.da_thanh_toan:
        print("Phiếu phạt đã được thanh toán trước đó.")
    else:
        print(f"\n{phieu}")
        if xac_nhan(f"\nXác nhận thanh toán {phieu.tong_tien_phat:,.0f} đ? (y/n): "):
            if app.thanh_toan_phat(ma_phat):
                print("Thanh toán thành công!")
                app.luu_du_lieu("data")
            else:
                print("Thanh toán thất bại.")
        else:
            print("Đã hủy.")
    input("\nNhấn Enter để tiếp tục...")


def _loc_phieu_phat(app) -> None:
    in_tieu_de("LỌC PHIẾU PHẠT")
    print("Chọn bộ lọc phiếu phạt:")
    lua_chon = chon_menu([
        "Xem phiếu phạt theo bạn đọc",
        "Xem phiếu phạt chưa thanh toán",
        "Xem tất cả phiếu phạt"
    ])

    if lua_chon == 1:
        ma_ban_doc = nhap_chuoi("Nhập mã bạn đọc: ")
        ds = app.lay_phat_theo_doc_gia(ma_ban_doc)
        in_bang_phat(ds, f"Phiếu phạt của bạn đọc {ma_ban_doc}")
        tong = sum(p.tong_tien_phat for p in ds if not p.da_thanh_toan)
        if tong > 0:
            print(f"\n  💰 Tổng tiền còn nợ: {tong:,.0f} đ")
    elif lua_chon == 2:
        ds = app.lay_phat_chua_thanh_toan()
        in_bang_phat(ds, "Danh sách chưa thanh toán")
        tong = app.tong_tien_phat_chua_thu()
        print(f"\n  💰 Tổng tiền chưa thu: {tong:,.0f} đ")
    elif lua_chon == 3:
        ds = app.lay_tat_ca_phat()
        in_bang_phat(ds, "Tất cả phiếu phạt")
        tong = app.tong_tien_phat_chua_thu()
        print(f"\n  💰 Tổng tiền chưa thu: {tong:,.0f} đ")

    input("\nNhấn Enter để tiếp tục...")

