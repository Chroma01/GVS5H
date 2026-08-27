import sys
import heapq


def half_diffs_even(arr, n):
    """
    res[k] = sum(largest k) - sum(smallest k) for the first 2*k elements.
    """
    res = [0] * (n // 2 + 1)

    low = []    # max-heap via negative values: smallest floor(i/2) elements
    high = []   # min-heap: largest ceil(i/2) elements
    sum_low = 0
    sum_high = 0
    low_size = 0

    heappush = heapq.heappush
    heappop = heapq.heappop

    for i, x in enumerate(arr, 1):
        if low_size and x <= -low[0]:
            heappush(low, -x)
            sum_low += x
            low_size += 1
        else:
            heappush(high, x)
            sum_high += x

        target_low = i >> 1

        if low_size < target_low:
            v = heappop(high)
            sum_high -= v
            heappush(low, -v)
            sum_low += v
            low_size += 1
        elif low_size > target_low:
            v = -heappop(low)
            sum_low -= v
            heappush(high, v)
            sum_high += v
            low_size -= 1

        if (i & 1) == 0:
            res[i >> 1] = sum_high - sum_low

    return res


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    del data

    pref = half_diffs_even(a, n)

    if n % 2 == 0:
        ans = pref[n // 2]
    else:
        rev = half_diffs_even(reversed(a), n)
        m = n // 2
        ans = 0
        for k in range(m + 1):
            v = pref[k] + rev[m - k]
            if v > ans:
                ans = v

    print(ans)


if __name__ == "__main__":
    main()