/*
 * ui/manage_reader_tab.cpp
 * Tab quản lý Độc giả: thêm, xoá, tìm kiếm, hiển thị
 * Sử dụng: HashTable<Reader>
 */

#pragma once
#include "widgets.cpp"
#include "../models.cpp"
#include "../custom_structures.cpp"

// ============================================================
//  In 1 dòng độc giả
// ============================================================
static string readerTypeStr(ReaderType t) {
    switch (t) {
        case READER_STUDENT: return "Sinh vien";
        case READER_TEACHER: return "Giang vien";
        default:             return "Khac";
    }
}

static void printReaderRow(int idx, const Reader& r) {
    cout << "  " << left
         << setw(4)  << idx
         << setw(10) << r.id
         << setw(25) << r.name
         << setw(14) << readerTypeStr(r.type)
         << setw(8)  << r.borrow_count
         << "\n";
}

static void printReaderTableHeader() {
    cout << "  " << left
         << setw(4)  << "STT"
         << setw(10) << "Ma DG"
         << setw(25) << "Ho ten"
         << setw(14) << "Loai"
         << setw(8)  << "Dang muon"
         << "\n";
    cout << "  " << string(61, '-') << "\n";
}

// ============================================================
//  CRUD
// ============================================================
void showAllReaders(HashTable<Reader>& readers) {
    printTableHeader("DANH SACH DOC GIA");
    List<Reader> all = readers.getAllValues();
    if (all.isEmpty()) { showError("Chua co doc gia nao!"); return; }
    printReaderTableHeader();
    for (int i = 0; i < all.size(); i++)
        printReaderRow(i + 1, all.get(i));
}

void addReader(HashTable<Reader>& readers) {
    printTableHeader("THEM DOC GIA MOI");
    Reader r;
    r.id = inputLine("Ma doc gia  : ");
    if (readers.contains(r.id)) { showError("Ma doc gia da ton tai!"); return; }
    r.name        = inputLine("Ho ten      : ");
    cout << "  Loai doc gia (1=Sinh vien / 2=Giang vien): ";
    int t; cin >> t; cin.ignore();
    r.type        = (t == 2) ? READER_TEACHER : READER_STUDENT;
    r.borrow_count = 0;

    readers.insert(r.id, r);
    showSuccess("Da them doc gia: " + r.name);
}

void searchReader(HashTable<Reader>& readers) {
    printTableHeader("TIM KIEM DOC GIA");
    string kw = inputLine("Nhap ma / ho ten: ");
    List<Reader> all = readers.getAllValues();
    bool found = false;
    printReaderTableHeader();
    for (int i = 0; i < all.size(); i++) {
        Reader& r = all.get(i);
        if (r.id.find(kw) != string::npos || r.name.find(kw) != string::npos) {
            printReaderRow(i + 1, r);
            found = true;
        }
    }
    if (!found) showError("Khong tim thay doc gia phu hop!");
}

void deleteReader(HashTable<Reader>& readers) {
    printTableHeader("XOA DOC GIA");
    string id = inputLine("Nhap ma doc gia: ");
    if (!readers.contains(id)) { showError("Khong tim thay doc gia!"); return; }
    Reader r = readers.get(id);
    if (r.borrow_count > 0) { showError("Doc gia dang muon sach, khong the xoa!"); return; }
    if (confirm("Xac nhan xoa \"" + r.name + "\"?")) {
        readers.remove(id);
        showSuccess("Da xoa doc gia!");
    }
}

// ============================================================
//  Menu chính của tab Độc giả
// ============================================================
void readerMenu(HashTable<Reader>& readers) {
    int choice;
    do {
        system("cls");
        cout << "============================================================\n";
        cout << "              QUAN LY DOC GIA\n";
        cout << "============================================================\n";
        cout << "\n";
        cout << "  [1]  Hien thi tat ca doc gia\n";
        cout << "  [2]  Them doc gia moi\n";
        cout << "  [3]  Tim kiem doc gia\n";
        cout << "  [4]  Xoa doc gia\n";
        cout << "  [0]  Quay lai menu chinh\n";
        cout << "\n  Lua chon: ";
        cin >> choice;
        cin.ignore();

        switch (choice) {
            case 1: showAllReaders(readers); pause(); break;
            case 2: addReader(readers);      pause(); break;
            case 3: searchReader(readers);   pause(); break;
            case 4: deleteReader(readers);   pause(); break;
            case 0: break;
            default: showError("Lua chon khong hop le!"); pause(); break;
        }
    } while (choice != 0);
}
