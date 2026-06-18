#include <iostream>
#include <string>
#include <ctime>
#include <cstdio>
using namespace std;

// ================================================================
// ENUMS
// ================================================================
enum class BookCondition { NEW, USED };
enum class Gender        { MALE, FEMALE, OTHER };
enum class TrackStatus   { BORROWING, RETURNED, OVERDUE };
enum class FineReason    { OVERDUE, DAMAGED, LOST };   // lý do phạt

string conditionToStr(BookCondition c) {
    return c == BookCondition::NEW ? "Moi" : "Da su dung";
}
string genderToStr(Gender g) {
    if (g == Gender::MALE)   return "Nam";
    if (g == Gender::FEMALE) return "Nu";
    return "Khac";
}
string trackStatusToStr(TrackStatus s) {
    if (s == TrackStatus::BORROWING) return "Dang muon";
    if (s == TrackStatus::RETURNED)  return "Da tra";
    return "Qua han";
}
string fineReasonToStr(FineReason r) {
    if (r == FineReason::OVERDUE)  return "Tra tre";
    if (r == FineReason::DAMAGED)  return "Sach bi hong";
    return "Mat sach";
}

// ================================================================
// HELPER: so sánh ngày "dd/mm/yyyy"
// ================================================================
// trả về số ngày từ epoch (đủ để so sánh)
static long dateToDays(const string& ddmmyyyy) {
    int d, m, y;
    sscanf(ddmmyyyy.c_str(), "%d/%d/%d", &d, &m, &y);
    // công thức đơn giản, không cần thư viện ngoài
    m = (m + 9) % 12;
    y -= m / 10;
    return 365L*y + y/4 - y/100 + y/400 + (m*306 + 5)/10 + d - 1;
}

static string todayStr() {
    time_t now = time(nullptr);
    tm*    t   = localtime(&now);
    char   buf[12];
    sprintf(buf, "%02d/%02d/%04d",
            t->tm_mday, t->tm_mon + 1, t->tm_year + 1900);
    return string(buf);
}

// ================================================================
// 1. BOOK
// ================================================================
struct Book {
    string        ma_sach;
    string        ten_sach;
    string        tac_gia;
    string        the_loai;
    string        nha_xuat_ban;
    int           so_luong;
    BookCondition tinh_trang;

    // ---- Constructors ----
    Book()
        : so_luong(0), tinh_trang(BookCondition::NEW) {}

    Book(const string& ms, const string& ts, const string& tg,
         const string& tl, const string& nxb,
         int sl, BookCondition tt)
        : ma_sach(ms), ten_sach(ts), tac_gia(tg),
          the_loai(tl), nha_xuat_ban(nxb),
          so_luong(sl), tinh_trang(tt) {}

    // ---- Thao tác ----
    bool matchFilter(const string& kw) const {
        return ma_sach.find(kw)      != string::npos ||
               ten_sach.find(kw)     != string::npos ||
               tac_gia.find(kw)      != string::npos ||
               the_loai.find(kw)     != string::npos ||
               nha_xuat_ban.find(kw) != string::npos;
    }

    // ---- Bộ lọc ----
    bool filterByTheLoai(const string& tl)  const { return the_loai  == tl; }
    bool filterByTinhTrang(BookCondition tt) const { return tinh_trang == tt; }

    void display() const {
        cout << "-------------------------------\n"
             << "Ma sach      : " << ma_sach                     << "\n"
             << "Ten sach     : " << ten_sach                    << "\n"
             << "Tac gia      : " << tac_gia                     << "\n"
             << "The loai     : " << the_loai                    << "\n"
             << "NXB          : " << nha_xuat_ban                << "\n"
             << "So luong     : " << so_luong                    << "\n"
             << "Tinh trang   : " << conditionToStr(tinh_trang)  << "\n";
    }
};

ostream& operator<<(ostream& os, const Book& b) {
    os << "[" << b.ma_sach << "] " << b.ten_sach
       << " | " << b.tac_gia
       << " | " << conditionToStr(b.tinh_trang);
    return os;
}

