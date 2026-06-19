class List:
    def __init__(self):
        self.capacity = 4
        self.size = 0
        self.data = [None] * self.capacity

    def _resize(self):
        new_capacity = 4 if self.capacity == 0 else self.capacity * 2
        new_data = [None] * new_capacity
        for i in range(self.size):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_capacity

    def pushBack(self, value):
        if self.size == self.capacity:
            self._resize()
        self.data[self.size] = value
        self.size += 1

    def popBack(self):
        if self.size > 0:
            self.size -= 1
            self.data[self.size] = None

    def remove(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        for i in range(index, self.size - 1):
            self.data[i] = self.data[i + 1]
        self.size -= 1
        self.data[self.size] = None

    def __getitem__(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        return self.data[index]

    def __setitem__(self, index, value):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        self.data[index] = value

    def getSize(self):
        return self.size

    def getCapacity(self):
        return self.capacity

    def clear(self):
        self.size = 0
        self.data = [None] * self.capacity

    def print(self):
        elements = [str(self.data[i]) for i in range(self.size)]
        print("[" + ", ".join(elements) + "]")

class Entry:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashTable:
    def __init__(self, capacity=16):
        self.capacity = capacity
        self.liveCount = 0
        self.buckets = [List() for _ in range(self.capacity)]

    def _hash(self, key, capacity=None):
        if capacity is None:
            capacity = self.capacity
        h = 5381
        for c in key:
            h = (((h << 5) + h) + ord(c)) & 0xFFFFFFFF
        return h % capacity

    def _rehash(self):
        new_capacity = self.capacity * 2
        new_buckets = [List() for _ in range(new_capacity)]
        
        for i in range(self.capacity):
            bucket = self.buckets[i]
            for j in range(bucket.getSize()):
                entry = bucket[j]
                index = self._hash(entry.key, new_capacity)
                new_buckets[index].pushBack(entry)
                
        self.buckets = new_buckets
        self.capacity = new_capacity

    def insert(self, key, value):
        if (self.liveCount + 1) / self.capacity > 0.75:
            self._rehash()
            
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for i in range(bucket.getSize()):
            if bucket[i].key == key:
                bucket[i].value = value
                return
                
        bucket.pushBack(Entry(key, value))
        self.liveCount += 1

    def get(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]
        for i in range(bucket.getSize()):
            if bucket[i].key == key:
                return bucket[i].value
        return None

    def remove(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]
        for i in range(bucket.getSize()):
            if bucket[i].key == key:
                bucket.remove(i)
                self.liveCount -= 1
                return True
        return False

    def forEach(self, callback):
        for i in range(self.capacity):
            bucket = self.buckets[i]
            for j in range(bucket.getSize()):
                callback(bucket[j].key, bucket[j].value)

    def getSize(self):
        return self.liveCount

class PriorityQueue:
    def __init__(self):
        self.data = List()

    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * i + 2

    def _heapifyUp(self, i):
        while i > 0 and self.data[self._parent(i)] < self.data[i]:
            p = self._parent(i)
            self.data[p], self.data[i] = self.data[i], self.data[p]
            i = p

    def _heapifyDown(self, i):
        n = self.data.getSize()
        while True:
            largest = i
            l = self._left(i)
            r = self._right(i)
            
            if l < n and self.data[largest] < self.data[l]:
                largest = l
            if r < n and self.data[largest] < self.data[r]:
                largest = r
                
            if largest == i:
                break
                
            self.data[i], self.data[largest] = self.data[largest], self.data[i]
            i = largest

    def push(self, val):
        self.data.pushBack(val)
        self._heapifyUp(self.data.getSize() - 1)

    def top(self):
        if self.isEmpty():
            raise RuntimeError("PriorityQueue rong!")
        return self.data[0]

    def pop(self):
        if self.isEmpty():
            return
        self.data[0] = self.data[self.data.getSize() - 1]
        self.data.popBack()
        if not self.isEmpty():
            self._heapifyDown(0)

    def empty(self):
        return self.data.getSize() == 0

    def isEmpty(self):
        return self.data.getSize() == 0

    def getSize(self):
        return self.data.getSize()
