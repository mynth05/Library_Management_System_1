# -*- coding: utf-8 -*-
"""
Bộ kiểm thử tự động (Unit Tests) cho Hệ thống Quản lý Thư viện.
Chạy test bằng lệnh: python -m unittest test_library.py -v
"""

import unittest
import os
import shutil
from models import Book, BookCondition, Reader, Gender, TrackBook, TrackStatus, Fine, FineReason
from custom_structures import List, HashTable
from app_logic import LogicApp, Validator, MAX_BORROW_PER_READER, FINE_PER_DAY, FINE_DAMAGE, FINE_LOST


class TestCustomStructures(unittest.TestCase):
    """Kiểm thử các cấu trúc dữ liệu tự cài đặt (List và HashTable)."""

    def test_custom_list_basic(self):
        """Kiểm tra các thao tác cơ bản trên List tự cài đặt."""
        my_list = List()
        self.assertEqual(len(my_list), 0)
        self.assertTrue(my_list.is_empty())

        # Thêm phần tử
        my_list.append(10)
        my_list.append(20)
        my_list.append(30)
        self.assertEqual(len(my_list), 3)
        self.assertFalse(my_list.is_empty())

        # Lấy phần tử (hỗ trợ cả âm)
        self.assertEqual(my_list.get(0), 10)
        self.assertEqual(my_list.get(1), 20)
        self.assertEqual(my_list.get(-1), 30)
        self.assertEqual(my_list.get(-2), 20)

        # Cập nhật phần tử
        my_list.set(1, 99)
        self.assertEqual(my_list.get(1), 99)
        my_list.set(-1, 88)
        self.assertEqual(my_list.get(-1), 88)

        # Lỗi chỉ mục
        with self.assertRaises(IndexError):
            my_list.get(5)
        with self.assertRaises(IndexError):
            my_list.get(-4)

    def test_custom_list_operations(self):
        """Kiểm tra các thao tác nâng cao của List: extend, insert, pop, contains, copy, slice, add, reversed."""
        my_list = List()
        my_list.extend([1, 2, 3])
        self.assertEqual(len(my_list), 3)
        self.assertEqual(my_list.to_list(), [1, 2, 3])

        # Chèn phần tử
        my_list.insert(1, 99)  # [1, 99, 2, 3]
        self.assertEqual(my_list.to_list(), [1, 99, 2, 3])
        my_list.insert(0, 88)  # [88, 1, 99, 2, 3]
        my_list.insert(len(my_list), 77)  # [88, 1, 99, 2, 3, 77]
        self.assertEqual(my_list.to_list(), [88, 1, 99, 2, 3, 77])

        with self.assertRaises(IndexError):
            my_list.insert(10, 100)

        # Pop phần tử
        self.assertEqual(my_list.pop(), 77)
        self.assertEqual(my_list.pop(2), 99)
        self.assertEqual(my_list.to_list(), [88, 1, 2, 3])

        # Phép toán cộng + và copy
        copied = my_list.copy()
        self.assertEqual(copied.to_list(), my_list.to_list())
        
        added = my_list + [4, 5]
        self.assertEqual(added.to_list(), [88, 1, 2, 3, 4, 5])

        # Membership, Reverse, Eq, Slice
        self.assertTrue(1 in my_list)
        self.assertFalse(99 in my_list)
        
        self.assertEqual(list(reversed(my_list)), [3, 2, 1, 88])
        self.assertEqual(my_list, copied)
        self.assertNotEqual(my_list, added)

        # Slice
        sliced = my_list[1:3]
        self.assertEqual(sliced.to_list(), [1, 2])

        # Kiểm tra __repr__ và __str__
        self.assertTrue("List" in repr(my_list))
        self.assertTrue("List" in str(my_list))

        # Pop từ list rỗng
        empty = List()
        with self.assertRaises(IndexError):
            empty.pop()

    def test_hash_table_basic(self):
        """Kiểm tra các thao tác cơ bản trên HashTable."""
        ht = HashTable(capacity=8)
        self.assertEqual(len(ht), 0)

        # Thêm/Cập nhật cặp key-value
        ht.put("A", 1)
        ht.put("B", 2)
        ht.put("A", 10)  # Cập nhật ghi đè
        self.assertEqual(len(ht), 2)
        self.assertEqual(ht.get("A"), 10)
        self.assertEqual(ht.get("B"), 2)
        self.assertEqual(ht.get("C", default=-1), -1)

        # Contains
        self.assertTrue(ht.contains("A"))
        self.assertFalse(ht.contains("C"))
        self.assertTrue("B" in ht)

        # Xóa
        self.assertTrue(ht.remove("A"))
        self.assertFalse(ht.contains("A"))
        self.assertEqual(len(ht), 1)
        self.assertFalse(ht.remove("A"))  # Xóa lại phải trả về False

        # Các phương thức keys, values, items
        ht.put("C", 3)
        ht.put("D", 4)
        self.assertEqual(set(ht.keys().to_list()), {"B", "C", "D"})
        self.assertEqual(set(ht.values().to_list()), {2, 3, 4})
        self.assertEqual(set(ht.items().to_list()), {("B", 2), ("C", 3), ("D", 4)})

        # Index syntax
        ht["E"] = 5
        self.assertEqual(ht["E"], 5)
        with self.assertRaises(KeyError):
            _ = ht["XYZ"]

        # Iterator
        keys_from_iter = {k for k in ht}
        self.assertEqual(keys_from_iter, {"B", "C", "D", "E"})

    def test_hash_table_resize_and_collisions(self):
        """Kiểm tra HashTable tự động tăng kích thước khi vượt ngưỡng load factor và xử lý xung đột."""
        # Tạo HashTable với kích thước ban đầu siêu nhỏ là 2
        ht = HashTable(capacity=2)
        ht.put("k1", 10)
        self.assertEqual(ht.capacity, 2)
        
        ht.put("k2", 20)
        self.assertEqual(ht.capacity, 2)
        
        ht.put("k3", 30)  # size/capacity = 2/2 = 1.0 >= 0.75 -> resize lên 4
        self.assertEqual(ht.capacity, 4)
        
        ht.put("k4", 40)  # size/capacity = 3/4 = 0.75 >= 0.75 -> resize lên 8
        self.assertEqual(ht.capacity, 8)
        
        self.assertEqual(ht.get("k1"), 10)
        self.assertEqual(ht.get("k2"), 20)
        self.assertEqual(ht.get("k3"), 30)
        self.assertEqual(ht.get("k4"), 40)