// ================================================================
// 2. READER
// ================================================================
struct Reader {
    string ma_ban_doc;
    string ho_ten;
    string ngay_sinh;       // "dd/mm/yyyy"
    Gender gioi_tinh;
    string dia_chi;
    string so_dien_thoai;

    // ---- Constructors ----
    Reader() : gioi_tinh(Gender::OTHER) {}

    Reader(const string& mbd, const string& ht, const string& ns,
           Gender gt, const string& dc, const string& sdt)
        : ma_ban_doc(mbd), ho_ten(ht), ngay_sinh(ns),
          gioi_tinh(gt), dia_chi(dc), so_dien_thoai(sdt) {}

    // ---- Thao tác ----
    bool matchFilter(const string& kw) const {
        return ma_ban_doc.find(kw)    != string::npos ||
               ho_ten.find(kw)        != string::npos ||
               so_dien_thoai.find(kw) != string::npos ||
               dia_chi.find(kw)       != string::npos;
    }

    // ---- Bộ lọc ----
    bool filterByGioiTinh(Gender gt) const { return gioi_tinh == gt; }

    void display() const {
        cout << "-------------------------------\n"
             << "Ma ban doc   : " << ma_ban_doc               << "\n"
             << "Ho ten       : " << ho_ten                   << "\n"
             << "Ngay sinh    : " << ngay_sinh                << "\n"
             << "Gioi tinh    : " << genderToStr(gioi_tinh)  << "\n"
             << "Dia chi      : " << dia_chi                  << "\n"
             << "So DT        : " << so_dien_thoai            << "\n";
    }
};

ostream& operator<<(ostream& os, const Reader& r) {
    os << "[" << r.ma_ban_doc << "] " << r.ho_ten
       << " | " << genderToStr(r.gioi_tinh);
    return os;
}

// ================================================================
// 3. TRACKBOOK
// ================================================================
struct TrackBook {
    string      ma_phieu;
    string      ma_sach;          // FK -> Book
    string      ma_ban_doc;       // FK -> Reader
    string      ngay_muon;        // "dd/mm/yyyy"
    string      han_tra;          // "dd/mm/yyyy"
    string      ngay_tra_thuc_te; // "" nếu chưa trả
    TrackStatus trang_thai;

    // ---- Constructors ----
    TrackBook() : trang_thai(TrackStatus::BORROWING) {}

    TrackBook(const string& mp, const string& ms, const string& mbd,
              const string& ngay_muon_, const string& han_tra_)
        : ma_phieu(mp), ma_sach(ms), ma_ban_doc(mbd),
          ngay_muon(ngay_muon_), han_tra(han_tra_),
          ngay_tra_thuc_te(""), trang_thai(TrackStatus::BORROWING) {}

    // ---- Thao tác ----
    bool isOverdue() const {
        string moc =
            ngay_tra_thuc_te.empty()
            ? todayStr()
            : ngay_tra_thuc_te;
    
        return dateToDays(moc) > dateToDays(han_tra);
    }

    int soNgayTre() const {
    string moc =
        ngay_tra_thuc_te.empty()
        ? todayStr()
        : ngay_tra_thuc_te;

    long diff =
        dateToDays(moc) - dateToDays(han_tra);

    return diff > 0 ? (int)diff : 0;
    }
    void updateStatus() {
        if (!ngay_tra_thuc_te.empty())
            trang_thai = TrackStatus::RETURNED;
        else if (isOverdue())
            trang_thai = TrackStatus::OVERDUE;
        else
            trang_thai = TrackStatus::BORROWING;
    }

    // ---- Bộ lọc ----
    bool filterByMaSach(const string& ms)   const { return ma_sach    == ms; }
    bool filterByMaBanDoc(const string& mbd) const { return ma_ban_doc == mbd; }
    bool filterByStatus(TrackStatus s)       const { return trang_thai == s; }

