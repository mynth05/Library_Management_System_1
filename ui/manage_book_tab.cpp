/*
 * ui/manage_book_tab.cpp
 * Tab quản lý Sách: thêm, xoá, tìm kiếm, hiển thị danh sách
 * Sử dụng: List<Book>
 */

#pragma once
#include "widgets.cpp"
#include "../models.cpp"
#include "../custom_structures.cpp"

// ============================================================
//  Hiển thị 1 dòng sách trong bảng
// ============================================================
static void printBookRow(int idx, const Book& b) {
    cout << "  " << left
         << setw(4)  << idx
         << setw(10) << b.id
         << setw(30) << b.title
         << setw(20) << b.author
         << setw(6)  << b.quantity
         << setw(6)  << b.available
         << "\n";
}

static void printBookTableHeader() {
    cout << "  " << left
         << setw(4)  << "STT"
         << setw(10) << "Ma sach"
         << setw(30) << "Tua de"
         << setw(20) << "Tac gia"
         << setw(6)  << "So luong"
         << setw(6)  << "Con lai"
         << "\n";
    cout << "  " << string(76, '-') << "\n";
}

// ============================================================
//  Các chức năng CRUD
// ============================================================
void showAllBooks(List<Book>& books) {
    printTableHeader("DANH SACH SACH");
    if (books.isEmpty()) { showError("Chua co sach nao trong he thong!"); return; }
    printBookTableHeader();
    for (int i = 0; i < books.size(); i++)
        printBookRow(i + 1, books.get(i));
}

void addBook(List<Book>& books) {
    printTableHeader("THEM SACH MOI");
    Book b;
    b.id        = inputLine("Ma sach     : ");
    // Kiểm tra trùng ID
    for (int i = 0; i < books.size(); i++) {
        if (books.get(i).id == b.id) { showError("Ma sach da ton tai!"); return; }
    }
    b.title     = inputLine("Tua de      : ");
    b.author    = inputLine("Tac gia     : ");
    b.quantity  = inputInt ("So luong    : ");
    b.available = b.quantity;

    books.push_back(b);
    showSuccess("Da them sach: " + b.title);
}

void searchBook(List<Book>& books) {
    printTableHeader("TIM KIEM SACH");
    string kw = inputLine("Nhap tu khoa (ma / tua de / tac gia): ");
    bool found = false;
    printBookTableHeader();
    for (int i = 0; i < books.size(); i++) {
        Book& b = books.get(i);
        if (b.id.find(kw)     != string::npos ||
            b.title.find(kw)  != string::npos ||
            b.author.find(kw) != string::npos) {
            printBookRow(i + 1, b);
            found = true;
        }
    }
    if (!found) showError("Khong tim thay sach phu hop!");
}

void deleteBook(List<Book>& books) {
    printTableHeader("XOA SACH");
    string id = inputLine("Nhap ma sach can xoa: ");
    for (int i = 0; i < books.size(); i++) {
        if (books.get(i).id == id) {
            if (books.get(i).available != books.get(i).quantity) {
                showError("Sach dang duoc muon, khong the xoa!");
                return;
            }
            if (confirm("Xac nhan xoa sach \"" + books.get(i).title + "\"?")) {
                books.remove(i);
                showSuccess("Da xoa sach!");
            }
            return;
        }
    }
    showError("Khong tim thay sach voi ma: " + id);
}

void updateBook(List<Book>& books) {
    printTableHeader("CAP NHAT SACH");
    string id = inputLine("Nhap ma sach can cap nhat: ");
    for (int i = 0; i < books.size(); i++) {
        Book& b = books.get(i);
        if (b.id == id) {
            cout << "  (Enter de giu nguyen gia tri cu)\n";
            string tmp;
            tmp = inputLine("Tua de moi [" + b.title + "]: ");
            if (!tmp.empty()) b.title = tmp;
            tmp = inputLine("Tac gia moi [" + b.author + "]: ");
            if (!tmp.empty()) b.author = tmp;
            showSuccess("Da cap nhat sach!");
            return;
        }
    }
    showError("Khong tim thay sach voi ma: " + id);
}

// ============================================================
//  Menu chính của tab Sách
// ============================================================
void bookMenu(List<Book>& books) {
    int choice;
    do {
        system("cls");  // hoặc "clear" trên Linux
        cout << "============================================================\n";
        cout << "              QUAN LY SACH\n";
        cout << "============================================================\n";
        cout << "\n";
        cout << "  [1]  Hien thi tat ca sach\n";
        cout << "  [2]  Them sach moi\n";
        cout << "  [3]  Tim kiem sach\n";
        cout << "  [4]  Cap nhat sach\n";
        cout << "  [5]  Xoa sach\n";
        cout << "  [0]  Quay lai menu chinh\n";
        cout << "\n  Lua chon: ";
        cin >> choice;
        cin.ignore();

        switch (choice) {
            case 1: showAllBooks(books); pause(); break;
            case 2: addBook(books);      pause(); break;
            case 3: searchBook(books);   pause(); break;
            case 4: updateBook(books);   pause(); break;
            case 5: deleteBook(books);   pause(); break;
            case 0: break;
            default: showError("Lua chon khong hop le!"); pause(); break;
        }
    } while (choice != 0);
}
