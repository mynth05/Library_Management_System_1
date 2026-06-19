/*
 * ui/manage_borrow_return_tab.cpp
 * Tab Mượn / Trả sách
 * Sử dụng: List<Book>, HashTable<Reader>, List<TrackBook>, PriorityQueue<Fine>
 */

#pragma once
#include "widgets.cpp"
#include "../models.cpp"
#include "../custom_structures.cpp"
#include <ctime>

// ============================================================
//  Cấu hình phạt theo loại độc giả
//  Sinh viên: mượn tối đa 3 quyển, 14 ngày, phạt 2000đ/ngày
//  Giảng viên: mượn tối đa 5 quyển, 30 ngày, phạt 1000đ/ngày
// ============================================================
static int maxBorrowDays(ReaderType t) { return (t == READER_TEACHER) ? 30 : 14; }
static int maxBorrowBooks(ReaderType t){ return (t == READER_TEACHER) ? 5  : 3;  }
static double finePerDay(ReaderType t) { return (t == READER_TEACHER) ? 1000.0 : 2000.0; }

// ============================================================
//  Lấy ngày hiện tại (số giây từ epoch)
// ============================================================
static time_t today() { return time(nullptr); }

static int daysDiff(time_t from, time_t to) {
    return (int)difftime(to, from) / 86400;
}

// ============================================================
//  In danh sách phiếu mượn
// ============================================================
static void printTrackTableHeader() {
    cout << "  " << left
         << setw(10) << "Ma phieu"
         << setw(10) << "Ma sach"
         << setw(10) << "Ma DG"
         << setw(14) << "Ngay muon"
         << setw(14) << "Han tra"
         << setw(10) << "Trang thai"
         << "\n";
    cout << "  " << string(68, '-') << "\n";
}

static string timeStr(time_t t) {
    char buf[12];
    strftime(buf, sizeof(buf), "%d/%m/%Y", localtime(&t));
    return string(buf);
}

static void printTrackRow(const TrackBook& tb) {
    cout << "  " << left
         << setw(10) << tb.track_id
         << setw(10) << tb.book_id
         << setw(10) << tb.reader_id
         << setw(14) << timeStr(tb.borrow_date)
         << setw(14) << timeStr(tb.due_date)
         << setw(10) << (tb.is_returned ? "Da tra" : "Dang muon")
         << "\n";
}

// ============================================================
//  Mượn sách
// ============================================================
void borrowBook(List<Book>& books,
                HashTable<Reader>& readers,
                List<TrackBook>& tracks)
{
    printTableHeader("MUON SACH");
    string reader_id = inputLine("Ma doc gia : ");
    if (!readers.contains(reader_id)) { showError("Khong tim thay doc gia!"); return; }

    Reader& r = readers.getRef(reader_id);
    if (r.borrow_count >= maxBorrowBooks(r.type)) {
        showError("Doc gia da muon toi da " + to_string(maxBorrowBooks(r.type)) + " quyen!");
        return;
    }

    string book_id = inputLine("Ma sach    : ");
    Book* bk = nullptr;
    for (int i = 0; i < books.size(); i++) {
        if (books.get(i).id == book_id) { bk = &books.get(i); break; }
    }
    if (!bk) { showError("Khong tim thay sach!"); return; }
    if (bk->available == 0) { showError("Sach hien khong con ban sao nao!"); return; }

    // Tạo phiếu mượn
    TrackBook tb;
    tb.track_id   = "TB" + to_string(tracks.size() + 1);
    tb.book_id    = book_id;
    tb.reader_id  = reader_id;
    tb.borrow_date = today();
    tb.due_date   = today() + maxBorrowDays(r.type) * 86400LL;
    tb.is_returned = false;

    tracks.push_back(tb);
    bk->available--;
    r.borrow_count++;

    cout << "\n  [OK] Muon thanh cong!\n";
    cout << "  Ma phieu: " << tb.track_id
         << "  |  Han tra: " << timeStr(tb.due_date) << "\n";
}