    void display() const {
        cout << "-------------------------------\n"
             << "Ma phieu     : " << ma_phieu                      << "\n"
             << "Ma sach      : " << ma_sach                       << "\n"
             << "Ma ban doc   : " << ma_ban_doc                    << "\n"
             << "Ngay muon    : " << ngay_muon                     << "\n"
             << "Han tra      : " << han_tra                       << "\n"
             << "Ngay tra     : " << (ngay_tra_thuc_te.empty()
                                      ? "Chua tra" : ngay_tra_thuc_te) << "\n"
             << "Trang thai   : " << trackStatusToStr(trang_thai)  << "\n"
             << "So ngay tre  : " << soNgayTre()                   << "\n";
    }
};

ostream& operator<<(ostream& os, const TrackBook& tb) {
    os << "[" << tb.ma_phieu << "] "
       << tb.ma_sach << " <- " << tb.ma_ban_doc
       << " | " << trackStatusToStr(tb.trang_thai);
    return os;
}

// ================================================================
// 4. FINE  (tách riêng, quan hệ 1:0..1 với TrackBook)
// ================================================================
struct Fine {
    string     ma_phat;
    string     ma_phieu;          // FK -> TrackBook (1:1)
    FineReason ly_do;
    int        so_ngay_tre;
    double     tien_phat_ngay;    // VND/ngày
    double     tien_phat_sach;    // bồi thường nếu hỏng/mất
    double     tong_tien_phat;    // tự tính trong constructor
    bool       da_thanh_toan;

    // Đơn giá mặc định (có thể thay đổi theo chính sách)
    static constexpr double DON_GIA_NGAY  = 2000.0;  // 2,000 VND/ngày trễ
    static constexpr double DON_GIA_HONG  = 50000.0; // bồi thường sách hỏng
    static constexpr double DON_GIA_MAT   = 150000.0;// bồi thường mất sách

    // ---- Constructors ----
    Fine() : so_ngay_tre(0), tien_phat_ngay(0),
             tien_phat_sach(0), tong_tien_phat(0),
             da_thanh_toan(false), ly_do(FineReason::OVERDUE) {}

    // Tạo Fine từ TrackBook đã xác định vi phạm
    Fine(const string& mp_phat, const TrackBook& tb, FineReason reason)
        : ma_phat(mp_phat),
          ma_phieu(tb.ma_phieu),
          ly_do(reason),
          so_ngay_tre(tb.soNgayTre()),
          da_thanh_toan(false)
    {
        tien_phat_ngay = so_ngay_tre * DON_GIA_NGAY;

        if      (reason == FineReason::DAMAGED) tien_phat_sach = DON_GIA_HONG;
        else if (reason == FineReason::LOST)    tien_phat_sach = DON_GIA_MAT;
        else                                    tien_phat_sach = 0.0;

        tong_tien_phat = tien_phat_ngay + tien_phat_sach;
    }

    // ---- Thao tác ----
    void thanhToan() { da_thanh_toan = true; }

    // ---- Bộ lọc ----
    bool filterByMaPhieu(const string& mp) const { return ma_phieu == mp; }
    bool filterChuaTra()                   const { return !da_thanh_toan; }

    void display() const {
        cout << "-------------------------------\n"
             << "Ma phat      : " << ma_phat                      << "\n"
             << "Ma phieu     : " << ma_phieu                     << "\n"
             << "Ly do        : " << fineReasonToStr(ly_do)       << "\n"
             << "So ngay tre  : " << so_ngay_tre                  << "\n"
             << "Phat tre han : " << tien_phat_ngay   << " VND\n"
             << "Boi thuong   : " << tien_phat_sach   << " VND\n"
             << "Tong phat    : " << tong_tien_phat   << " VND\n"
             << "Trang thai   : " << (da_thanh_toan ? "Da nop" : "Chua nop") << "\n";
    }
};

ostream& operator<<(ostream& os, const Fine& f) {
    os << "[" << f.ma_phat << "] phieu=" << f.ma_phieu
       << " | " << fineReasonToStr(f.ly_do)
       << " | " << f.tong_tien_phat << " VND"
       << " | " << (f.da_thanh_toan ? "Da nop" : "Chua nop");
    return os;
}
