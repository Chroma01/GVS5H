import sys
import heapq


def prefix_values(a):
    n = len(a)
    pref = [0] * (n + 1)

    # low: max-heap (stored as negatives) of the smallest ceil(k/2) elements
    # high: min-heap of the largest floor(k/2) elements
    low = []
    high = []
    low_sum = 0
    high_sum = 0

    heappush = heapq.heappush
    heappop = heapq.heappop

    for i, x in enumerate(a, 1):
        if not low or x <= -low[0]:
            heappush(low, -x)
            low_sum += x
        else:
            heappush(high, x)
            high_sum += x

        # Rebalance so that len(low) == ceil(i/2), len(high) == floor(i/2).
        if len(low) > len(high) + 1:
            y = -heappop(low)
            low_sum -= y
            heappush(high, y)
            high_sum += y
        elif len(low) < len(high):
            y = heappop(high)
            high_sum -= y
            heappush(low, -y)
            low_sum += y

        if (i & 1) == 0:
            pref[i] = high_sum - low_sum

    return pref


def suffix_values(a):
    n = len(a)
    suff = [0] * (n + 1)

    low = []
    high = []
    low_sum = 0
    high_sum = 0

    heappush = heapq.heappush
    heappop = heapq.heappop

    for idx in range(n - 1, -1, -1):
        x = a[idx]

        if not low or x <= -low[0]:
            heappush(low, -x)
            low_sum += x
        else:
            heappush(high, x)
            high_sum += x

        if len(low) > len(high) + 1:
            y = -heappop(low)
            low_sum -= y
            heappush(high, y)
            high_sum += y
        elif len(low) < len(high):
            y = heappop(high)
            high_sum -= y
            heappush(low, -y)
            low_sum += y

        length = n - idx
        if (length & 1) == 0:
            suff[idx] = high_sum - low_sum

    return suff


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:1 + n]

    if n % 2 == 0:
        pref = prefix_values(a)
        print(pref[n])
    else:
        pref = prefix_values(a)
        suff = suffix_values(a)

        ans = 0
        # The unmatched position must have even 0-based index.
        for i in range(0, n, 2):
            v = pref[i] + suff[i + 1]
            if v > ans:
                ans = v

        print(ans)


if __name__ == "__main__":
    solve()