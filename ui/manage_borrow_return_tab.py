# -*- coding: utf-8 -*-
"""Giao diện quản lí mượn – trả sách: tạo phiếu, gia hạn, trả, báo mất/hư."""

import sys, os
import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models import TrackStatus
from custom_structures import List
from ui.widgets import (
    nhap_chuoi, nhap_ngay, chon_menu,
    in_tieu_de, in_bang_phieu_muon,
)

# Bản đồ mã lỗi → thông báo
_MUON_MSG = {
    0: "Tạo phiếu mượn thành công.",
    1: "Mã phiếu không hợp lệ hoặc đã tồn tại.",
    2: "Không tìm thấy sách.",
    3: "Hết sách (số lượng = 0).",
    4: "Không tìm thấy bạn đọc.",
    5: "Bạn đọc đã đạt giới hạn số sách mượn đồng thời.",
    6: "Định dạng ngày không hợp lệ (cần YYYY-MM-DD).",
    7: "Hạn trả phải sau ngày mượn.",
}
_TRA_MSG = {
    0: "Trả sách thành công.",
    1: "Không tìm thấy phiếu mượn.",
    2: "Sách đã được trả trước đó.",
    3: "Ngày trả không hợp lệ.",
}
_GIA_HAN_MSG = {
    0: "Gia hạn thành công.",
    1: "Không tìm thấy phiếu.",
    2: "Phiếu đã trả.",
    3: "Đã đạt số lần gia hạn tối đa (3 lần).",
    4: "Hạn trả mới phải sau hạn trả hiện tại.",
    5: "Ngày không hợp lệ.",
}
_BAO_MSG = {
    0: "Báo cáo thành công, phiếu phạt đã được tạo.",
    1: "Không tìm thấy phiếu.",
    2: "Phiếu đã trả.",
    3: "Ngày không hợp lệ.",
    4: "Phiếu phạt cho phiếu này đã tồn tại.",
}


# ─────────────────────────────────────────────────────────────────
#  Màn hình chính — Quản lí Mượn Trả
# ─────────────────────────────────────────────────────────────────

def man_hinh_quan_li_muon_tra(app) -> None:
    """Vòng lặp giao diện quản lí mượn trả."""
    MENU = List()
    MENU.extend([
        "Tạo phiếu mượn",
        "Trả sách",
        "Gia hạn mượn sách",
        "Báo mất sách",
        "Báo hư hỏng sách",
        "Tìm kiếm phiếu mượn",
        "Lọc danh sách phiếu mượn",
        "Quay lại",
    ])

    while True:
        in_tieu_de("QUẢN LÍ MƯỢN TRẢ")
        lua_chon = chon_menu(MENU)

        if lua_chon == 1:
            _tao_phieu_muon(app)
        elif lua_chon == 2:
            _tra_sach(app)
        elif lua_chon == 3:
            _gia_han(app)
        elif lua_chon == 4:
            _bao_mat(app)
        elif lua_chon == 5:
            _bao_hu(app)
        elif lua_chon == 6:
            _tim_kiem_phieu(app)
        elif lua_chon == 7:
            _loc_phieu_muon(app)
        elif lua_chon == 8:
            break


# ─────────────────────────────────────────────────────────────────
#  Chức năng phụ trợ tự động sinh
# ─────────────────────────────────────────────────────────────────

def _sinh_ma_phieu(app) -> str:
    """Tự sinh mã phiếu kế tiếp có dạng PH1, PH2, PH3..."""
    max_num = 0
    for t in app.lay_tat_ca_phieu_muon():
        if t.ma_phieu.startswith("PH"):
            try:
                num = int(t.ma_phieu[2:])
                if num > max_num:
                    max_num = num
            except ValueError:
                pass
    return f"PH{max_num + 1}"


