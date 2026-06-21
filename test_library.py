# -*- coding: utf-8 -*-
"""
Bộ kiểm thử tự động (Unit Tests) cho Hệ thống Quản lý Thư viện.
Chạy test bằng lệnh: python -m unittest test_library.py -v
"""

import unittest
from models import Book, BookCondition, Reader, Gender, TrackStatus
from custom_structures import List, HashTable, PriorityQueue
from app_logic import LogicApp, Validator

class TestCustomStructures(unittest.TestCase):
    """Kiểm thử các cấu trúc dữ liệu tự cài đặt."""

    def test_custom_list(self):
        # Kiểm tra khởi tạo và thêm phần tử
        my_list = List()
        self.assertEqual(len(my_list), 0)
        
        my_list.append(10)
        my_list.append(20)
        self.assertEqual(len(my_list), 2)
        self.assertEqual(my_list.get(0), 10)
        
        # Kiểm tra cập nhật và lấy phần tử
        my_list.set(1, 99)
        self.assertEqual(my_list.get(1), 99)
        
        # Kiểm tra xóa phần tử
        popped = my_list.pop()
        self.assertEqual(popped, 99)
        self.assertEqual(len(my_list), 1)

    def test_hash_table(self):
        ht = HashTable(capacity=8)
        # Kiểm tra thêm và lấy dữ liệu
        ht.put("S001", "Lap trinh Python")
        ht.put("S002", "Cau truc du lieu")
        self.assertTrue(ht.contains("S001"))
        self.assertEqual(ht.get("S002"), "Cau truc du lieu")
        
        # Kiểm tra cập nhật value khi trùng key
        ht.put("S001", "Python Nang Cao")
        self.assertEqual(ht.get("S001"), "Python Nang Cao")
        self.assertEqual(len(ht), 2)
        
        # Kiểm tra xóa dữ liệu
        ht.remove("S001")
        self.assertFalse(ht.contains("S001"))

    def test_priority_queue(self):
        pq = PriorityQueue()
        # Thêm các phần tử với độ ưu tiên (nhỏ nhất là ưu tiên cao nhất - Min Heap)
        pq.push(priority=3, item="Sách C")
        pq.push(priority=1, item="Sách A")
        pq.push(priority=2, item="Sách B")
        
        # Kiểm tra lấy phần tử ưu tiên cao nhất
        self.assertEqual(pq.peek(), "Sách A")
        self.assertEqual(pq.pop(), "Sách A")
        self.assertEqual(pq.pop(), "Sách B")
        self.assertEqual(pq.pop(), "Sách C")
        self.assertTrue(pq.is_empty())


class TestAppLogic(unittest.TestCase):
    """Kiểm thử luồng nghiệp vụ trung tâm (Business Logic)."""

    def setUp(self):
        """Khởi tạo một instance LogicApp mới tinh trước mỗi bài test."""
        self.app = LogicApp()
        
        # Mock data (Dữ liệu giả lập)
        self.sach_mau = Book("B01", "Toán", "Nam", "Giáo trình", "BKHN", 2, BookCondition.NEW)
        self.doc_gia_mau = Reader("R01", "Nguyễn Đăng Hiếu", "2006-10-15", Gender.MALE, "Hà Nội", "0912345678")
        
        self.app.them_sach(self.sach_mau)
        self.app.them_doc_gia(self.doc_gia_mau)

    def test_validator(self):
        # Kiểm tra hàm validate ngày tháng
        self.assertTrue(Validator.is_valid_date("2026-10-15"))
        self.assertFalse(Validator.is_valid_date("15/10/2026")) # Sai định dạng
        self.assertFalse(Validator.is_valid_date("2026-13-45")) # Ngày tháng vô lý

        # Kiểm tra số điện thoại (phải bắt đầu bằng 0, có 10 số)
        self.assertTrue(Validator.is_valid_phone("0912345678"))
        self.assertFalse(Validator.is_valid_phone("912345678")) # Thiếu số 0
        self.assertFalse(Validator.is_valid_phone("09123456789")) # Thừa số

    def test_them_sach_logic(self):
        # Không được thêm sách trùng mã
        sach_trung = Book("B01", "Lý", "Nam", "Giáo trình", "BKHN", 5)
        ket_qua = self.app.them_sach(sach_trung)
        self.assertFalse(ket_qua)
        self.assertEqual(self.app.tim_sach("B01").ten_sach, "Toán") # Dữ liệu cũ không bị đè

    def test_muon_sach_flow(self):
        # Mượn hợp lệ (Kho có 2 cuốn)
        ma_loi_1 = self.app.muon_sach("PM01", "B01", "R01", "2026-06-01", "2026-06-15")
        self.assertEqual(ma_loi_1, 0)
        self.assertEqual(self.app.tim_sach("B01").so_luong, 1) # Kho bị trừ 1 cuốn
        
        # Mượn lần 2 hợp lệ (Kho có 1 cuốn)
        ma_loi_2 = self.app.muon_sach("PM02", "B01", "R01", "2026-06-02", "2026-06-16")
        self.assertEqual(ma_loi_2, 0)
        self.assertEqual(self.app.tim_sach("B01").so_luong, 0) # Kho hết sạch
        
        # Mượn lần 3 bị từ chối do hết sách
        ma_loi_3 = self.app.muon_sach("PM03", "B01", "R01", "2026-06-03", "2026-06-17")
        self.assertEqual(ma_loi_3, 3) # Lỗi số 3: Hết sách

    def test_gioi_han_muon_sach(self):
        # Sét lại kho sách nhiều lên để test giới hạn mượn của bạn đọc
        self.app.cap_nhat_sach("B01", so_luong=10)
        
        # Mượn 5 cuốn (đạt giới hạn MAX_BORROW_PER_READER = 5)
        for i in range(5):
            self.app.muon_sach(f"PM{i}", "B01", "R01", "2026-06-01", "2026-06-15")
            
        # Cuốn thứ 6 phải bị từ chối
        ma_loi = self.app.muon_sach("PM_MAX", "B01", "R01", "2026-06-01", "2026-06-15")
        self.assertEqual(ma_loi, 5) # Lỗi số 5: Bạn đọc đã đạt giới hạn


if __name__ == '__main__':
    unittest.main() 