// ============================================================
//  Trả sách (tự động tính phạt nếu trễ hạn)
// ============================================================
void returnBook(List<Book>& books,
                HashTable<Reader>& readers,
                List<TrackBook>& tracks,
                PriorityQueue<Fine>& fines)
{
    printTableHeader("TRA SACH");
    string track_id = inputLine("Ma phieu muon: ");

    for (int i = 0; i < tracks.size(); i++) {
        TrackBook& tb = tracks.get(i);
        if (tb.track_id == track_id) {
            if (tb.is_returned) { showError("Phieu nay da duoc tra truoc do!"); return; }

            tb.is_returned = true;
            time_t return_date = today();

            // Cập nhật sách
            for (int j = 0; j < books.size(); j++) {
                if (books.get(j).id == tb.book_id) { books.get(j).available++; break; }
            }

            // Cập nhật độc giả
            Reader& r = readers.getRef(tb.reader_id);
            r.borrow_count--;

            // Tính phạt
            int days_late = daysDiff(tb.due_date, return_date);
            if (days_late > 0) {
                Fine f;
                f.track_id   = track_id;
                f.reader_id  = tb.reader_id;
                f.book_id    = tb.book_id;
                f.days_late  = days_late;
                f.amount     = days_late * finePerDay(r.type);
                f.is_paid    = false;
                fines.push(f);

                cout << "\n  [!] TRA TRE " << days_late << " NGAY!\n";
                cout << "      Tien phat: " << f.amount << " VND\n";
                cout << "      (Da them vao hang doi xu ly phat)\n";
            } else {
                cout << "\n  [OK] Tra sach thanh cong. Khong co phat.\n";
            }
            return;
        }
    }
    showError("Khong tim thay phieu muon: " + track_id);
}

// ============================================================
//  Xem tất cả phiếu mượn
// ============================================================
void showAllTracks(List<TrackBook>& tracks) {
    printTableHeader("LICH SU MUON / TRA SACH");
    if (tracks.isEmpty()) { showError("Chua co giao dich nao!"); return; }
    printTrackTableHeader();
    for (int i = 0; i < tracks.size(); i++)
        printTrackRow(tracks.get(i));
}

// ============================================================
//  Xem phiếu mượn đang hoạt động (chưa trả)
// ============================================================
void showActiveBorrows(List<TrackBook>& tracks) {
    printTableHeader("SACH DANG DUOC MUON");
    bool any = false;
    printTrackTableHeader();
    for (int i = 0; i < tracks.size(); i++) {
        if (!tracks.get(i).is_returned) {
            printTrackRow(tracks.get(i));
            any = true;
        }
    }
    if (!any) showError("Khong co sach nao dang duoc muon!");
}

// ============================================================
//  Menu chính tab Mượn/Trả
// ============================================================
void borrowReturnMenu(List<Book>& books,
                      HashTable<Reader>& readers,
                      List<TrackBook>& tracks,
                      PriorityQueue<Fine>& fines)
{
    int choice;
    do {
        system("cls");
        cout << "============================================================\n";
        cout << "              QUAN LY MUON / TRA SACH\n";
        cout << "============================================================\n";
        cout << "\n";
        cout << "  [1]  Muon sach\n";
        cout << "  [2]  Tra sach\n";
        cout << "  [3]  Lich su muon/tra\n";
        cout << "  [4]  Sach dang duoc muon\n";
        cout << "  [0]  Quay lai\n";
        cout << "\n  Lua chon: ";
        cin >> choice;
        cin.ignore();

        switch (choice) {
            case 1: borrowBook(books, readers, tracks);               pause(); break;
            case 2: returnBook(books, readers, tracks, fines);        pause(); break;
            case 3: showAllTracks(tracks);                            pause(); break;
            case 4: showActiveBorrows(tracks);                        pause(); break;
            case 0: break;
            default: showError("Lua chon khong hop le!"); pause(); break;
        }
    } while (choice != 0);
}
