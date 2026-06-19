"""Các cấu trúc dữ liệu và thuật toán cốt lõi tự cài đặt.

Module không dùng trạng thái toàn cục có thể thay đổi. Mỗi cấu trúc quản lý
dữ liệu nội bộ của chính nó và báo lỗi bằng ngoại lệ khi thao tác không hợp lệ.
"""


class HashNode:
    """Nút liên kết dùng để xử lý xung đột trong một bucket bảng băm."""

    def __init__(self, key, value):
        """Khởi tạo nút với khóa, giá trị và liên kết kế tiếp rỗng."""
        self.key = key
        self.value = value
        self.next = None

    def __repr__(self):
        return f"HashNode({self.key!r}: {self.value!r})"


class HashTable:
    """Bảng băm chuỗi liên kết, tự tăng gấp đôi khi tải đạt 0.75."""

    DEFAULT_CAPACITY = 64
    LOAD_FACTOR_THRESHOLD = 0.75

    def __init__(self, capacity: int = DEFAULT_CAPACITY):
        """Tạo bảng rỗng với số bucket ban đầu là ``capacity``."""
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * self.capacity

    def _hash(self, key) -> int:
        """Tính hash bằng polynomial rolling hash."""
        h = 0
        for ch in str(key):
            h = (h * 31 + ord(ch)) % self.capacity
        return h

    def put(self, key, value) -> None:
        """Thêm hoặc cập nhật một cặp key-value."""
        if self.size / self.capacity >= self.LOAD_FACTOR_THRESHOLD:
            self._resize()

        idx = self._hash(key)
        node = self.buckets[idx]

        while node:
            if node.key == key:
                node.value = value
                return
            node = node.next

        new_node = HashNode(key, value)
        new_node.next = self.buckets[idx]
        self.buckets[idx] = new_node
        self.size += 1

    def get(self, key, default=None):
        """Trả về giá trị theo key, hoặc default nếu không tìm thấy."""
        idx = self._hash(key)
        node = self.buckets[idx]
        while node:
            if node.key == key:
                return node.value
            node = node.next
        return default

    def remove(self, key) -> bool:
        """Xóa một cặp key-value."""
        idx = self._hash(key)
        node = self.buckets[idx]
        prev = None

        while node:
            if node.key == key:
                if prev:
                    prev.next = node.next
                else:
                    self.buckets[idx] = node.next
                self.size -= 1
                return True
            prev = node
            node = node.next
        return False

    def contains(self, key) -> bool:
        """Kiểm tra key có tồn tại hay không."""
        idx = self._hash(key)
        node = self.buckets[idx]
        while node:
            if node.key == key:
                return True
            node = node.next
        return False

    def keys(self):
        """Trả về tất cả key."""
        result = List()
        for bucket in self.buckets:
            node = bucket
            while node:
                result.append(node.key)
                node = node.next
        return result

    def values(self):
        """Trả về tất cả value."""
        result = List()
        for bucket in self.buckets:
            node = bucket
            while node:
                result.append(node.value)
                node = node.next
        return result

    def items(self):
        """Trả về tất cả cặp (key, value)."""
        result = List()
        for bucket in self.buckets:
            node = bucket
            while node:
                result.append((node.key, node.value))
                node = node.next
        return result

    def _resize(self) -> None:
        """Tăng gấp đôi dung lượng và hash lại dữ liệu."""
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0

        for bucket in old_buckets:
            node = bucket
            while node:
                node = node.next
                self.put(node.key, node.value)
                node = node.next

    def __len__(self):
        return self.size

    def __getitem__(self, key):
        value = self.get(key)
        if value is None and not self.contains(key):
            raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        self.put(key, value)

    def __contains__(self, key):
        return self.contains(key)

    def __iter__(self):
        for key in self.keys():
            yield key

    def __repr__(self):
        return f"HashTable(size={self.size}, capacity={self.capacity})"


