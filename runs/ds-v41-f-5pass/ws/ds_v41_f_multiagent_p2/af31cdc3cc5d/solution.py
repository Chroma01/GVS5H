import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))

    # pref[i] = best score obtainable inside segment a[1..i] when i is even
    # (i.e. sum of upper half minus sum of lower half of that segment).
    pref = [0] * (n + 1)
    low = []    # max-heap (negated): holds the smaller half
    high = []   # min-heap: holds the larger half
    sum_low = 0
    sum_high = 0
    for i in range(1, n + 1):
        x = a[i - 1]
        if low and x <= -low[0]:
            heapq.heappush(low, -x)
            sum_low += x
        else:
            heapq.heappush(high, x)
            sum_high += x
        while len(low) > len(high) + 1:
            v = -heapq.heappop(low)
            sum_low -= v
            heapq.heappush(high, v)
            sum_high += v
        while len(high) > len(low):
            v = heapq.heappop(high)
            sum_high -= v
            heapq.heappush(low, -v)
            sum_low += v
        if i % 2 == 0:
            pref[i] = (sum_low + sum_high) - 2 * sum_low

    if n % 2 == 0:
        print(pref[n])
        return

    # suff[j] = best score inside segment a[j..n] when that length is even.
    suff = [0] * (n + 2)
    low = []
    high = []
    sum_low = 0
    sum_high = 0
    cnt = 0
    for j in range(n, 0, -1):
        x = a[j - 1]
        cnt += 1
        if low and x <= -low[0]:
            heapq.heappush(low, -x)
            sum_low += x
        else:
            heapq.heappush(high, x)
            sum_high += x
        while len(low) > len(high) + 1:
            v = -heapq.heappop(low)
            sum_low -= v
            heapq.heappush(high, v)
            sum_high += v
        while len(high) > len(low):
            v = heapq.heappop(high)
            sum_high -= v
            heapq.heappush(low, -v)
            sum_low += v
        if cnt % 2 == 0:
            suff[j] = (sum_low + sum_high) - 2 * sum_low

    ans = 0
    for u in range(1, n + 1, 2):        # u must be odd (1-based)
        right = suff[u + 1] if u + 1 <= n else 0
        s = pref[u - 1] + right
        if s > ans:
            ans = s
    print(ans)


main()