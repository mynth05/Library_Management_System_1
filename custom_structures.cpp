#include <iostream>
#include <string>
#include <algorithm>
#include <stdexcept>
using namespace std;

// ===================== LIST =====================
template <typename T>
class List {
private:
    T* data;
    int size;
    int capacity;

    void resize() {
        int newCapacity = (capacity == 0) ? 4 : capacity * 2;
        T* newData = new T[newCapacity];

        for (int i = 0; i < size; i++)
            newData[i] = data[i];

        delete[] data;
        data = newData;
        capacity = newCapacity;
    }

public:
    List() : data(new T[4]), size(0), capacity(4) {}

    // Copy constructor
    List(const List& other)
        : data(new T[other.capacity]),
          size(other.size),
          capacity(other.capacity) {

        for (int i = 0; i < size; i++)
            data[i] = other.data[i];
    }

    // Copy assignment
    List& operator=(const List& other) {
        if (this == &other)
            return *this;

        delete[] data;

        capacity = other.capacity;
        size = other.size;
        data = new T[capacity];

        for (int i = 0; i < size; i++)
            data[i] = other.data[i];

        return *this;
    }

    // Move constructor
    List(List&& other) noexcept
        : data(other.data),
          size(other.size),
          capacity(other.capacity) {

        other.data = nullptr;
        other.size = 0;
        other.capacity = 0;
    }

    // Move assignment
    List& operator=(List&& other) noexcept {
        if (this == &other)
            return *this;

        delete[] data;

        data = other.data;
        size = other.size;
        capacity = other.capacity;

        other.data = nullptr;
        other.size = 0;
        other.capacity = 0;

        return *this;
    }

    ~List() {
        delete[] data;
    }

    void pushBack(const T& value) {
        if (size == capacity)
            resize();

        data[size++] = value;
    }

    void popBack() {
        if (size > 0)
            --size;
    }

    void remove(int idx) {
        if (idx < 0 || idx >= size)
            throw out_of_range("Index out of range");

        for (int i = idx; i < size - 1; i++)
            data[i] = data[i + 1];

        --size;
    }

    T& operator[](int idx) {
        if (idx < 0 || idx >= size)
            throw out_of_range("Index out of range");

        return data[idx];
    }

    const T& operator[](int idx) const {
        if (idx < 0 || idx >= size)
            throw out_of_range("Index out of range");

        return data[idx];
    }

    int getSize() const {
        return size;
    }

    int getCapacity() const {
        return capacity;
    }

    void print() const {
        cout << "[";

        for (int i = 0; i < size; i++) {
            cout << data[i];

            if (i < size - 1)
                cout << ", ";
        }

        cout << "]\n";
    }
};

// ===================== HASH TABLE =====================

template<typename T>
struct Entry {
    string key;
    T value;
};

template<typename T>
class HashTable {
private:
    List<Entry<T>>* buckets;
    int capacity;
    int liveCount;

    int hash(const string& key, int cap) const {
        unsigned long h = 5381;

        for (char c : key)
            h = ((h << 5) + h) + c;

        return h % cap;
    }

    int hash(const string& key) const {
        return hash(key, capacity);
    }

    void rehash() {
        int newCapacity = capacity * 2;
        List<Entry<T>>* newBuckets = new List<Entry<T>>[newCapacity];

        for (int i = 0; i < capacity; i++) {
            for (int j = 0; j < buckets[i].getSize(); j++) {
                const Entry<T>& e = buckets[i][j];
                int idx = hash(e.key, newCapacity);
                newBuckets[idx].pushBack(e);
            }
        }

        delete[] buckets;
        buckets = newBuckets;
        capacity = newCapacity;
    }

public:
    HashTable(int cap = 16)
        : capacity(cap), liveCount(0) {

        buckets = new List<Entry<T>>[capacity];
    }

