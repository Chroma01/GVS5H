import sys
from heapq import heappush, heappop


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    n = data[0]
    a = data[1:]
    del data

    if n % 2 == 0:
        b = sorted(a)
        h = n // 2
        print(sum(b[h:]) - sum(b[:h]))
        return

    m = n // 2
    pref = [0] * (m + 1)

    # low: max-heap (negated) of the smaller half
    # high: min-heap of the larger half
    low = []
    high = []
    sum_low = 0
    sum_high = 0

    # Prefix scores for even lengths 2, 4, ..., n-1
    for i in range(n - 1):
        x = a[i]
        if not low or x <= -low[0]:
            heappush(low, -x)
            sum_low += x
        else:
            heappush(high, x)
            sum_high += x

        total = i + 1
        desired = (total + 1) >> 1
        l = len(low)
        if l > desired:
            v = -heappop(low)
            sum_low -= v
            heappush(high, v)
            sum_high += v
        elif l < desired:
            v = heappop(high)
            sum_high -= v
            heappush(low, -v)
            sum_low += v

        if (total & 1) == 0:
            pref[total >> 1] = sum_high - sum_low

    # Survivor is the last element: prefix length n-1, empty suffix.
    ans = pref[m]

    low.clear()
    high.clear()
    sum_low = 0
    sum_high = 0

    # Suffix scores for starts i = n-1, n-2, ..., 1.
    # When current length n-i is even, i is odd and p = i-1 is a valid survivor.
    for i in range(n - 1, 0, -1):
        x = a[i]
        if not low or x <= -low[0]:
            heappush(low, -x)
            sum_low += x
        else:
            heappush(high, x)
            sum_high += x

        total = n - i
        desired = (total + 1) >> 1
        l = len(low)
        if l > desired:
            v = -heappop(low)
            sum_low -= v
            heappush(high, v)
            sum_high += v
        elif l < desired:
            v = heappop(high)
            sum_high -= v
            heappush(low, -v)
            sum_low += v

        if (total & 1) == 0:
            p = i - 1
            val = pref[p >> 1] + (sum_high - sum_low)
            if val > ans:
                ans = val

    print(ans)


if __name__ == "__main__":
    solve()