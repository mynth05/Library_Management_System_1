#pragma once

#include <iostream>
#include <string>

#include "models.cpp"

#include "custom_structures.cpp"

using namespace std;

class LogicApp {
private:
    HashTable<Book> books;
    HashTable<Reader> readers;
    HashTable<TrackBook> trackBooks;
    HashTable<Fine> fines;

public:

    // ================= BOOK =================

    void addBook(const Book& book) {
        books.insert(book.maSach, book);
    }

    bool removeBook(const string& maSach) {
        return books.remove(maSach);
    }

    Book* findBook(const string& maSach) {
        return books.get(maSach);
    }

    // ================= READER =================

    void addReader(const Reader& reader) {
        readers.insert(reader.maBanDoc, reader);
    }

    bool removeReader(const string& maBanDoc) {
        return readers.remove(maBanDoc);
    }

    Reader* findReader(const string& maBanDoc) {
        return readers.get(maBanDoc);
    }

    // ================= BORROW =================

    bool borrowBook(
        const string& maPhieu,
        const string& maSach,
        const string& maBanDoc
    ) {
        Book* book = books.get(maSach);

        if (book == nullptr)
            return false;

        if (book->soLuong <= 0)
            return false;

        Reader* reader = readers.get(maBanDoc);

        if (reader == nullptr)
            return false;

        book->soLuong--;

        TrackBook track;

        track.maPhieu = maPhieu;
        track.maSach = maSach;
        track.maBanDoc = maBanDoc;

        trackBooks.insert(maPhieu, track);

        return true;
    }

    // ================= RETURN =================

    bool returnBook(const string& maPhieu) {
        TrackBook* track = trackBooks.get(maPhieu);

        if (track == nullptr)
            return false;

        Book* book = books.get(track->maSach);

        if (book != nullptr)
            book->soLuong++;

        trackBooks.remove(maPhieu);

        return true;
    }

    // ================= FINE =================

    void addFine(const Fine& fine) {
        fines.insert(fine.maPhat, fine);
    }

    Fine* findFine(const string& maPhat) {
        return fines.get(maPhat);
    }

    bool payFine(const string& maPhat) {
        Fine* fine = fines.get(maPhat);

        if (fine == nullptr)
            return false;

        fine->daThanhToan = true;

        return true;
    }

    // ================= STATISTICS =================

    int totalBooks() {
        return books.getSize();
    }

    int totalReaders() {
        return readers.getSize();
    }

    int totalBorrowRecords() {
        return trackBooks.getSize();
    }

    int totalFines() {
        return fines.getSize();
    }
};
