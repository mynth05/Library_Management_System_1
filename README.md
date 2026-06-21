# HỆ THỐNG QUẢN LÝ THƯ VIỆN

Bài tập Lớn môn Kỹ thuật Lập trình - Đại học Bách Khoa Hà Nội.

169314 - MI3310

## 1. Thông tin nhóm sinh viên

* Phạm Thị Minh Thuý - 202418992
* Nguyễn Đăng Hiếu - 202418900

## 2. Cấu trúc mã nguồn

* `main.py`: Điểm khởi đầu của chương trình, thiết lập môi trường mã hóa UTF-8 cho dòng lệnh, điều phối vòng lặp và gọi hàm khởi chạy hệ thống.
* `app_logic.py`: Chứa logic chính của hệ thống: kiểm tra dữ liệu đầu vào (Validator), xử lý CRUD, mượn/trả sách, tự động tính phạt, thống kê, xếp hạng và lưu trữ file JSON.
* `models.py`: Định nghĩa các lớp dữ liệu nền tảng như `Book`, `Reader`, `TrackBook`, `Fine` cùng các `Enum` trạng thái tương ứng.
* `custom_structures.py`: Chứa các cấu trúc dữ liệu và giải thuật tự cài đặt, gồm `HashTable` (xử lý va chạm Separate Chaining) và `List` (mảng động).
* `ui/`: Chia nhỏ giao diện Console thành các module độc lập, gồm quản lý sách, quản lý bạn đọc, mượn trả, quản lý phạt, thống kê và widget nhập liệu dùng chung.
* `test_library.py`: Bộ kiểm thử tự động toàn diện (Unit Tests) với gần 60 kịch bản bao phủ các cấu trúc dữ liệu và logic hệ thống.
* `data/`: Chứa dữ liệu của hệ thống dưới định dạng JSON (`books.json`, `readers.json`, `tracks.json`, `fines.json`).

## 3. Mô tả tổng quan

Chương trình mô phỏng hệ thống quản lý thư viện vận hành hoàn toàn trên giao diện dòng lệnh (CLI). Điểm đặc biệt của dự án là **không phụ thuộc vào các cấu trúc dữ liệu mặc định của Python** (như `list` hay `dict`), mà sử dụng 100% cấu trúc dữ liệu tự thiết kế nhằm đáp ứng yêu cầu thuật toán chuyên sâu của môn học.

Các chức năng chính:

* **Quản lý dữ liệu Sách & Bạn đọc**: Đọc/ghi dữ liệu, thêm, sửa, xóa. Hỗ trợ tra cứu nhanh qua `HashTable`.
* **Xử lý Mượn/Trả sách**: Ràng buộc logic chặt chẽ (kiểm tra tồn kho, kiểm tra giới hạn 5 cuốn/người). Hỗ trợ gia hạn sách (tối đa 3 lần).
* **Quản lý Vi phạm & Phạt**: Tự động tính toán số ngày trễ hạn và sinh phiếu phạt khi độc giả trả sách muộn. Xử lý nghiệp vụ thu hồi, đổi trạng thái khi sách bị báo mất hoặc hư hỏng.
* **Tra cứu & Bộ lọc**: Tra cứu chính xác bằng Bảng băm ($O(1)$) hoặc tìm kiếm/lọc tương đối (tuần tự) theo từ khóa, thể loại, tình trạng.
* **Thống kê & Báo cáo**: Tổng hợp số liệu hệ thống. Sử dụng thuật toán Sắp xếp chèn (Insertion Sort) để in bảng xếp hạng Top sách và Top bạn đọc có lượt mượn nhiều nhất.
* **Lưu trữ dữ liệu tĩnh**: Tự động đồng bộ hóa toàn bộ trạng thái hệ thống xuống các file `.json` để bảo toàn dữ liệu giữa các lần chạy.

## 4. Cấu trúc dữ liệu và giải thuật sử dụng