class TestAppLogic(unittest.TestCase):
    """Kiểm thử toàn diện logic nghiệp vụ (LogicApp và Validator)."""

    def setUp(self):
        """Khởi tạo LogicApp và chèn dữ liệu mẫu trước mỗi test case."""
        self.app = LogicApp()
        self.sach_1 = Book("B01", "Lap trinh Python", "Tac gia A", "Tin hoc", "NXB Tre", 5, BookCondition.NEW)
        self.sach_2 = Book("B02", "Giai tich 1", "Tac gia B", "Toan hoc", "NXB Giao duc", 1, BookCondition.USED)
        self.doc_gia_1 = Reader("R01", "Nguyen Van A", "2000-01-01", Gender.MALE, "Ha Noi", "0987654321")
        self.doc_gia_2 = Reader("R02", "Tran Thi B", "2001-02-02", Gender.FEMALE, "HCM", "0912345678")

        self.app.them_sach(self.sach_1)
        self.app.them_sach(self.sach_2)
        self.app.them_doc_gia(self.doc_gia_1)
        self.app.them_doc_gia(self.doc_gia_2)

        # Thư mục tạm dùng để test lưu dữ liệu JSON
        self.temp_dir = "./test_data_temp"

    def tearDown(self):
        """Dọn dẹp thư mục tạm sau khi test xong."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_validator(self):
        """Kiểm tra các hàm kiểm định dữ liệu đầu vào (Validator)."""
        # Ngày hợp lệ
        self.assertTrue(Validator.is_valid_date("2026-06-20"))
        self.assertTrue(Validator.is_valid_date("2024-02-29"))  # Năm nhuận
        # Ngày không hợp lệ
        self.assertFalse(Validator.is_valid_date("2023-02-29"))  # Không phải năm nhuận
        self.assertFalse(Validator.is_valid_date("2026-06-31"))  # Tháng 6 chỉ có 30 ngày
        self.assertFalse(Validator.is_valid_date("2026-13-10"))  # Tháng 13 không tồn tại
        self.assertFalse(Validator.is_valid_date("26-06-2026"))  # Sai định dạng
        self.assertFalse(Validator.is_valid_date("invalid-date"))

        # ID hợp lệ (chữ, số, gạch ngang, gạch dưới)
        self.assertTrue(Validator.is_valid_id("valid_id-123"))
        self.assertFalse(Validator.is_valid_id("invalid id"))  # Chứa dấu cách
        self.assertFalse(Validator.is_valid_id(""))  # Rỗng

        # Số điện thoại hợp lệ (10 số bắt đầu bằng 0)
        self.assertTrue(Validator.is_valid_phone("0987654321"))
        self.assertFalse(Validator.is_valid_phone("987654321"))  # Thiếu số 0 đầu
        self.assertFalse(Validator.is_valid_phone("098765432"))   # 9 số
        self.assertFalse(Validator.is_valid_phone("09876543210"))  # 11 số
        self.assertFalse(Validator.is_valid_phone("abc7654321"))   # Chứa chữ

        # Số nguyên không âm
        self.assertTrue(Validator.is_positive_int(0))
        self.assertTrue(Validator.is_positive_int(10))
        self.assertFalse(Validator.is_positive_int(-5))
        self.assertFalse(Validator.is_positive_int("10"))

    def test_crud_sach(self):
        """Kiểm tra các nghiệp vụ thêm, sửa, xóa, tìm kiếm, sắp xếp và lọc sách."""
        # Thêm sách mới hợp lệ
        sach_moi = Book("B03", "Vat ly dai cuong", "Tac gia C", "Vat ly", "NXB GD", 3, BookCondition.NEW)
        self.assertTrue(self.app.them_sach(sach_moi))
        self.assertEqual(self.app.tong_dau_sach(), 3)

        # Thêm sách mã trùng
        self.assertFalse(self.app.them_sach(sach_moi))

        # Thêm sách mã không hợp lệ
        sach_loi_id = Book("B 04", "Title", "Author", "Genre", "Publisher", 2)
        self.assertFalse(self.app.them_sach(sach_loi_id))

        # Thêm sách số lượng âm
        sach_loi_sl = Book("B04", "Title", "Author", "Genre", "Publisher", -1)
        self.assertFalse(self.app.them_sach(sach_loi_sl))

        # Tìm sách
        self.assertEqual(self.app.tim_sach("B01").ten_sach, "Lap trinh Python")
        self.assertIsNone(self.app.tim_sach("B99"))

        # Cập nhật sách
        self.assertTrue(self.app.cap_nhat_sach("B01", ten_sach="Python Nang Cao", so_luong=10))
        self.assertEqual(self.app.tim_sach("B01").ten_sach, "Python Nang Cao")
        self.assertEqual(self.app.tim_sach("B01").so_luong, 10)

        with self.assertRaises(KeyError):
            self.app.cap_nhat_sach("B99", ten_sach="No Name")
        with self.assertRaises(ValueError):
            self.app.cap_nhat_sach("B01", truong_la="Error")
        with self.assertRaises(ValueError):
            self.app.cap_nhat_sach("B01", so_luong=-2)
        with self.assertRaises(ValueError):
            self.app.cap_nhat_sach("B01", tinh_trang="NEW")  # phải là Enum BookCondition

        # Lọc sách
        sach_loc = self.app.loc_sach(the_loai="Toan hoc")
        self.assertEqual(len(sach_loc), 1)
        self.assertEqual(sach_loc.get(0).ma_sach, "B02")

        # Tìm sách theo tên/thể loại
        self.assertEqual(len(self.app.tim_sach_theo_ten("Python")), 1)
        self.assertEqual(len(self.app.tim_sach_theo_the_loai("Tin")), 1)

        # Sắp xếp sách
        self.app.them_sach(Book("B04", "A b c", "Author", "Genre", "Publisher", 7))
        sorted_books = self.app.sap_xep_sach(tieu_chi="ten_sach")
        self.assertEqual(sorted_books.get(0).ten_sach, "A b c")  # "A b c" đứng đầu theo bảng chữ cái

        # Xóa sách
        self.assertTrue(self.app.xoa_sach("B02"))
        self.assertIsNone(self.app.tim_sach("B02"))
        self.assertFalse(self.app.xoa_sach("B02"))  # Xóa lại phải trả về False

    def test_crud_doc_gia(self):
        """Kiểm tra thêm, sửa, xóa, tìm kiếm, lọc bạn đọc."""
        # Thêm bạn đọc mới
        ban_doc_moi = Reader("R03", "Le Van C", "1999-09-09", Gender.OTHER, "Da Nang", "0909090909")
        self.assertTrue(self.app.them_doc_gia(ban_doc_moi))
        self.assertEqual(self.app.tong_doc_gia(), 3)

        # Mã trùng
        self.assertFalse(self.app.them_doc_gia(ban_doc_moi))

        # Mã không hợp lệ
        doc_gia_loi_id = Reader("R 04", "Name", "1999-09-09", Gender.MALE, "Add", "0987654321")
        self.assertFalse(self.app.them_doc_gia(doc_gia_loi_id))

        # Tìm bạn đọc
        self.assertEqual(self.app.tim_doc_gia("R01").ho_ten, "Nguyen Van A")

        # Cập nhật bạn đọc
        self.assertTrue(self.app.cap_nhat_doc_gia("R01", ho_ten="Nguyen Van A New", gioi_tinh=Gender.FEMALE))
        self.assertEqual(self.app.tim_doc_gia("R01").ho_ten, "Nguyen Van A New")
        self.assertEqual(self.app.tim_doc_gia("R01").gioi_tinh, Gender.FEMALE)

        with self.assertRaises(KeyError):
            self.app.cap_nhat_doc_gia("R99", ho_ten="Error")
        with self.assertRaises(ValueError):
            self.app.cap_nhat_doc_gia("R01", gioi_tinh="FEMALE")  # Phải là Enum Gender
        with self.assertRaises(ValueError):
            self.app.cap_nhat_doc_gia("R01", so_dien_thoai="invalid")
        with self.assertRaises(ValueError):
            self.app.cap_nhat_doc_gia("R01", ngay_sinh="2026-15-15")

        # Tìm theo tên
        self.assertEqual(len(self.app.tim_doc_gia_theo_ten("Tran Thi")), 1)

        # Lọc bạn đọc
        female_readers = self.app.loc_doc_gia(gioi_tinh=Gender.FEMALE)
        self.assertEqual(len(female_readers), 2)  # R02 gốc và R01 mới được sửa thành FEMALE

        # Xóa bạn đọc
        self.assertTrue(self.app.xoa_doc_gia("R02"))
        self.assertIsNone(self.app.tim_doc_gia("R02"))

    def test_muon_tra_sach_va_phieu_phat(self):
        """Kiểm tra toàn bộ luồng mượn sách, trả sách và tạo các phiếu phạt quá hạn tương ứng."""
        # 1. Mượn sách
        # Mượn hợp lệ (sách B01 còn 5 cuốn)
        ma_loi = self.app.muon_sach("PM01", "B01", "R01", "2026-06-01", "2026-06-15")
        self.assertEqual(ma_loi, 0)
        self.assertEqual(self.app.tim_sach("B01").so_luong, 4)  # Đã giảm 1 cuốn

        # Trùng mã phiếu mượn
        self.assertEqual(self.app.muon_sach("PM01", "B01", "R02", "2026-06-01", "2026-06-15"), 1)
        # Sách không tồn tại
        self.assertEqual(self.app.muon_sach("PM02", "B99", "R01", "2026-06-01", "2026-06-15"), 2)
        # Độc giả không tồn tại
        self.assertEqual(self.app.muon_sach("PM02", "B01", "R99", "2026-06-01", "2026-06-15"), 4)
        # Ngày tháng sai định dạng
        self.assertEqual(self.app.muon_sach("PM02", "B01", "R01", "2026-06-01", "2026-06-00"), 6)
        # Ngày hạn trả trước ngày mượn
        self.assertEqual(self.app.muon_sach("PM02", "B01", "R01", "2026-06-15", "2026-06-01"), 7)

        # Mượn hết sách
        # B02 chỉ có 1 cuốn
        self.assertEqual(self.app.muon_sach("PM02", "B02", "R01", "2026-06-01", "2026-06-15"), 0)
        # Người sau mượn B02 sẽ báo hết sách
        self.assertEqual(self.app.muon_sach("PM03", "B02", "R02", "2026-06-01", "2026-06-15"), 3)

        # Mượn vượt quá giới hạn mượn
        # Chỉnh kho sách lên nhiều cuốn để mượn tiếp
        self.app.cap_nhat_sach("B01", so_luong=10)
        # Độc giả R01 đã mượn 2 cuốn (PM01, PM02). Mượn thêm 3 cuốn nữa để đạt giới hạn 5 cuốn.
        self.assertEqual(self.app.muon_sach("PM03", "B01", "R01", "2026-06-01", "2026-06-15"), 0)
        self.assertEqual(self.app.muon_sach("PM04", "B01", "R01", "2026-06-01", "2026-06-15"), 0)
        self.assertEqual(self.app.muon_sach("PM05", "B01", "R01", "2026-06-01", "2026-06-15"), 0)
        # Cuốn thứ 6 phải trả về lỗi vượt giới hạn (code 5)
        self.assertEqual(self.app.muon_sach("PM06", "B01", "R01", "2026-06-01", "2026-06-15"), 5)

        # 2. Trả sách
        # Trả sách đúng hạn (Ngày trả 2026-06-10 <= Hạn trả 2026-06-15)
        self.assertEqual(self.app.tra_sach("PM01", "2026-06-10"), 0)
        self.assertEqual(self.app.tim_sach("B01").so_luong, 8)  # Trả về kho -> tăng 1
        
        # Trả lại phiếu đã trả trước đó
        self.assertEqual(self.app.tra_sach("PM01", "2026-06-10"), 2)
        # Trả phiếu không tồn tại
        self.assertEqual(self.app.tra_sach("PM99", "2026-06-10"), 1)
        # Ngày trả không hợp lệ
        self.assertEqual(self.app.tra_sach("PM02", "invalid-date"), 3)

        # Trả sách trễ hạn (Hạn trả 2026-06-15, Ngày trả thực tế 2026-06-20 -> trễ 5 ngày)
        self.assertEqual(self.app.tra_sach("PM02", "2026-06-20"), 0)
        # Kiểm tra tự động tạo phiếu phạt trễ hạn
        fine = self.app.tim_phieu_phat("FINE_PM02")
        self.assertIsNotNone(fine)
        self.assertEqual(fine.so_ngay_tre, 5)
        self.assertEqual(fine.tien_phat_ngay, 5 * FINE_PER_DAY)
        self.assertEqual(fine.ly_do, FineReason.OVERDUE)
        self.assertFalse(fine.da_thanh_toan)

        # Thanh toán phạt
        self.assertTrue(self.app.thanh_toan_phat("FINE_PM02"))
        self.assertTrue(self.app.tim_phieu_phat("FINE_PM02").da_thanh_toan)
        self.assertFalse(self.app.thanh_toan_phat("FINE_PM02"))  # Thanh toán lại báo False

        # Các thống kê liên quan đến phiếu mượn
        self.assertEqual(len(self.app.lay_phieu_muon_theo_doc_gia("R01")), 5)
        self.assertEqual(len(self.app.lay_tat_ca_phieu_muon()), 5)
        self.assertEqual(len(self.app.lay_tat_ca_phat()), 1)

    def test_gia_han_muon(self):
        """Kiểm tra logic gia hạn thời gian mượn sách."""
        self.app.muon_sach("PM_GH", "B01", "R01", "2026-06-01", "2026-06-15")

        # Gia hạn hợp lệ
        self.assertEqual(self.app.gia_han_muon("PM_GH", "2026-06-25"), 0)
        self.assertEqual(self.app.tim_phieu_muon("PM_GH").han_tra, "2026-06-25")
        self.assertEqual(self.app.tim_phieu_muon("PM_GH").so_lan_gia_han, 1)

        # Ngày hạn mới trước/bằng ngày hạn cũ
        self.assertEqual(self.app.gia_han_muon("PM_GH", "2026-06-20"), 4)

        # Gia hạn thêm 2 lần nữa (tổng cộng 3 lần - đạt tối đa)
        self.assertEqual(self.app.gia_han_muon("PM_GH", "2026-07-05"), 0)
        self.assertEqual(self.app.gia_han_muon("PM_GH", "2026-07-15"), 0)
        
        # Gia hạn lần thứ 4 bị từ chối
        self.assertEqual(self.app.gia_han_muon("PM_GH", "2026-07-25"), 3)

        # Trả sách rồi thì không được gia hạn
        self.app.tra_sach("PM_GH", "2026-06-10")
        self.assertEqual(self.app.gia_han_muon("PM_GH", "2026-07-30"), 2)

        # Phiếu không tồn tại
        self.assertEqual(self.app.gia_han_muon("PM99", "2026-07-30"), 1)
        # Ngày nhập vào lỗi
        self.assertEqual(self.app.gia_han_muon("PM_GH", "invalid-date"), 5)

    def test_bao_mat_sach(self):
        """Kiểm tra chức năng báo mất sách."""
        self.app.muon_sach("PM_MAT", "B01", "R01", "2026-06-01", "2026-06-15")
        
        # Báo mất hợp lệ đúng hạn (Trễ 0 ngày, phạt tiền sách mất)
        self.assertEqual(self.app.bao_mat_sach("PM_MAT", "2026-06-10"), 0)
        
        fine = self.app.tim_phieu_phat("LOST_PM_MAT")
        self.assertIsNotNone(fine)
        self.assertEqual(fine.so_ngay_tre, 0)
        self.assertEqual(fine.tien_phat_sach, FINE_LOST)
        self.assertEqual(fine.tong_tien_phat, FINE_LOST)
        self.assertEqual(fine.ly_do, FineReason.LOST)
        
        # Số lượng sách B01 không được trả về (vì bị mất)
        self.assertEqual(self.app.tim_sach("B01").so_luong, 4)  # lúc đầu 5, mượn 1 còn 4, không tăng lại

    def test_bao_hu_sach(self):
        """Kiểm tra chức năng báo hư hỏng sách."""
        self.app.muon_sach("PM_HU", "B01", "R01", "2026-06-01", "2026-06-15")

        # Báo hư hợp lệ trễ 2 ngày (hạn 15, báo 17 -> trễ 2 ngày + phạt hư hỏng)
        self.assertEqual(self.app.bao_hu_sach("PM_HU", "2026-06-17"), 0)

        fine = self.app.tim_phieu_phat("DMG_PM_HU")
        self.assertIsNotNone(fine)
        self.assertEqual(fine.so_ngay_tre, 2)
        self.assertEqual(fine.tien_phat_ngay, 2 * FINE_PER_DAY)
        self.assertEqual(fine.tien_phat_sach, FINE_DAMAGE)
        self.assertEqual(fine.tong_tien_phat, 2 * FINE_PER_DAY + FINE_DAMAGE)
        self.assertEqual(fine.ly_do, FineReason.DAMAGED)

        # Số lượng sách được hoàn trả về kho (vì sách hỏng vẫn thu hồi) và tình trạng sách đổi thành USED
        self.assertEqual(self.app.tim_sach("B01").so_luong, 5)
        self.assertEqual(self.app.tim_sach("B01").tinh_trang, BookCondition.USED)

    def test_loc_va_cap_nhat_trang_thai_phieu_muon(self):
        """Kiểm tra lọc danh sách phiếu mượn theo trạng thái và cập nhật trạng thái tự động."""
        self.app.muon_sach("PM_DH", "B01", "R01", "2026-06-01", "2026-06-30")  # đang trong hạn
        self.app.muon_sach("PM_QH", "B01", "R02", "2026-06-01", "2026-06-10")  # đã quá hạn

        # Cập nhật trạng thái phiếu theo ngày 2026-06-20
        self.app.cap_nhat_trang_thai_phieu("2026-06-20")

        self.assertEqual(self.app.tim_phieu_muon("PM_DH").trang_thai, TrackStatus.BORROWING)
        self.assertEqual(self.app.tim_phieu_muon("PM_QH").trang_thai, TrackStatus.OVERDUE)

        # Lọc danh sách quá hạn
        qua_han_list = self.app.lay_phieu_qua_han()
        self.assertEqual(len(qua_han_list), 1)
        self.assertEqual(qua_han_list.get(0).ma_phieu, "PM_QH")

    def test_thong_ke_nang_cao(self):
        """Kiểm tra các báo cáo thống kê nâng cao (Top sách, top độc giả)."""
        self.app.muon_sach("PM01", "B01", "R01", "2026-06-01", "2026-06-15")
        self.app.muon_sach("PM02", "B02", "R01", "2026-06-01", "2026-06-15")
        self.app.muon_sach("PM03", "B01", "R02", "2026-06-02", "2026-06-15")

        # Thống kê tổng số
        self.assertEqual(self.app.tong_dau_sach(), 2)
        self.assertEqual(self.app.tong_doc_gia(), 2)
        self.assertEqual(self.app.tong_phieu_muon(), 3)
        self.assertEqual(self.app.tong_dang_muon(), 3)

        # Top sách được mượn nhiều nhất (B01 mượn 2 lần, B02 mượn 1 lần)
        top_sach = self.app.top_sach_duoc_muon_nhieu(1)
        self.assertEqual(len(top_sach), 1)
        book, count = top_sach.get(0)
        self.assertEqual(book.ma_sach, "B01")
        self.assertEqual(count, 2)

        # Top bạn đọc mượn nhiều nhất (R01 mượn 2 lần, R02 mượn 1 lần)
        top_doc_gia = self.app.top_doc_gia_muon_nhieu(1)
        self.assertEqual(len(top_doc_gia), 1)
        reader, count = top_doc_gia.get(0)
        self.assertEqual(reader.ma_ban_doc, "R01")
        self.assertEqual(count, 2)

    def test_luu_va_tai_du_lieu_json(self):
        """Kiểm tra lưu dữ liệu ra file JSON và tải lại dữ liệu."""
        # Thực hiện các thay đổi dữ liệu và lưu
        self.app.muon_sach("PM01", "B01", "R01", "2026-06-01", "2026-06-15")
        self.app.tra_sach("PM01", "2026-06-20")  # Tạo phạt trễ hạn

        self.assertTrue(self.app.luu_du_lieu(self.temp_dir))

        # Kiểm tra file được tạo ra
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "books.json")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "readers.json")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "tracks.json")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "fines.json")))

        # Khởi tạo một app mới và tải lại dữ liệu
        new_app = LogicApp()
        self.assertTrue(new_app.tai_du_lieu(self.temp_dir))

        # Xác minh dữ liệu tải lại trùng khớp
        self.assertEqual(new_app.tong_dau_sach(), 2)
        self.assertEqual(new_app.tong_doc_gia(), 2)
        self.assertEqual(new_app.tong_phieu_muon(), 1)
        self.assertEqual(new_app.tong_phieu_phat(), 1)
        
        self.assertEqual(new_app.tim_sach("B01").ten_sach, "Lap trinh Python")
        self.assertEqual(new_app.tim_doc_gia("R01").ho_ten, "Nguyen Van A")
        self.assertEqual(new_app.tim_phieu_muon("PM01").trang_thai, TrackStatus.RETURNED)
        self.assertEqual(new_app.tim_phieu_phat("FINE_PM01").so_ngay_tre, 5)


if __name__ == '__main__':
    unittest.main()
