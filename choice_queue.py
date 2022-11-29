class Queue:
    """Default queue class."""

    def __init__(self, values: list):
        self.queue = values
        self.max_n = len(values)
        self.head = 0
        self.tail = len(values)
        self.size = len(values)

    def is_empty(self):
        return self.size == 0

    def push(self, x):
        if self.size == self.max_n:
            raise IndexError('Queue is full')
        self.queue[self.head - 1] = x
        self.head = (self.head - 1) % self.max_n
        self.size += 1

    def pop(self):
        if self.is_empty():
            raise IndexError('Queue is empty')
        x = self.queue[self.tail - 1]
        self.queue[self.tail - 1] = None
        self.tail = (self.tail - 1) % self.max_n
        self.size -= 1
        return x

    def __str__(self):
        return ' '.join(map(str, self.queue))