def _tinh_han_tra(ngay_muon_str: str) -> str:
    """Cộng thêm 90 ngày so với ngày mượn."""
    dt = datetime.datetime.strptime(ngay_muon_str, "%Y-%m-%d")
    dt_new = dt + datetime.timedelta(days=90)
    return dt_new.strftime("%Y-%m-%d")


def _nhap_ma_phieu_hop_le(app, prompt: str) -> str:
    """Yêu cầu người dùng nhập mã phiếu đúng thực tế mới cho qua."""
    while True:
        ma_phieu = nhap_chuoi(prompt)
        if ma_phieu.lower() == 'q':
            return None
        phieu = app.tim_phieu_muon(ma_phieu)
        if phieu is None:
            print("Không tìm thấy mã phiếu mượn này trong hệ thống. Vui lòng nhập lại (hoặc gõ 'q' để hủy)!")
        else:
            return ma_phieu


# ─────────────────────────────────────────────────────────────────
#  Chức năng con
# ─────────────────────────────────────────────────────────────────

def _tao_phieu_muon(app) -> None:
    in_tieu_de("TẠO PHIẾU MƯỢN")

    while True:
        ma_phieu = nhap_chuoi("Mã phiếu mượn: ")
        if app.tim_phieu_muon(ma_phieu) is None:
            break
        print("Mã phiếu đã tồn tại. Vui lòng nhập mã khác.")

    while True:
        ma_sach = nhap_chuoi("Mã sách: ")
        if app.tim_sach(ma_sach) is not None:
            break
        print("Mã sách không tồn tại. Vui lòng nhập lại.")

    while True:
        ma_ban_doc = nhap_chuoi("Mã bạn đọc: ")
        if app.tim_doc_gia(ma_ban_doc) is None:
            print("Mã bạn đọc không tồn tại. Vui lòng nhập lại.")
            continue
        # Kiểm tra bạn đọc có đang mượn cuốn này không
        dang_muon = any(
            t.ma_sach == ma_sach and t.trang_thai != TrackStatus.RETURNED
            for t in app.lay_phieu_muon_theo_doc_gia(ma_ban_doc)
        )
        if dang_muon:
            print("Bạn đọc đang mượn cuốn sách này. Vui lòng nhập mã bạn đọc khác.")
            continue
        break

    ngay_muon = nhap_ngay("Ngày mượn (YYYY-MM-DD): ")
    han_tra   = _tinh_han_tra(ngay_muon)
    print(f"Hạn trả (tự động cộng 90 ngày): {han_tra}")

    ma = app.muon_sach(ma_phieu, ma_sach, ma_ban_doc, ngay_muon, han_tra)
    print(f"\n{_MUON_MSG.get(ma, 'Lỗi không xác định.')}")
    if ma == 0:
        app.luu_du_lieu("data")
    input("\nNhấn Enter để tiếp tục...")


def _tra_sach(app) -> None:
    in_tieu_de("TRẢ SÁCH")
    ma_phieu = _nhap_ma_phieu_hop_le(app, "Mã phiếu mượn: ")
    if not ma_phieu:
        return

    phieu = app.tim_phieu_muon(ma_phieu)
    while True:
        ngay_tra = nhap_ngay("Ngày trả (YYYY-MM-DD): ")
        if ngay_tra >= phieu.ngay_muon:
            break
        print(f"Ngày trả phải sau ngày mượn ({phieu.ngay_muon}). Vui lòng nhập lại.")

    ma = app.tra_sach(ma_phieu, ngay_tra)
    print(f"\n{_TRA_MSG.get(ma, 'Lỗi không xác định.')}")
    if ma == 0:
        app.luu_du_lieu("data")
        ma_phat = f"FINE_{ma_phieu}"
        phieu_phat = app.tim_phieu_phat(ma_phat)
        if phieu_phat:
            print(f"  Phiếu phạt: {phieu_phat}")
    input("\nNhấn Enter để tiếp tục...")


