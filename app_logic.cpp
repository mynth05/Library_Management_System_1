#pragma once
#include <string>
#include "models.h"
#include "custom_structures.h"
using namespace std;

class LogicApp {
private:
    HashTable<Book>      books;
    HashTable<Reader>    readers;
    HashTable<TrackBook> trackBooks;
    HashTable<Fine>      fines;

    // Đơn giản: phiếu mượn tối đa mỗi độc giả
    static const int MAX_BORROW_PER_READER = 5;

    // Tiền phạt mặc định mỗi ngày trễ
    static constexpr double FINE_PER_DAY = 5000.0; // VND

public:
    // ==================== BOOK ====================

    bool addBook(const Book& book) {
        if (book.maSach.empty()) return false;
        books.insert(book.maSach, book);
        return true;
    }

    bool removeBook(const string& maSach) {
        // Không xóa nếu đang có người mượn
        bool dangMuon = false;
        trackBooks.forEach([&](const string&, const TrackBook& t) {
            if (t.maSach == maSach && t.trangThai != TrackStatus::RETURNED)
                dangMuon = true;
        });
        if (dangMuon) return false;
        return books.remove(maSach);
    }

    Book* findBook(const string& maSach) {
        return books.get(maSach);
    }

    // Tìm kiếm sách theo tên (trả về list kết quả)
    List<Book> searchBookByName(const string& keyword) const {
        List<Book> result;
        books.forEach([&](const string&, const Book& b) {
            // Tìm không phân biệt hoa thường (đơn giản)
            string ten = b.tenSach, kw = keyword;
            for (char& c : ten) c = tolower(c);
            for (char& c : kw)  c = tolower(c);
            if (ten.find(kw) != string::npos)
                result.pushBack(b);
        });
        return result;
    }

    List<Book> searchBookByAuthor(const string& keyword) const {
        List<Book> result;
        books.forEach([&](const string&, const Book& b) {
            string tg = b.tacGia, kw = keyword;
            for (char& c : tg) c = tolower(c);
            for (char& c : kw) c = tolower(c);
            if (tg.find(kw) != string::npos)
                result.pushBack(b);
        });
        return result;
    }

    List<Book> searchBookByGenre(const string& keyword) const {
        List<Book> result;
        books.forEach([&](const string&, const Book& b) {
            string tl = b.theLoai, kw = keyword;
            for (char& c : tl) c = tolower(c);
            for (char& c : kw) c = tolower(c);
            if (tl.find(kw) != string::npos)
                result.pushBack(b);
        });
        return result;
    }

    void getAllBooks(List<Book>& out) const {
        books.forEach([&](const string&, const Book& b) {
            out.pushBack(b);
        });
    }

    // ==================== READER ====================

    bool addReader(const Reader& reader) {
        if (reader.maBanDoc.empty()) return false;
        readers.insert(reader.maBanDoc, reader);
        return true;
    }

    bool removeReader(const string& maBanDoc) {
        // Không xóa nếu đang có sách mượn
        bool dangMuon = false;
        trackBooks.forEach([&](const string&, const TrackBook& t) {
            if (t.maBanDoc == maBanDoc && t.trangThai != TrackStatus::RETURNED)
                dangMuon = true;
        });
        if (dangMuon) return false;
        return readers.remove(maBanDoc);
    }

    Reader* findReader(const string& maBanDoc) {
        return readers.get(maBanDoc);
    }

    void getAllReaders(List<Reader>& out) const {
        readers.forEach([&](const string&, const Reader& r) {
            out.pushBack(r);
        });
    }

    // Lấy danh sách phiếu mượn của một độc giả
    List<TrackBook> getBorrowsByReader(const string& maBanDoc) const {
        List<TrackBook> result;
        trackBooks.forEach([&](const string&, const TrackBook& t) {
            if (t.maBanDoc == maBanDoc)
                result.pushBack(t);
        });
        return result;
    }

    // ==================== BORROW ====================