    HashTable(const HashTable& other)
        : capacity(other.capacity),
          liveCount(other.liveCount) {

        buckets = new List<Entry<T>>[capacity];

        for (int i = 0; i < capacity; i++)
            buckets[i] = other.buckets[i];
    }

    HashTable& operator=(const HashTable& other) {
        if (this == &other)
            return *this;

        delete[] buckets;

        capacity = other.capacity;
        liveCount = other.liveCount;

        buckets = new List<Entry<T>>[capacity];

        for (int i = 0; i < capacity; i++)
            buckets[i] = other.buckets[i];

        return *this;
    }

    HashTable(HashTable&& other) noexcept
        : buckets(other.buckets),
          capacity(other.capacity),
          liveCount(other.liveCount) {

        other.buckets = nullptr;
        other.capacity = 0;
        other.liveCount = 0;
    }

    HashTable& operator=(HashTable&& other) noexcept {
        if (this == &other)
            return *this;

        delete[] buckets;

        buckets = other.buckets;
        capacity = other.capacity;
        liveCount = other.liveCount;

        other.buckets = nullptr;
        other.capacity = 0;
        other.liveCount = 0;

        return *this;
    }

    ~HashTable() {
        delete[] buckets;
    }

    void insert(const string& key, const T& value) {
        if ((double)(liveCount + 1) / capacity > 0.75)
            rehash();

        int idx = hash(key);

        for (int i = 0; i < buckets[idx].getSize(); i++) {
            if (buckets[idx][i].key == key) {
                buckets[idx][i].value = value;
                return;
            }
        }

        buckets[idx].pushBack({key, value});
        ++liveCount;
    }

    T* get(const string& key) {
        int idx = hash(key);

        for (int i = 0; i < buckets[idx].getSize(); i++) {
            if (buckets[idx][i].key == key)
                return &buckets[idx][i].value;
        }

        return nullptr;
    }

    const T* get(const string& key) const {
        int idx = hash(key);

        for (int i = 0; i < buckets[idx].getSize(); i++) {
            if (buckets[idx][i].key == key)
                return &buckets[idx][i].value;
        }

        return nullptr;
    }

    bool remove(const string& key) {
        int idx = hash(key);

        for (int i = 0; i < buckets[idx].getSize(); i++) {
            if (buckets[idx][i].key == key) {
                buckets[idx].remove(i);
                --liveCount;
                return true;
            }
        }

        return false;
    }

    int getSize() const {
        return liveCount;
    }
};

// ===================== PRIORITY QUEUE (max-heap) =====================

template<typename T>
class PriorityQueue {
private:
    List<T> data;

    int parent(int i) const { return (i - 1) / 2; }
    int left(int i) const { return 2 * i + 1; }
    int right(int i) const { return 2 * i + 2; }

    void heapifyUp(int i) {
        while (i > 0 && data[parent(i)] < data[i]) {
            swap(data[parent(i)], data[i]);
            i = parent(i);
        }
    }

    void heapifyDown(int i) {
        int n = data.getSize();

        while (true) {
            int largest = i;
            int l = left(i);
            int r = right(i);

            if (l < n && data[largest] < data[l])
                largest = l;

            if (r < n && data[largest] < data[r])
                largest = r;

            if (largest == i)
                break;

            swap(data[i], data[largest]);
            i = largest;
        }
    }

public:
    void push(const T& val) {
        data.pushBack(val);
        heapifyUp(data.getSize() - 1);
    }

    T top() const {
        if (empty())
            throw runtime_error("PriorityQueue rong!");

        return data[0];
    }

    void pop() {
        if (empty())
            return;

        data[0] = data[data.getSize() - 1];
        data.popBack();

        if (!empty())
            heapifyDown(0);
    }

    bool empty() const {
        return data.getSize() == 0;
    }

    bool isEmpty() const {
        return data.getSize() == 0;
    }

    int getSize() const {
        return data.getSize();
    }
};
