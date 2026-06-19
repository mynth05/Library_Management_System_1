#include <iostream>
#include <string>
#include <iomanip>
#include <limits>
#include <climits>
#include "models.h"
#include "custom_structures.h"
#include "app_logic.h"
using namespace std;

// ==================== HELPERS ====================

void clearScreen() {
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
}

void pauseEnter() {
    cout << "\n  Nhan Enter de tiep tuc...";
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    cin.get();
}

string nhapChuoi(const string& prompt) {
    cout << "  " << prompt;
    string s;
    getline(cin, s);
    return s;
}

int nhapSoNguyen(const string& prompt, int min = INT_MIN, int max = INT_MAX) {
    int val;
    while (true) {
        cout << "  " << prompt;
        if (cin >> val && val >= min && val <= max) {
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            return val;
        }
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        cout << "  >> Gia tri khong hop le, vui long nhap lai!\n";
    }
}

void divider(char c = '-', int len = 55) {
    cout << "  ";
    for (int i = 0; i < len; i++) cout << c;
    cout << "\n";
}

void header(const string& title) {
    clearScreen();
    divider('=');
    cout << "  " << left << setw(53) << ("  " + title) << "\n";
    divider('=');
}

// Hiển thị ngày giờ hệ thống đơn giản (dùng ctime)
string ngayHomNay() {
    time_t t = time(nullptr);
    tm* lt = localtime(&t);
    char buf[20];
    sprintf(buf, "%02d/%02d/%04d", lt->tm_mday, lt->tm_mon + 1, lt->tm_year + 1900);
    return string(buf);
}

string conditionStr(BookCondition c) {
    return (c == BookCondition::NEW) ? "Moi" : "Da dung";
}

string genderStr(Gender g) {
    if (g == Gender::MALE)   return "Nam";
    if (g == Gender::FEMALE) return "Nu";
    return "Khac";
}

string trackStatusStr(TrackStatus s) {
    if (s == TrackStatus::BORROWING) return "Dang muon";
    if (s == TrackStatus::RETURNED)  return "Da tra";
    return "QUA HAN";
}

string fineReasonStr(FineReason r) {
    if (r == FineReason::OVERDUE)      return "Tra tre";
    if (r == FineReason::LOST_BOOK)    return "Mat sach";
    return "Hu hong";
}

void inSach(const Book& b) {
    cout << "  Ma sach   : " << b.maSach      << "\n"
         << "  Ten sach  : " << b.tenSach     << "\n"
         << "  Tac gia   : " << b.tacGia      << "\n"
         << "  The loai  : " << b.theLoai     << "\n"
         << "  NXB       : " << b.nhaXuatBan  << "\n"
         << "  So luong  : " << b.soLuong     << "\n"
         << "  Tinh trang: " << conditionStr(b.trangThai) << "\n";
}

void inDocGia(const Reader& r) {
    cout << "  Ma ban doc : " << r.maBanDoc     << "\n"
         << "  Ho ten     : " << r.hoTen        << "\n"
         << "  Ngay sinh  : " << r.ngaySinh     << "\n"
         << "  Gioi tinh  : " << genderStr(r.gioiTinh) << "\n"
         << "  Dia chi    : " << r.diaChi       << "\n"
         << "  SDT        : " << r.soDienThoai  << "\n";
}

void inPhieu(const TrackBook& t) {
    cout << "  Ma phieu   : " << t.maPhieu      << "\n"
         << "  Ma sach    : " << t.maSach       << "\n"
         << "  Ma ban doc : " << t.maBanDoc     << "\n"
         << "  Ngay muon  : " << t.ngayMuon     << "\n"
         << "  Han tra    : " << t.hanTra        << "\n"
         << "  Ngay tra TT: " << (t.ngayTraThucTe.empty() ? "---" : t.ngayTraThucTe) << "\n"
         << "  Trang thai : " << trackStatusStr(t.trangThai) << "\n";
}

void inPhat(const Fine& f) {
    cout << "  Ma phat    : " << f.maPhat       << "\n"
         << "  Ma phieu   : " << f.maPhieu      << "\n"
         << "  Ly do      : " << fineReasonStr(f.lyDo) << "\n"
         << "  So ngay tre: " << f.soNgayTre    << "\n"
         << fixed << setprecision(0)
         << "  Phat/ngay  : " << f.tienPhatNgay << " VND\n"
         << "  Phat sach  : " << f.tienPhatSach << " VND\n"
         << "  Tong tien  : " << f.tongTienPhat << " VND\n"
         << "  Thanh toan : " << (f.daThanhToan ? "Da thanh toan" : "CHUA THANH TOAN") << "\n";
}

