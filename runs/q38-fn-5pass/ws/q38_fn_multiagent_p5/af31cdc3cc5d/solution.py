import sys
import heapq


def half_values(iterable, m):
    """
    vals[k] = sum(largest k) - sum(smallest k)
    for the first 2k elements of iterable.
    """
    vals = [0] * (m + 1)
    if m == 0:
        return vals

    low = []   # max-heap via negative values: smaller half
    high = []  # min-heap: larger half
    sum_low = 0
    sum_high = 0

    heappush = heapq.heappush
    heappop = heapq.heappop

    n = 0
    limit = m << 1

    for x in iterable:
        n += 1

        if not low or x <= -low[0]:
            heappush(low, -x)
            sum_low += x
        else:
            heappush(high, x)
            sum_high += x

        # Keep low as the smaller half.
        # When n is odd, low has one extra element.
        low_target = (n + 1) >> 1
        high_target = n - low_target

        while len(low) > low_target:
            v = -heappop(low)
            sum_low -= v
            heappush(high, v)
            sum_high += v

        while len(high) > high_target:
            v = heappop(high)
            sum_high -= v
            heappush(low, -v)
            sum_low += v

        # Safety fix for heap ordering.
        if low and high and -low[0] > high[0]:
            a = -heappop(low)
            sum_low -= a
            b = heappop(high)
            sum_high -= b

            heappush(low, -b)
            sum_low += b
            heappush(high, a)
            sum_high += a

        if (n & 1) == 0:
            vals[n >> 1] = sum_high - sum_low
            if n == limit:
                break

    return vals


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    del data

    if n % 2 == 0:
        m = n // 2
        pref = half_values(a, m)
        print(pref[m])
    else:
        m = (n - 1) // 2

        # pref[p] = best score for first 2p elements
        pref = half_values(a, m)

        # suff[q] = best score for last 2q elements
        suff = half_values(reversed(a), m)

        ans = 0
        for p in range(m + 1):
            cur = pref[p] + suff[m - p]
            if cur > ans:
                ans = cur

        print(ans)


if __name__ == "__main__":
    solve()