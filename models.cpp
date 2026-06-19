#pragma once
#include <string>
using namespace std;

// ==================== BOOK ====================
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

    Book() : soLuong(0), trangThai(BookCondition::NEW) {}
};

// ==================== READER ====================
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

    Reader() : gioiTinh(Gender::OTHER) {}
};

// ==================== TRACK BOOK ====================
enum class TrackStatus {
    BORROWING,
    RETURNED,
    OVERDUE
};

// Utility: parse "DD/MM/YYYY" -> days since epoch (rough, for comparison)
inline long dateToDays(const string& date) {
    if (date.size() < 10) return 0;
    int d = stoi(date.substr(0, 2));
    int m = stoi(date.substr(3, 2));
    int y = stoi(date.substr(6, 4));
    // Zeller-style approximation
    if (m < 3) { m += 12; y--; }
    return 365L * y + y / 4 - y / 100 + y / 400 + (153 * m - 457) / 5 + d;
}

struct TrackBook {
    string maPhieu;
    string maSach;
    string maBanDoc;
    string ngayMuon;   // "DD/MM/YYYY"
    string hanTra;     // "DD/MM/YYYY"
    string ngayTraThucTe; // "" nếu chưa trả
    TrackStatus trangThai;

    TrackBook() : trangThai(TrackStatus::BORROWING) {}

    // Tính số ngày trễ so với ngayTraThucTe (hoặc hôm nay nếu chưa trả)
    int soNgayTre(const string& ngayHienTai = "") const {
        if (hanTra.empty()) return 0;
        string ngayTra = ngayTraThucTe.empty() ? ngayHienTai : ngayTraThucTe;
        if (ngayTra.empty()) return 0;
        long diff = dateToDays(ngayTra) - dateToDays(hanTra);
        return (diff > 0) ? (int)diff : 0;
    }

    bool isOverdue(const string& ngayHienTai = "") const {
        if (trangThai == TrackStatus::RETURNED) return false;
        if (hanTra.empty() || ngayHienTai.empty()) return trangThai == TrackStatus::OVERDUE;
        return dateToDays(ngayHienTai) > dateToDays(hanTra);
    }

    void updateStatus(const string& ngayHienTai) {
        if (trangThai == TrackStatus::RETURNED) return;
        if (isOverdue(ngayHienTai))
            trangThai = TrackStatus::OVERDUE;
    }
};

// ==================== FINE ====================
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
    double tienPhatNgay;   // phạt mỗi ngày trễ
    double tienPhatSach;   // phạt mất/hỏng sách
    double tongTienPhat;
    bool daThanhToan;

    Fine()
        : lyDo(FineReason::OVERDUE),
          soNgayTre(0),
          tienPhatNgay(0), tienPhatSach(0),
          tongTienPhat(0), daThanhToan(false) {}

    void tinhTongTien() {
        tongTienPhat = soNgayTre * tienPhatNgay + tienPhatSach;
    }

    void thanhToan() {
        daThanhToan = true;
    }
};