// ==================== MENU SÁCH ====================

void menuSach(LogicApp& app) {
    while (true) {
        header("QUAN LY SACH");
        cout << "  [1] Them sach\n"
             << "  [2] Tim kiem sach\n"
             << "  [3] Xem tat ca sach\n"
             << "  [4] Xoa sach\n"
             << "  [0] Quay lai\n";
        divider();
        int ch = nhapSoNguyen("Chon: ", 0, 4);

        if (ch == 0) break;

        if (ch == 1) {
            header("THEM SACH");
            Book b;
            b.maSach     = nhapChuoi("Ma sach    : ");
            b.tenSach    = nhapChuoi("Ten sach   : ");
            b.tacGia     = nhapChuoi("Tac gia    : ");
            b.theLoai    = nhapChuoi("The loai   : ");
            b.nhaXuatBan = nhapChuoi("NXB        : ");
            b.soLuong    = nhapSoNguyen("So luong   : ", 0);
            int tt = nhapSoNguyen("Tinh trang (1=Moi, 2=Da dung): ", 1, 2);
            b.trangThai  = (tt == 1) ? BookCondition::NEW : BookCondition::USED;

            if (app.addBook(b))
                cout << "\n  >> Them sach thanh cong!\n";
            else
                cout << "\n  >> Loi: Ma sach khong hop le!\n";
            pauseEnter();
        }

        else if (ch == 2) {
            header("TIM KIEM SACH");
            cout << "  [1] Theo ten\n"
                 << "  [2] Theo tac gia\n"
                 << "  [3] Theo the loai\n"
                 << "  [4] Theo ma sach\n";
            int opt = nhapSoNguyen("Chon: ", 1, 4);
            string kw = nhapChuoi("Nhap tu khoa: ");

            List<Book> result;
            if (opt == 1) result = app.searchBookByName(kw);
            else if (opt == 2) result = app.searchBookByAuthor(kw);
            else if (opt == 3) result = app.searchBookByGenre(kw);
            else {
                Book* b = app.findBook(kw);
                if (b) result.pushBack(*b);
            }

            divider();
            if (result.getSize() == 0) {
                cout << "  Khong tim thay ket qua.\n";
            } else {
                cout << "  Tim thay " << result.getSize() << " ket qua:\n";
                for (int i = 0; i < result.getSize(); i++) {
                    divider('-', 40);
                    inSach(result[i]);
                }
            }
            pauseEnter();
        }

        else if (ch == 3) {
            header("DANH SACH SACH");
            List<Book> all;
            app.getAllBooks(all);
            if (all.getSize() == 0) {
                cout << "  Chua co sach nao.\n";
            } else {
                cout << "  Tong: " << all.getSize() << " sach\n";
                for (int i = 0; i < all.getSize(); i++) {
                    divider('-', 40);
                    inSach(all[i]);
                }
            }
            pauseEnter();
        }

        else if (ch == 4) {
            header("XOA SACH");
            string ma = nhapChuoi("Ma sach can xoa: ");
            if (app.removeBook(ma))
                cout << "\n  >> Xoa thanh cong!\n";
            else
                cout << "\n  >> Loi: Khong tim thay hoac sach dang duoc muon!\n";
            pauseEnter();
        }
    }
}

// ==================== MENU ĐỘC GIẢ ====================

