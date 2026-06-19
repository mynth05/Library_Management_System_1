/*
 * main.cpp
 * Hệ thống Quản lý Thư viện
 * Kỹ thuật lập trình - HUST
 */

#include "models.cpp"
#include "custom_structures.cpp"
#include "ui/widgets.cpp"
#include "ui/manage_book_tab.cpp"
#include "ui/manage_reader_tab.cpp"
#include "ui/manage_borrow_return_tab.cpp"
#include <iostream>
#include <string>
#include <limits>

using namespace std;

// ============================================================
//  Dữ liệu toàn cục (global state)
// ============================================================
List<Book>       g_books;
HashTable<Reader> g_readers;      // key = reader_id
List<TrackBook>  g_trackbooks;    // bản ghi mượn/trả
PriorityQueue<Fine> g_fines;      // ưu tiên theo mức phạt cao nhất

// ============================================================
//  Tiện ích console
// ============================================================
void clearScreen() {
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
}

void pause() {
    cout << "\n  Nhấn Enter để tiếp tục...";
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    cin.get();
}

void printBanner() {
    cout << "============================================================\n";
    cout << "         HE THONG QUAN LY THU VIEN - HUST\n";
    cout << "============================================================\n";
}

void printMainMenu() {
    clearScreen();
    printBanner();
    cout << "\n";
    cout << "  [1]  Quan ly Sach\n";
    cout << "  [2]  Quan ly Doc gia\n";
    cout << "  [3]  Quan ly Muon / Tra sach\n";
    cout << "  [4]  Xem / Xu ly Phat\n";
    cout << "  [0]  Thoat\n";
    cout << "\n  Lua chon: ";
}

// ============================================================
//  Tab 4: Quản lý phạt (sử dụng PriorityQueue)
// ============================================================
void fineMenu() {
    int choice;
    do {
        clearScreen();
        printBanner();
        cout << "\n  --- QUAN LY PHAT ---\n\n";
        cout << "  [1]  Hien thi danh sach phat (theo muc do)\n";
        cout << "  [2]  Xu ly phat cao nhat (pop)\n";
        cout << "  [0]  Quay lai\n";
        cout << "\n  Lua chon: ";
        cin >> choice;
        cin.ignore();

        if (choice == 1) {
            clearScreen();
            printBanner();
            cout << "\n  DANH SACH PHAT (uu tien cao -> thap):\n";
            cout << "  ----------------------------------------\n";
            // In toàn bộ hàng đợi mà không hủy
            PriorityQueue<Fine> tmp = g_fines;
            int idx = 1;
            while (!tmp.isEmpty()) {
                Fine f = tmp.top();
                tmp.pop();
                cout << "  " << idx++ << ". DocGia: " << f.reader_id
                     << "  |  Sach: " << f.book_id
                     << "  |  So ngay tre: " << f.days_late
                     << "  |  Tien phat: " << f.amount << " VND\n";
            }
            pause();
        } else if (choice == 2) {
            if (g_fines.isEmpty()) {
                cout << "\n  Khong co khoan phat nao!\n";
            } else {
                Fine f = g_fines.top();
                g_fines.pop();
                cout << "\n  Da xu ly phat: DocGia " << f.reader_id
                     << " - " << f.amount << " VND\n";
            }
            pause();
        }
    } while (choice != 0);
}

// ============================================================
//  main
// ============================================================
int main() {
    // --- Dữ liệu mẫu khởi tạo ---
    // (Có thể thay bằng load từ file)
    Book b1; b1.id = "B001"; b1.title = "Giao trinh CTDL & GT"; b1.author = "Nguyen Duc Nghia"; b1.quantity = 5; b1.available = 5;
    Book b2; b2.id = "B002"; b2.title = "Lap trinh C++ hien dai"; b2.author = "Bjarne Stroustrup"; b2.quantity = 3; b2.available = 3;
    g_books.push_back(b1);
    g_books.push_back(b2);

    Reader r1; r1.id = "R001"; r1.name = "Nguyen Van A"; r1.type = READER_STUDENT; r1.borrow_count = 0;
    Reader r2; r2.id = "R002"; r2.name = "Tran Thi B";   r2.type = READER_TEACHER; r2.borrow_count = 0;
    g_readers.insert(r1.id, r1);
    g_readers.insert(r2.id, r2);

    // --- Vòng lặp menu chính ---
    int choice;
    do {
        printMainMenu();
        cin >> choice;
        cin.ignore();

        switch (choice) {
            case 1: bookMenu(g_books);                              break;
            case 2: readerMenu(g_readers);                          break;
            case 3: borrowReturnMenu(g_books, g_readers,
                                     g_trackbooks, g_fines);        break;
            case 4: fineMenu();                                     break;
            case 0: cout << "\n  Tam biet!\n\n";                   break;
            default: cout << "\n  Lua chon khong hop le!\n"; pause(); break;
        }
    } while (choice != 0);

    return 0;
}
