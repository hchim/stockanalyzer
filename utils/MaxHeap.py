import heapq

class MaxHeap(object):


    def __init__(self, n):
        self.n = n
        self.data = []
        self.size = 0


    def add(self, val):
        """
        Add a value to the heap.

        Parameters
        ----------
        val: number or tuple
            if val is a typle, the first value of the tuple will be used by the heap.
        """
        if self.size == self.n:
            heapq.heappop(self.data)

        heapq.heappush(self.data, val)
        self.size += 1


    def add_data(self, data):
        for i in range(len(data)):
            self.add(data[i])


    def clear(self):
        self.size = 0
        self.data = []


    def heapsort(self):
        result = [heapq.heappop(self.data) for i in range(len(self.data))]
        self.clear()
        return result