| Thành phần | Cấu trúc dữ liệu / giải thuật | Mục đích | Độ phức tạp chính |
|---|---|---|---|
| Lưu trữ và Tra cứu | `HashTable` | Lưu Sách, Độc giả, Phiếu mượn, Phạt. Tra cứu cực nhanh qua mã định danh. | Trung bình `O(1)` |
| Mảng dữ liệu chung | `List` (Mảng động) | Lưu trữ các danh sách trả về. Tự động cấp phát và thu hồi bộ nhớ (resize). | Truy cập `O(1)`, thêm cuối `O(1)` |
| Sắp xếp & Thống kê | `Insertion Sort` | Sắp xếp Sách/Bạn đọc theo các thuộc tính động (`getattr`) và tìm Top N. | `O(n^2)` |
| Tìm kiếm & Lọc | Tìm kiếm tuần tự | Duyệt qua danh sách đối tượng để lọc theo từ khóa, nhà xuất bản, giới tính... | `O(n)` |

Trong đó:
* `n` là số lượng đối tượng (sách, độc giả, phiếu mượn).

## 5. Định dạng dữ liệu đầu vào (JSON)

Hệ thống tự động lưu và đọc dữ liệu thông qua các tệp JSON tại thư mục `data/`.

### 5.1. File sách (`data/books.json`)
Các trường lưu trữ: `ma_sach`, `ten_sach`, `tac_gia`, `the_loai`, `nha_xuat_ban`, `so_luong`, `tinh_trang`.
Ví dụ:
```json
[
  {
    "ma_sach": "MI3310",
    "ten_sach": "Kỹ thuật lập trình",
    "tac_gia": "Vũ Thành Nam",
    "the_loai": "Giáo trình",
    "nha_xuat_ban": "HUST",
    "so_luong": 10,
    "tinh_trang": "new"
  }
]
```

### 5.2. File bạn đọc (`data/readers.json`)
Các trường lưu trữ: `ma_ban_doc`, `ho_ten`, `ngay_sinh`, `gioi_tinh`, `dia_chi`, `so_dien_thoai`.
Ví dụ:
```json
[
  {
    "ma_ban_doc": "BD001",
    "ho_ten": "Nguyễn Đăng Hiếu",
    "ngay_sinh": "2006-10-15",
    "gioi_tinh": "male",
    "dia_chi": "Hà Nội",
    "so_dien_thoai": "0912345678"
  }
]
```

### 5.3. File phiếu mượn (`data/tracks.json`)
Các trường lưu trữ: `ma_phieu`, `ma_sach`, `ma_ban_doc`, `ngay_muon`, `han_tra`, `ngay_tra_thuc_te`, `trang_thai`, `so_lan_gia_han`.
Ví dụ:
```json
[
  {
    "ma_phieu": "PH01",
    "ma_sach": "MI3310",
    "ma_ban_doc": "BD001",
    "ngay_muon": "2026-06-01",
    "han_tra": "2026-08-30",
    "ngay_tra_thuc_te": "",
    "trang_thai": "borrowing",
    "so_lan_gia_han": 0
  }
]
```

## 6. Hướng dẫn cài đặt và chạy chương trình

### 6.1. Yêu cầu chung
* Python 3.8 trở lên.
* **KHÔNG yêu cầu cài đặt thư viện bên ngoài** bằng `pip`. Dự án sử dụng hoàn toàn các thư viện chuẩn của Python (`os`, `sys`, `json`, `re`, `unittest`) và hoạt động trên mọi môi trường (Windows, macOS, Linux).

Kiểm tra phiên bản Python:
```bash
python3 --version
```

### 6.2. Tải mã nguồn
Người dùng Git có thể clone repository:
```bash
git clone [https://github.com/mynth05/Library_Management_System.git](https://github.com/mynth05/Library_Management_System.git)
cd Library_Management_System
```

Người dùng không sử dụng Git có thể tải file ZIP từ GitHub, giải nén và mở terminal tại thư mục chứa `main.py`.

### 6.3. Windows 10/11
Mở PowerShell hoặc Command Prompt tại thư mục project và chạy trực tiếp:
```powershell
python main.py
```
*(Nếu hệ thống của bạn nhận diện Python bằng lệnh `py`, hãy thay thế bằng `py main.py`).*

### 6.4. macOS
Bộ cài Python chính thức từ macOS hoặc Homebrew đều tương thích. Mở Terminal tại thư mục project và chạy:
```bash
python3 main.py
```

### 6.5. Ubuntu, Debian, Arch Linux, Fedora
Các hệ điều hành Linux vận hành CLI cực kỳ mượt mà. Mở Terminal và chạy:
```bash
python3 main.py
```

