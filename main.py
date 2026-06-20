# -*- coding: utf-8 -*-
"""Điểm chạy chính (Entry point) của ứng dụng quản lý thư viện."""

import sys
import os

# Cấu hình mã hóa UTF-8 cho dòng nhập xuất chuẩn để tránh lỗi Unicode trên Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')
if hasattr(sys.stdin, 'reconfigure'):
    sys.stdin.reconfigure(encoding='utf-8')

# Thêm thư mục hiện tại vào sys.path để đảm bảo các import hoạt động trơn tru
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from ui.cli import run_app

if __name__ == "__main__":
    run_app()
