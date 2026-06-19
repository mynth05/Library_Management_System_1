/*
 * ui/widgets.cpp
 * Các widget/helper dùng chung cho toàn bộ UI
 */

#pragma once
#include <iostream>
#include <string>
#include <iomanip>
#include <limits>
using namespace std;

// ============================================================
//  In tiêu đề bảng
// ============================================================
void printTableHeader(const string& title) {
    int width = 60;
    cout << "\n  " << string(width, '=') << "\n";
    int pad = (width - (int)title.size()) / 2;
    cout << "  " << string(pad, ' ') << title << "\n";
    cout << "  " << string(width, '=') << "\n";
}

// ============================================================
//  Nhập chuỗi có khoảng trắng
// ============================================================
string inputLine(const string& prompt) {
    cout << "  " << prompt;
    string s;
    getline(cin, s);
    return s;
}

// ============================================================
//  Nhập số nguyên với kiểm tra
// ============================================================
int inputInt(const string& prompt) {
    int val;
    while (true) {
        cout << "  " << prompt;
        if (cin >> val) {
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            return val;
        }
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        cout << "  [!] Vui long nhap so nguyen!\n";
    }
}

// ============================================================
//  Xác nhận Y/N
// ============================================================
bool confirm(const string& msg) {
    cout << "  " << msg << " (y/n): ";
    char c; cin >> c; cin.ignore();
    return (c == 'y' || c == 'Y');
}

// ============================================================
//  Thông báo thành công / lỗi
// ============================================================
void showSuccess(const string& msg) {
    cout << "\n  [OK] " << msg << "\n";
}

void showError(const string& msg) {
    cout << "\n  [!] " << msg << "\n";
}

void pause() {
    cout << "\n  Nhan Enter de tiep tuc...";
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    cin.get();
}