void menuDocGia(LogicApp& app) {
    while (true) {
        header("QUAN LY DOC GIA");
        cout << "  [1] Them doc gia\n"
             << "  [2] Tim doc gia theo ma\n"
             << "  [3] Xem tat ca doc gia\n"
             << "  [4] Xoa doc gia\n"
             << "  [5] Xem lich su muon cua doc gia\n"
             << "  [0] Quay lai\n";
        divider();
        int ch = nhapSoNguyen("Chon: ", 0, 5);

        if (ch == 0) break;

        if (ch == 1) {
            header("THEM DOC GIA");
            Reader r;
            r.maBanDoc    = nhapChuoi("Ma ban doc  : ");
            r.hoTen       = nhapChuoi("Ho ten      : ");
            r.ngaySinh    = nhapChuoi("Ngay sinh   : ");
            int gt = nhapSoNguyen("Gioi tinh (1=Nam, 2=Nu, 3=Khac): ", 1, 3);
            r.gioiTinh    = (gt == 1) ? Gender::MALE : (gt == 2) ? Gender::FEMALE : Gender::OTHER;
            r.diaChi      = nhapChuoi("Dia chi     : ");
            r.soDienThoai = nhapChuoi("So dien thoai: ");

            if (app.addReader(r))
                cout << "\n  >> Them doc gia thanh cong!\n";
            else
                cout << "\n  >> Loi: Ma ban doc khong hop le!\n";
            pauseEnter();
        }

        else if (ch == 2) {
            header("TIM DOC GIA");
            string ma = nhapChuoi("Ma ban doc: ");
            Reader* r = app.findReader(ma);
            divider('-', 40);
            if (r) inDocGia(*r);
            else cout << "  Khong tim thay doc gia.\n";
            pauseEnter();
        }

        else if (ch == 3) {
            header("DANH SACH DOC GIA");
            List<Reader> all;
            app.getAllReaders(all);
            if (all.getSize() == 0) {
                cout << "  Chua co doc gia nao.\n";
            } else {
                cout << "  Tong: " << all.getSize() << " doc gia\n";
                for (int i = 0; i < all.getSize(); i++) {
                    divider('-', 40);
                    inDocGia(all[i]);
                }
            }
            pauseEnter();
        }

        else if (ch == 4) {
            header("XOA DOC GIA");
            string ma = nhapChuoi("Ma ban doc can xoa: ");
            if (app.removeReader(ma))
                cout << "\n  >> Xoa thanh cong!\n";
            else
                cout << "\n  >> Loi: Khong tim thay hoac doc gia dang muon sach!\n";
            pauseEnter();
        }

        else if (ch == 5) {
            header("LICH SU MUON");
            string ma = nhapChuoi("Ma ban doc: ");
            List<TrackBook> tracks = app.getBorrowsByReader(ma);
            if (tracks.getSize() == 0) {
                cout << "  Khong co lich su muon.\n";
            } else {
                cout << "  Tim thay " << tracks.getSize() << " phieu:\n";
                for (int i = 0; i < tracks.getSize(); i++) {
                    divider('-', 40);
                    inPhieu(tracks[i]);
                }
            }
            pauseEnter();
        }
    }
}

// ==================== MENU MƯỢN / TRẢ ====================

void menuMuonTra(LogicApp& app) {
    while (true) {
        header("MUON / TRA SACH");
        cout << "  [1] Muon sach\n"
             << "  [2] Tra sach\n"
             << "  [3] Xem phieu muon theo ma phieu\n"
             << "  [4] Xem tat ca phieu muon\n"
             << "  [0] Quay lai\n";
        divider();
        int ch = nhapSoNguyen("Chon: ", 0, 4);

        if (ch == 0) break;

        if (ch == 1) {
            header("MUON SACH");
            string maPhieu  = nhapChuoi("Ma phieu  : ");
            string maSach   = nhapChuoi("Ma sach   : ");
            string maBanDoc = nhapChuoi("Ma ban doc: ");
            string ngayMuon = nhapChuoi("Ngay muon (DD/MM/YYYY): ");
            string hanTra   = nhapChuoi("Han tra   (DD/MM/YYYY): ");

            int ret = app.borrowBook(maPhieu, maSach, maBanDoc, ngayMuon, hanTra);
            cout << "\n";
            if      (ret == 0) cout << "  >> Muon sach thanh cong!\n";
            else if (ret == 1) cout << "  >> Loi: Khong tim thay sach!\n";
            else if (ret == 2) cout << "  >> Loi: Sach da het!\n";
            else if (ret == 3) cout << "  >> Loi: Khong tim thay doc gia!\n";
            else if (ret == 4) cout << "  >> Loi: Doc gia da muon qua 5 cuon!\n";
            else if (ret == 5) cout << "  >> Loi: Ma phieu da ton tai!\n";
            pauseEnter();
        }

        else if (ch == 2) {
            header("TRA SACH");
            string maPhieu = nhapChuoi("Ma phieu  : ");
            string ngayTra = nhapChuoi("Ngay tra  (DD/MM/YYYY) [Enter = hom nay]: ");
            if (ngayTra.empty()) ngayTra = ngayHomNay();

            int ret = app.returnBook(maPhieu, ngayTra);
            cout << "\n";
            if (ret == 0) {
                cout << "  >> Tra sach thanh cong!\n";
                // Kiểm tra xem có phiếu phạt tự động không
                Fine* f = app.findFine("FINE_" + maPhieu);
                if (f) {
                    cout << "  >> CANH BAO: Sach tra tre! Da tao phieu phat:\n";
                    divider('-', 40);
                    inPhat(*f);
                }
            }
            else if (ret == 1) cout << "  >> Loi: Khong tim thay phieu muon!\n";
            else if (ret == 2) cout << "  >> Loi: Sach nay da duoc tra roi!\n";
            pauseEnter();
        }

        else if (ch == 3) {
            header("XEM PHIEU MUON");
            string ma = nhapChuoi("Ma phieu: ");
            TrackBook* t = app.findTrack(ma);
            divider('-', 40);
            if (t) inPhieu(*t);
            else cout << "  Khong tim thay phieu muon.\n";
            pauseEnter();
        }

        else if (ch == 4) {
            header("TAT CA PHIEU MUON");
            List<TrackBook> all;
            app.getAllTracks(all);
            if (all.getSize() == 0) {
                cout << "  Chua co phieu muon nao.\n";
            } else {
                cout << "  Tong: " << all.getSize() << " phieu\n";
                for (int i = 0; i < all.getSize(); i++) {
                    divider('-', 40);
                    inPhieu(all[i]);
                }
            }
            pauseEnter();
        }
    }
}

