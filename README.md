# HỆ THỐNG QUẢN LÝ THƯ VIỆN

Bài tập cá nhân/nhóm môn Kỹ thuật Lập trình - Đại học Bách Khoa Hà Nội.

169314 - MI3310

## 1. Thông tin nhóm sinh viên

* Phạm Thị Minh Thuý - 202418992
* Nguyễn Đăng Hiếu - 202418900

## 2. Cấu trúc mã nguồn

* `main.py`: Điểm khởi đầu của chương trình, thiết lập môi trường mã hóa UTF-8 cho Console và gọi hàm khởi chạy ứng dụng.
* `app_logic.py`: Chứa logic lõi của hệ thống: kiểm duyệt đầu vào (Validator), xử lý CRUD, quy tắc mượn/trả, tự động sinh phiếu phạt, thuật toán sắp xếp và thao tác đọc/ghi file JSON.
* `models.py`: Định nghĩa các lớp đối tượng dữ liệu thuần túy gồm `Book`, `Reader`, `TrackBook`, `Fine` và các trạng thái `Enum` tương ứng.
* `custom_structures.py`: Chứa các cấu trúc dữ liệu nền tảng **tự cài đặt 100%**, bao gồm mảng động `List`, nút liên kết `HashNode` và bảng băm `HashTable`.
* `ui/`: Chứa giao diện dòng lệnh (CLI) được module hóa:
  * `cli.py`: Quản lý hệ thống Menu chính và điều hướng.
  * `widges.py`: Chứa các tiện ích dùng chung như hàm xóa màn hình, in tiêu đề, vẽ bảng hiển thị ASCII và các hàm hỗ trợ nhập liệu chặt chẽ (`try-except`).
  * `manage_book_tab.py`: Phân hệ quản lý Sách.
  * `manage_reader_tab.py`: Phân hệ quản lý Bạn đọc.
  * `manage_borrow_return_tab.py`: Phân hệ quản lý Mượn/Trả sách.
  * `manage_fine_tab.py`: Phân hệ quản lý Phạt.
  * `manage_record_tab.py`: Phân hệ báo cáo thống kê.
* `test_library.py`: Bộ kiểm thử tự động toàn diện (Unit Tests) với gần 60 kịch bản bao phủ các cấu trúc dữ liệu và logic hệ thống.
* `data/`: Thư mục chứa cơ sở dữ liệu của hệ thống dưới định dạng JSON.

## 3. Mô tả tổng quan

Chương trình là một Hệ thống Quản lý Thư viện hoạt động trên môi trường giao diện dòng lệnh (CLI). Điểm đặc biệt của dự án là **không phụ thuộc vào các cấu trúc dữ liệu mặc định của Python** (như `list` hay `dict`), mà sử dụng hoàn toàn cấu trúc dữ liệu tự thiết kế, đảm bảo chuẩn đầu ra của môn Kỹ thuật Lập trình.

Các chức năng chính:

* **Quản lý Danh mục Sách & Bạn đọc**: Thêm, sửa, xóa, tìm kiếm, lọc và sắp xếp dữ liệu. Các thông tin được lưu trữ và tra cứu cực nhanh theo mã định danh duy nhất.
* **Xử lý Mượn/Trả sách**: Ràng buộc logic chặt chẽ (kiểm tra tồn kho, kiểm tra giới hạn 5 cuốn/người). Hỗ trợ gia hạn sách (tối đa 3 lần).
* **Quản lý Vi phạm & Phạt**: Tự động tính toán số ngày trễ hạn và sinh phiếu phạt khi độc giả trả sách muộn. Xử lý nghiệp vụ khi sách bị báo mất hoặc hư hỏng.
* **Tra cứu & Bộ lọc**: Tra cứu chính xác bằng Bảng băm ($O(1)$) hoặc tìm kiếm/lọc tương đối theo từ khóa, thể loại, tình trạng.
* **Thống kê & Báo cáo**: Thống kê số liệu tổng quan của thư viện. Sử dụng thuật toán sắp xếp chèn (Insertion Sort) để tìm Top những cuốn sách và bạn đọc có lượt mượn nhiều nhất.
* **Lưu trữ dữ liệu tĩnh**: Tự động đồng bộ hóa toàn bộ trạng thái hệ thống xuống các file `.json` để bảo toàn dữ liệu giữa các lần chạy.

## 4. Cấu trúc dữ liệu và giải thuật sử dụng

| Thành phần | Cấu trúc dữ liệu / giải thuật | Mục đích | Độ phức tạp chính |
|---|---|---|---|
| Mảng dữ liệu chung | `List` (Mảng động tự cài đặt) | Lưu trữ mọi danh sách tuần tự. Tự động cấp phát (nhân đôi) hoặc thu hồi bộ nhớ. | Truy cập `O(1)`, Thêm cuối trung bình `O(1)` |
| Lưu trữ và Tra cứu | `HashTable` (Separate Chaining) | Lưu dữ liệu Sách, Độc giả, Phiếu mượn, Phạt. Tra cứu cực nhanh qua `id`. Tự động `rehash` khi đạt tải 0.75. | Trung bình `O(1)` |
| Sắp xếp & Thống kê | `Insertion Sort` (Sắp xếp chèn) | Sắp xếp Sách/Bạn đọc theo các thuộc tính động (`getattr`) và tìm Top N. | `O(N^2)` tối đa, rất nhanh với dữ liệu nhỏ/đã sắp xếp một phần |
| Tìm kiếm & Lọc | Tìm kiếm tuần tự | Duyệt qua danh sách đối tượng để lọc theo từ khóa, nhà xuất bản, giới tính... | `O(N)` |

## 5. Định dạng dữ liệu lưu trữ

Hệ thống lưu trữ dữ liệu bền vững dưới định dạng JSON tại thư mục `data/`. Quá trình đọc/ghi (Serialization/Deserialization) được thực hiện thông qua các hàm `to_dict()` và `from_dict()` trong các class Model.

### 5.1. File sách (`data/books.json`)
Lưu danh mục sách. Ví dụ:
```json
[
  {
    "ma_sach": "MI3310",
    "ten_sach": "Kỹ thuật lập trình",
    "tac_gia": "Vũ Thành Nam",
    "the_loai": "Giáo trình",
    "nha_xuat_ban": "Bách khoa",
    "so_luong": 10,
    "tinh_trang": "new"
  }
]