def _gia_han(app) -> None:
    in_tieu_de("GIA HẠN MƯỢN SÁCH")
    ma_phieu = _nhap_ma_phieu_hop_le(app, "Mã phiếu mượn: ")
    if not ma_phieu:
        return
        
    han_tra_moi = nhap_ngay("Hạn trả mới (YYYY-MM-DD): ")

    ma = app.gia_han_muon(ma_phieu, han_tra_moi)
    print(f"\n{_GIA_HAN_MSG.get(ma, 'Lỗi không xác định.')}")
    if ma == 0:
        app.luu_du_lieu("data")
    if ma == 0:
        phieu = app.tim_phieu_muon(ma_phieu)
        if phieu:
            print(f"  Số lần gia hạn còn lại: {3 - phieu.so_lan_gia_han}")
    input("\nNhấn Enter để tiếp tục...")


def _bao_mat(app) -> None:
    in_tieu_de("BÁO MẤT SÁCH")
    ma_phieu = _nhap_ma_phieu_hop_le(app, "Mã phiếu mượn: ")
    if not ma_phieu:
        return
        
    ngay_bao = nhap_ngay("Ngày báo mất (YYYY-MM-DD): ")

    ma = app.bao_mat_sach(ma_phieu, ngay_bao)
    print(f"\n{_BAO_MSG.get(ma, 'Lỗi không xác định.')}")
    if ma == 0:
        app.luu_du_lieu("data")
    input("\nNhấn Enter để tiếp tục...")


def _bao_hu(app) -> None:
    in_tieu_de("BÁO HƯ HỎNG SÁCH")
    ma_phieu = _nhap_ma_phieu_hop_le(app, "Mã phiếu mượn: ")
    if not ma_phieu:
        return
        
    ngay_bao = nhap_ngay("Ngày báo hư (YYYY-MM-DD): ")

    ma = app.bao_hu_sach(ma_phieu, ngay_bao)
    print(f"\n{_BAO_MSG.get(ma, 'Lỗi không xác định.')}")
    if ma == 0:
        app.luu_du_lieu("data")
    input("\nNhấn Enter để tiếp tục...")


def _tim_kiem_phieu(app) -> None:
    in_tieu_de("TÌM KIẾM PHIẾU MƯỢN")
    menu_tim = List()
    menu_tim.extend(["Tìm theo mã phiếu", "Tìm theo mã bạn đọc"])
    lua_chon = chon_menu(menu_tim)

    if lua_chon == 1:
        ma_phieu = nhap_chuoi("Nhập mã phiếu mượn: ")
        phieu = app.tim_phieu_muon(ma_phieu)
        if phieu:
            print(f"\n{phieu}")
        else:
            print("Không tìm thấy phiếu.")
    elif lua_chon == 2:
        ma_ban_doc = nhap_chuoi("Nhập mã bạn đọc: ")
        ds = app.lay_phieu_muon_theo_doc_gia(ma_ban_doc)
        in_bang_phieu_muon(ds, f"Phiếu mượn của bạn đọc {ma_ban_doc}")

    input("\nNhấn Enter để tiếp tục...")


def _loc_phieu_muon(app) -> None:
    in_tieu_de("LỌC PHIẾU MƯỢN")
    menu_loc = List()
    menu_loc.extend(["Phiếu đang mượn", "Phiếu quá hạn", "Tất cả phiếu mượn"])
    lua_chon = chon_menu(menu_loc)

    if lua_chon == 1:
        ds = app.lay_phieu_theo_trang_thai(TrackStatus.BORROWING)
        in_bang_phieu_muon(ds, "Danh sách phiếu đang mượn")
    elif lua_chon == 2:
        ds = app.lay_phieu_qua_han()
        in_bang_phieu_muon(ds, "Danh sách phiếu quá hạn")
    elif lua_chon == 3:
        ds = app.lay_tat_ca_phieu_muon()
        in_bang_phieu_muon(ds, "Tất cả phiếu mượn")

    input("\nNhấn Enter để tiếp tục...")