// ==================== MENU PHẠT ====================

void menuPhat(LogicApp& app) {
    while (true) {
        header("QUAN LY PHAT");
        cout << "  [1] Them phieu phat thu cong\n"
             << "  [2] Thanh toan phieu phat\n"
             << "  [3] Tim phieu phat theo ma\n"
             << "  [4] Xem tat ca phieu phat\n"
             << "  [5] Xem phieu phat chua thanh toan\n"
             << "  [0] Quay lai\n";
        divider();
        int ch = nhapSoNguyen("Chon: ", 0, 5);

        if (ch == 0) break;

        if (ch == 1) {
            header("THEM PHIEU PHAT");
            Fine f;
            f.maPhat  = nhapChuoi("Ma phat   : ");
            f.maPhieu = nhapChuoi("Ma phieu  : ");
            int ly = nhapSoNguyen("Ly do (1=Tra tre, 2=Mat sach, 3=Hu hong): ", 1, 3);
            f.lyDo    = (ly == 1) ? FineReason::OVERDUE :
                        (ly == 2) ? FineReason::LOST_BOOK : FineReason::DAMAGED_BOOK;
            f.soNgayTre   = nhapSoNguyen("So ngay tre : ", 0);
            f.tienPhatNgay = nhapSoNguyen("Phat/ngay (VND): ", 0);
            f.tienPhatSach = nhapSoNguyen("Phat sach (VND): ", 0);
            f.tinhTongTien();
            f.daThanhToan = false;

            if (app.addFine(f))
                cout << "\n  >> Them phieu phat thanh cong! Tong tien: "
                     << fixed << setprecision(0) << f.tongTienPhat << " VND\n";
            else
                cout << "\n  >> Loi: Ma phat khong hop le!\n";
            pauseEnter();
        }

        else if (ch == 2) {
            header("THANH TOAN PHAT");
            string ma = nhapChuoi("Ma phat: ");
            if (app.payFine(ma))
                cout << "\n  >> Thanh toan thanh cong!\n";
            else
                cout << "\n  >> Loi: Khong tim thay hoac da thanh toan roi!\n";
            pauseEnter();
        }

        else if (ch == 3) {
            header("TIM PHIEU PHAT");
            string ma = nhapChuoi("Ma phat: ");
            Fine* f = app.findFine(ma);
            divider('-', 40);
            if (f) inPhat(*f);
            else cout << "  Khong tim thay phieu phat.\n";
            pauseEnter();
        }

        else if (ch == 4) {
            header("TAT CA PHIEU PHAT");
            List<Fine> all;
            app.getAllFines(all);
            if (all.getSize() == 0) {
                cout << "  Chua co phieu phat nao.\n";
            } else {
                cout << "  Tong: " << all.getSize() << " phieu phat\n";
                for (int i = 0; i < all.getSize(); i++) {
                    divider('-', 40);
                    inPhat(all[i]);
                }
            }
            pauseEnter();
        }

        else if (ch == 5) {
            header("PHIEU PHAT CHUA THANH TOAN");
            List<Fine> unpaid = app.getUnpaidFines();
            if (unpaid.getSize() == 0) {
                cout << "  Khong co phieu phat chua thanh toan.\n";
            } else {
                double total = 0;
                for (int i = 0; i < unpaid.getSize(); i++) {
                    divider('-', 40);
                    inPhat(unpaid[i]);
                    total += unpaid[i].tongTienPhat;
                }
                divider();
                cout << fixed << setprecision(0)
                     << "  TONG NO: " << total << " VND\n";
            }
            pauseEnter();
        }
    }
}