### 6.6. Sử dụng giao diện
Sau khi chạy, chương trình tự động tạo thư mục `data/` (nếu chưa có) và tải dữ liệu. Quy trình sử dụng cơ bản:
1. Nhập phím số tương ứng (1-6) để chọn các phân hệ trên Menu Chính.
2. Tại các Menu con, sử dụng bàn phím để nhập dữ liệu. Hệ thống có bộ Validate tự động bắt lỗi nhập sai định dạng.
3. Để lưu toàn bộ thay đổi và thoát, hãy chọn chức năng "Thoát" ở Menu Chính. Hệ thống sẽ tự động ghi đè dữ liệu xuống file JSON.

### 6.7. Chạy kiểm thử dành cho người phát triển
Dự án được trang bị bộ Unit Tests kiểm tra tính đúng đắn của cấu trúc dữ liệu tự cài đặt. Chạy lệnh:
```bash
python -m unittest test_library.py -v
```

### 6.8. Lỗi thường gặp

#### Lỗi UnicodeEncodeError trên Windows Console
Hệ thống hiển thị lỗi liên quan đến ký tự Unicode khi in bảng ASCII hoặc tiếng Việt. 
**Khắc phục**: Vấn đề này đã được nhóm xử lý trong `main.py` qua lệnh `reconfigure(encoding='utf-8')`. Đảm bảo bạn chạy chương trình bằng `main.py` thay vì gọi trực tiếp các module bên trong.

#### Lỗi KeyError / IndexError khi đọc file JSON
Thường xảy ra nếu người dùng mở file `books.json` hoặc `readers.json` lên và chỉnh sửa sai cú pháp bằng tay.
**Khắc phục**: Xóa các file `.json` bị lỗi trong thư mục `data/` để chương trình tự động khởi tạo lại cơ sở dữ liệu trống an toàn.

## 7. Các màn hình chính (Giao diện dòng lệnh)

* **Quản lí Sách**: In bảng danh sách Sách, thêm, sửa, xóa, tìm kiếm theo tên, lọc theo NXB và sắp xếp.
* **Quản lí Bạn Đọc**: Quản lý thông tin độc giả, chặn xóa nếu đang có phiếu mượn chưa trả.
* **Quản lí Mượn/Trả**: Thực hiện quy trình nghiệp vụ lõi. Tạo phiếu mượn, cập nhật ngày trả thực tế, gia hạn và báo hư/mất.
* **Quản lí Phạt**: In danh sách các phiếu phạt (được sinh ra tự động), cho phép tìm kiếm và thanh toán dư nợ.
* **Báo cáo Thống kê**: Hiển thị bảng tổng hợp thông số hệ thống, in bảng xếp hạng Top sách và Top bạn đọc có hoạt động nhiều nhất.

## 8. Kiểm thử tự động (Unit Tests)

Bộ Test tự động gồm 60 kịch bản bao phủ:
* Ép mảng động `List` tự động giãn nở (resize up) và thu hồi bộ nhớ (resize down).
* Ép bảng băm `HashTable` xử lý va chạm bằng Separate Chaining và kiểm tra tự động `rehash`.
* Kiểm tra các luồng nghiệp vụ: Cập nhật tồn kho, giới hạn số sách mượn đồng thời và kiểm duyệt tính hợp lệ của ngày tháng.

## 9. Các quy định nghiệp vụ và Tính phạt

Mỗi giao dịch mượn trả được kiểm soát bởi các công thức:
* **Hạn mức**: 1 bạn đọc mượn tối đa `5` cuốn sách cùng lúc.
* **Hạn trả mặc định**: `90` ngày kể từ ngày mượn.
* **Gia hạn**: Được phép gia hạn tối đa `3` lần.
* **Tính phạt trễ hạn**: `Số ngày trễ * 5,000 VNĐ`.
* **Phạt hư hỏng**: Thu hồi sách, chuyển trạng thái sang "USED". `Tiền phạt = 100,000 VNĐ + Phạt trễ hạn`.
* **Phạt mất sách**: Xóa sách khỏi hệ thống. `Tiền phạt = 300,000 VNĐ + Phạt trễ hạn`.
