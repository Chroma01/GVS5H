import sys
import heapq


class HalfDifference:
    """
    Maintains:
      sum(largest floor(m/2) elements) - sum(smallest floor(m/2) elements)
    for all inserted m elements when m is even.
    """
    def __init__(self):
        self.low = []   # max-heap via negatives: smallest half
        self.high = []  # min-heap: largest half (and median when size is odd)
        self.sum_low = 0
        self.sum_high = 0
        self.count = 0

    def add(self, x):
        self.count += 1

        if self.low and x <= -self.low[0]:
            heapq.heappush(self.low, -x)
            self.sum_low += x
        else:
            heapq.heappush(self.high, x)
            self.sum_high += x

        target_low_size = self.count // 2

        while len(self.low) > target_low_size:
            x = -heapq.heappop(self.low)
            self.sum_low -= x
            heapq.heappush(self.high, x)
            self.sum_high += x

        while len(self.low) < target_low_size:
            x = heapq.heappop(self.high)
            self.sum_high -= x
            heapq.heappush(self.low, -x)
            self.sum_low += x

    def value(self):
        return self.sum_high - self.sum_low


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    if n % 2 == 0:
        ds = HalfDifference()
        for x in a:
            ds.add(x)
        print(ds.value())
        return

    # left[i]: optimal value for A[0:i], where i is even.
    left = [0] * (n + 1)
    ds = HalfDifference()
    for i, x in enumerate(a, 1):
        ds.add(x)
        if i % 2 == 0:
            left[i] = ds.value()

    # right[i]: optimal value for A[i-1:n], when its length is even.
    right = [0] * (n + 2)
    ds = HalfDifference()
    for pos in range(n, 0, -1):
        ds.add(a[pos - 1])
        if (n - pos + 1) % 2 == 0:
            right[pos] = ds.value()

    # The final surviving original position must be odd (1-indexed).
    ans = 0
    for survivor in range(1, n + 1, 2):
        ans = max(ans, left[survivor - 1] + right[survivor + 1])

    print(ans)


if __name__ == "__main__":
    main()