    // Trả về: 0=OK, 1=không tìm thấy sách, 2=hết sách,
    //         3=không tìm thấy độc giả, 4=vượt giới hạn mượn,
    //         5=phiếu đã tồn tại
    int borrowBook(const string& maPhieu,
                   const string& maSach,
                   const string& maBanDoc,
                   const string& ngayMuon,
                   const string& hanTra) {
        if (trackBooks.get(maPhieu) != nullptr) return 5;

        Book* book = books.get(maSach);
        if (!book)             return 1;
        if (book->soLuong <= 0) return 2;

        Reader* reader = readers.get(maBanDoc);
        if (!reader) return 3;

        // Đếm số sách đang mượn
        int dangMuon = 0;
        trackBooks.forEach([&](const string&, const TrackBook& t) {
            if (t.maBanDoc == maBanDoc && t.trangThai != TrackStatus::RETURNED)
                dangMuon++;
        });
        if (dangMuon >= MAX_BORROW_PER_READER) return 4;

        book->soLuong--;

        TrackBook track;
        track.maPhieu   = maPhieu;
        track.maSach    = maSach;
        track.maBanDoc  = maBanDoc;
        track.ngayMuon  = ngayMuon;
        track.hanTra    = hanTra;
        track.trangThai = TrackStatus::BORROWING;
        trackBooks.insert(maPhieu, track);
        return 0;
    }

    // ==================== RETURN ====================

    // Trả về: 0=OK, 1=không tìm thấy phiếu, 2=đã trả rồi
    int returnBook(const string& maPhieu, const string& ngayTraThucTe) {
        TrackBook* track = trackBooks.get(maPhieu);
        if (!track) return 1;
        if (track->trangThai == TrackStatus::RETURNED) return 2;

        track->ngayTraThucTe = ngayTraThucTe;
        track->updateStatus(ngayTraThucTe);

        bool tre = track->isOverdue(ngayTraThucTe);
        track->trangThai = TrackStatus::RETURNED;

        Book* book = books.get(track->maSach);
        if (book) book->soLuong++;

        // Tự tạo phiếu phạt nếu trễ
        if (tre) {
            int ngayTre = track->soNgayTre(ngayTraThucTe);
            Fine fine;
            fine.maPhat      = "FINE_" + maPhieu;
            fine.maPhieu     = maPhieu;
            fine.lyDo        = FineReason::OVERDUE;
            fine.soNgayTre   = ngayTre;
            fine.tienPhatNgay = FINE_PER_DAY;
            fine.tienPhatSach = 0;
            fine.tinhTongTien();
            fine.daThanhToan = false;
            fines.insert(fine.maPhat, fine);
        }

        return 0;
    }

    TrackBook* findTrack(const string& maPhieu) {
        return trackBooks.get(maPhieu);
    }

    void getAllTracks(List<TrackBook>& out) const {
        trackBooks.forEach([&](const string&, const TrackBook& t) {
            out.pushBack(t);
        });
    }

    // Cập nhật trạng thái tất cả phiếu mượn theo ngày hôm nay
    void updateAllStatus(const string& ngayHienTai) {
        trackBooks.forEach([&](const string&, TrackBook& t) {
            t.updateStatus(ngayHienTai);
        });
    }

    // ==================== FINE ====================

    bool addFine(const Fine& fine) {
        if (fine.maPhat.empty()) return false;
        fines.insert(fine.maPhat, fine);
        return true;
    }

    Fine* findFine(const string& maPhat) {
        return fines.get(maPhat);
    }

    bool payFine(const string& maPhat) {
        Fine* fine = fines.get(maPhat);
        if (!fine || fine->daThanhToan) return false;
        fine->thanhToan();
        return true;
    }

    void getAllFines(List<Fine>& out) const {
        fines.forEach([&](const string&, const Fine& f) {
            out.pushBack(f);
        });
    }

    List<Fine> getUnpaidFines() const {
        List<Fine> result;
        fines.forEach([&](const string&, const Fine& f) {
            if (!f.daThanhToan) result.pushBack(f);
        });
        return result;
    }

    // ==================== STATISTICS ====================

    int totalBooks()         const { return books.getSize(); }
    int totalReaders()       const { return readers.getSize(); }
    int totalBorrowRecords() const { return trackBooks.getSize(); }
    int totalFines()         const { return fines.getSize(); }

    // Tổng tiền phạt chưa thu
    double totalUnpaidFineAmount() const {
        double total = 0;
        fines.forEach([&](const string&, const Fine& f) {
            if (!f.daThanhToan) total += f.tongTienPhat;
        });
        return total;
    }

    // Số sách đang được mượn (tổng số lượt)
    int totalBorrowing() const {
        int count = 0;
        trackBooks.forEach([&](const string&, const TrackBook& t) {
            if (t.trangThai == TrackStatus::BORROWING ||
                t.trangThai == TrackStatus::OVERDUE)
                count++;
        });
        return count;
    }

    int totalOverdue() const {
        int count = 0;
        trackBooks.forEach([&](const string&, const TrackBook& t) {
            if (t.trangThai == TrackStatus::OVERDUE) count++;
        });
        return count;
    }
};