// ==================== MENU THỐNG KÊ ====================

void menuThongKe(LogicApp& app) {
    header("THONG KE BAO CAO");
    string hom_nay = ngayHomNay();
    app.updateAllStatus(hom_nay);

    cout << "\n";
    divider('=', 40);
    cout << "  TONG QUAN HE THONG\n";
    divider('=', 40);
    cout << "  Ngay hien tai  : " << hom_nay               << "\n"
         << "  Tong so sach   : " << app.totalBooks()        << " dau sach\n"
         << "  Tong doc gia   : " << app.totalReaders()      << " nguoi\n"
         << "  Phieu muon     : " << app.totalBorrowRecords() << " phieu\n"
         << "  Dang muon      : " << app.totalBorrowing()     << " phieu\n"
         << "  Qua han        : " << app.totalOverdue()       << " phieu\n"
         << "  Phieu phat     : " << app.totalFines()         << " phieu\n"
         << fixed << setprecision(0)
         << "  No phat chua thu: " << app.totalUnpaidFineAmount() << " VND\n";
    divider('=', 40);

    pauseEnter();
}

// ==================== MAIN MENU ====================

int main() {
    LogicApp app;

    // Dữ liệu mẫu để test
    {
        Book b1; b1.maSach="S001"; b1.tenSach="Lap Trinh C++"; b1.tacGia="Nguyen Van A";
        b1.theLoai="CNTT"; b1.nhaXuatBan="NXB KHKT"; b1.soLuong=5; b1.trangThai=BookCondition::NEW;
        app.addBook(b1);

        Book b2; b2.maSach="S002"; b2.tenSach="Co So Du Lieu"; b2.tacGia="Tran Thi B";
        b2.theLoai="CNTT"; b2.nhaXuatBan="NXB GD"; b2.soLuong=3; b2.trangThai=BookCondition::USED;
        app.addBook(b2);

        Reader r1; r1.maBanDoc="BD001"; r1.hoTen="Le Van C"; r1.ngaySinh="01/01/2000";
        r1.gioiTinh=Gender::MALE; r1.diaChi="Ha Noi"; r1.soDienThoai="0901234567";
        app.addReader(r1);

        Reader r2; r2.maBanDoc="BD002"; r2.hoTen="Pham Thi D"; r2.ngaySinh="15/05/1999";
        r2.gioiTinh=Gender::FEMALE; r2.diaChi="HCM"; r2.soDienThoai="0912345678";
        app.addReader(r2);
    }

    while (true) {
        header("HE THONG QUAN LY THU VIEN");
        cout << "  Ngay: " << ngayHomNay() << "\n\n"
             << "  [1] Quan ly Sach\n"
             << "  [2] Quan ly Doc gia\n"
             << "  [3] Muon / Tra sach\n"
             << "  [4] Quan ly Phat\n"
             << "  [5] Thong ke bao cao\n"
             << "  [0] Thoat\n";
        divider();
        int ch = nhapSoNguyen("Chon: ", 0, 5);

        if      (ch == 0) { cout << "\n  Tam biet!\n\n"; break; }
        else if (ch == 1) menuSach(app);
        else if (ch == 2) menuDocGia(app);
        else if (ch == 3) menuMuonTra(app);
        else if (ch == 4) menuPhat(app);
        else if (ch == 5) menuThongKe(app);
    }

    return 0;
}