class List:
    """Mảng động hỗ trợ truy cập chỉ mục và tự tăng/giảm dung lượng."""

    _MIN_CAPACITY = 8

    def __init__(self, initial_capacity: int = _MIN_CAPACITY):
        """Tạo danh sách rỗng với dung lượng tối thiểu là 8."""
        self._capacity = max(int(initial_capacity), self._MIN_CAPACITY)
        self._size = 0
        self._elements = [None] * self._capacity

    def append(self, item) -> None:
        """Thêm phần tử vào cuối danh sách."""
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        self._elements[self._size] = item
        self._size += 1

    def extend(self, items) -> None:
        """Thêm lần lượt mọi phần tử từ một iterable vào cuối danh sách."""
        for item in items:
            self.append(item)

    def get(self, index):
        """Lấy phần tử tại chỉ mục, hỗ trợ chỉ mục âm."""
        index = self._normalize_existing_index(index)
        return self._elements[index]

    def set(self, index, item) -> None:
        """Đặt giá trị phần tử tại chỉ mục, hỗ trợ chỉ mục âm."""
        index = self._normalize_existing_index(index)
        self._elements[index] = item

    def insert(self, index, item) -> None:
        """Chèn phần tử vào chỉ mục."""
        if index < 0:
            index = max(0, index + self._size)
        if not (0 <= index <= self._size):
            raise IndexError("List: Chỉ mục chèn ngoài phạm vi")

        if self._size == self._capacity:
            self._resize(self._capacity * 2)

        for i in range(self._size, index, -1):
            self._elements[i] = self._elements[i - 1]
        self._elements[index] = item
        self._size += 1

    def pop(self, index=-1):
        """Xóa và trả về phần tử tại chỉ mục, mặc định là cuối danh sách."""
        if self.is_empty():
            raise IndexError("List: Pop từ danh sách rỗng")

        index = self._normalize_existing_index(index)
        item = self._elements[index]
        for i in range(index, self._size - 1):
            self._elements[i] = self._elements[i + 1]
        self._size -= 1
        self._elements[self._size] = None

        if self._size < self._capacity // 4 and self._capacity // 2 >= self._MIN_CAPACITY:
            self._resize(self._capacity // 2)

        return item

    def is_empty(self) -> bool:
        """Trả về ``True`` khi danh sách không có phần tử."""
        return self._size == 0

    def to_list(self) -> list:
        """Trả về bản sao built-in ``list`` của các phần tử đang lưu."""
        return [self._elements[i] for i in range(self._size)]

    def copy(self):
        """Trả về một ``List`` mới có cùng các phần tử."""
        copied = List(max(self._capacity, self._MIN_CAPACITY))
        copied.extend(self)
        return copied

    def _resize(self, new_capacity: int) -> None:
        """Cấp phát mảng mới và sao chép các phần tử hiện có."""
        new_capacity = max(new_capacity, self._MIN_CAPACITY)
        new_elements = [None] * new_capacity
        for i in range(self._size):
            new_elements[i] = self._elements[i]
        self._elements = new_elements
        self._capacity = new_capacity

    def _normalize_existing_index(self, index: int) -> int:
        """Chuẩn hóa chỉ mục âm và từ chối chỉ mục ngoài phạm vi."""
        if index < 0:
            index += self._size
        if not (0 <= index < self._size):
            raise IndexError("List: Chỉ mục ngoài phạm vi")
        return index

    def __len__(self):
        return self._size

    def __iter__(self):
        for i in range(self._size):
            yield self._elements[i]

    def __getitem__(self, index):
        if isinstance(index, slice):
            start, stop, step = index.indices(self._size)
            result = List()
            for i in range(start, stop, step):
                result.append(self._elements[i])
            return result
        return self.get(index)

    def __setitem__(self, index, value):
        self.set(index, value)

    def __contains__(self, item):
        for current in self:
            if current == item:
                return True
        return False

    def __add__(self, other):
        result = self.copy()
        result.extend(other)
        return result

    def __reversed__(self):
        for i in range(self._size - 1, -1, -1):
            yield self._elements[i]

    def __eq__(self, other):
        try:
            if len(self) != len(other):
                return False
            return all(self[i] == other[i] for i in range(self._size))
        except (TypeError, IndexError):
            return False

    def __repr__(self):
        return f"List({self.to_list()})"

    def __str__(self):
        if self.is_empty():
            return "List:[]"
        return "List:[" + ", ".join(str(item) for item in self) + "]"

class PriorityQueue:
    """Hàng đợi ưu tiên (Min-Heap) tự cài đặt, sử dụng cấu trúc mảng động List."""

    def __init__(self):
        """Khởi tạo một hàng đợi ưu tiên rỗng."""
        self._heap = List()  # Sử dụng class List bạn đã định nghĩa ở trên

    def push(self, priority, item) -> None:
        """Thêm một phần tử vào hàng đợi với độ ưu tiên xác định.
        
        Độ ưu tiên càng thấp (nhỏ) thì càng được ưu tiên xuất hàng trước.
        """
        # Lưu dưới dạng tuple (priority, item)
        self._heap.append((priority, item))
        self._sift_up(len(self._heap) - 1)

    def pop(self):
        """Xóa và trả về phần tử có độ ưu tiên cao nhất (nhỏ nhất).
        
        Ném ra IndexError nếu hàng đợi rỗng.
        """
        if self.is_empty():
            raise IndexError("PriorityQueue: Pop từ một hàng đợi rỗng")

        # Lưu lại item có ưu tiên cao nhất ở gốc
        root_item = self._heap.get(0)[1]
        
        # Nếu chỉ có 1 phần tử, lấy ra luôn
        if len(self._heap) == 1:
            self._heap.pop()
            return root_item

        # Đưa phần tử cuối cùng lên thay thế vị trí gốc
        last_item = self._heap.pop()
        self._heap.set(0, last_item)
        
        # Sàng phần tử gốc xuống đúng vị trí
        self._sift_down(0)
        
        return root_item

    def peek(self):
        """Trả về phần tử có độ ưu tiên cao nhất mà không xóa nó."""
        if self.is_empty():
            raise IndexError("PriorityQueue: Peek từ một hàng đợi rỗng")
        return self._heap.get(0)[1]

    def is_empty(self) -> bool:
        """Trả về True nếu hàng đợi không có phần tử nào."""
        return len(self._heap) == 0

    def _sift_up(self, index: int) -> None:
        """Đưa phần tử tại chỉ mục index lên trên cho tới khi thỏa mãn tính chất Min-Heap."""
        while index > 0:
            parent_idx = (index - 1) // 2
            if self._heap.get(index)[0] < self._heap.get(parent_idx)[0]:
                # Đổi chỗ vùng dữ liệu giữa node con và node cha
                self._swap(index, parent_idx)
                index = parent_idx
            else:
                break

    def _sift_down(self, index: int) -> None:
        """Đưa phần tử tại chỉ mục index xuống dưới cho tới khi thỏa mãn tính chất Min-Heap."""
        size = len(self._heap)
        while True:
            left_idx = 2 * index + 1
            right_idx = 2 * index + 2
            smallest_idx = index

            if left_idx < size and self._heap.get(left_idx)[0] < self._heap.get(smallest_idx)[0]:
                smallest_idx = left_idx
            if right_idx < size and self._heap.get(right_idx)[0] < self._heap.get(smallest_idx)[0]:
                smallest_idx = right_idx

            if smallest_idx != index:
                self._swap(index, smallest_idx)
                index = smallest_idx
            else:
                break

    def _swap(self, i: int, j: int) -> None:
        """Đổi chỗ hai phần tử tại chỉ mục i và j trong cặp heap."""
        temp = self._heap.get(i)
        self._heap.set(i, self._heap.get(j))
        self._heap.set(j, temp)

    def __len__(self):
        return len(self._heap)

    def __repr__(self):
        return f"PriorityQueue(size={len(self._heap)})"
