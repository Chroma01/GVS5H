import sys
import heapq


class MedianTracker:
    def __init__(self):
        self.lower = []  # max-heap via negated values
        self.upper = []  # min-heap
        self.sum_lower = 0
        self.sum_upper = 0
        self.count = 0

    def add(self, x):
        if not self.lower or x <= -self.lower[0]:
            heapq.heappush(self.lower, -x)
            self.sum_lower += x
        else:
            heapq.heappush(self.upper, x)
            self.sum_upper += x

        self.count += 1
        target_lower = (self.count + 1) // 2

        while len(self.lower) > target_lower:
            x = -heapq.heappop(self.lower)
            self.sum_lower -= x
            heapq.heappush(self.upper, x)
            self.sum_upper += x

        while len(self.lower) < target_lower:
            x = heapq.heappop(self.upper)
            self.sum_upper -= x
            heapq.heappush(self.lower, -x)
            self.sum_lower += x

    def value(self):
        return self.sum_upper - self.sum_lower


def solve():
    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))

    prefix = [None] * (n + 1)
    prefix[0] = 0
    tracker = MedianTracker()

    for i, x in enumerate(a, 1):
        tracker.add(x)
        if i % 2 == 0:
            prefix[i] = tracker.value()

    suffix = [None] * (n + 1)
    suffix[n] = 0
    tracker = MedianTracker()

    count = 0
    for i in range(n - 1, -1, -1):
        tracker.add(a[i])
        count += 1
        if count % 2 == 0:
            suffix[i] = tracker.value()

    if n % 2 == 0:
        print(prefix[n])
    else:
        answer = 0
        for unmatched in range(0, n, 2):
            answer = max(answer, prefix[unmatched] + suffix[unmatched + 1])
        print(answer)


if __name__ == "__main__":
    solve()