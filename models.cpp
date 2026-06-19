#pragma once
#include <string>

using namespace std;

enum class BookCondition {
    NEW,
    USED
};

struct Book {
    string maSach;
    string tenSach;
    string tacGia;
    string theLoai;
    string nhaXuatBan;

    int soLuong;

    BookCondition trangThai;
};

enum class Gender {
    MALE,
    FEMALE,
    OTHER
};

struct Reader {
    string maBanDoc;
    string hoTen;
    string ngaySinh;

    Gender gioiTinh;

    string diaChi;
    string soDienThoai;
};

enum class TrackStatus {
    BORROWING,
    RETURNED,
    OVERDUE
};

struct TrackBook {
    string maPhieu;

    string maSach;
    string maBanDoc;

    string ngayMuon;
    string hanTra;
    string ngayTraThucTe;

    TrackStatus trangThai;

    bool isOverdue() const {
        return trangThai == TrackStatus::OVERDUE;
    }

    int soNgayTre() const {
        return 0;
    }

    void updateStatus() {
    }
};
enum class FineReason {
    OVERDUE,
    LOST_BOOK,
    DAMAGED_BOOK
};

struct Fine {
    string maPhat;
    string maPhieu;

    FineReason lyDo;

    int soNgayTre;

    double tienPhatNgay;
    double tienPhatSach;
    double tongTienPhat;

    bool daThanhToan;

    void thanhToan() {
        daThanhToan = true;
    }
};
