import sys
import heapq


class HalfDifference:
    def __init__(self):
        self.low = []   # max-heap via negatives: smaller half
        self.high = []  # min-heap: larger half
        self.sum_low = 0
        self.sum_high = 0

    def add(self, x):
        if not self.high or x >= self.high[0]:
            heapq.heappush(self.high, x)
            self.sum_high += x
        else:
            heapq.heappush(self.low, -x)
            self.sum_low += x

        target_low = (len(self.low) + len(self.high)) // 2

        while len(self.low) > target_low:
            v = -heapq.heappop(self.low)
            self.sum_low -= v
            heapq.heappush(self.high, v)
            self.sum_high += v

        while len(self.low) < target_low:
            v = heapq.heappop(self.high)
            self.sum_high -= v
            heapq.heappush(self.low, -v)
            self.sum_low += v

    def value(self):
        return self.sum_high - self.sum_low


def main():
    input = sys.stdin.buffer.readline
    n = int(input())
    a = list(map(int, input().split()))

    if n % 2 == 0:
        a.sort()
        k = n // 2
        print(sum(a[k:]) - sum(a[:k]))
        return

    # pref[i] = best score for a[0:i], when i is even.
    pref = [0] * (n + 1)
    ds = HalfDifference()
    for i, x in enumerate(a, 1):
        ds.add(x)
        if i % 2 == 0:
            pref[i] = ds.value()

    # suf[i] = best score for a[i:n], when its length is even.
    suf = [0] * (n + 1)
    ds = HalfDifference()
    for i in range(n - 1, -1, -1):
        ds.add(a[i])
        if (n - i) % 2 == 0:
            suf[i] = ds.value()

    ans = 0
    # The surviving element has 0-based even index, so both sides have even size.
    for survivor in range(0, n, 2):
        ans = max(ans, pref[survivor] + suf[survivor + 1])

    print(ans)


if __name__ == "__main__":
    main()