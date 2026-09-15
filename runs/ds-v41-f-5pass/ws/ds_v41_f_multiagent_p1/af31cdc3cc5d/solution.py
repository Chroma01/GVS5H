import sys
import heapq


def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))

    def prefix_scores(arr):
        """res[L] = f(arr[:L]) for every even L (0..n), where
        f(segment) = sum(larger half) - sum(smaller half)."""
        lower = []          # max-heap (negated) holding the smaller half
        upper = []          # min-heap holding the larger half
        sum_low = 0
        sum_up = 0
        res = [0] * (len(arr) + 1)
        for i, x in enumerate(arr, start=1):
            heapq.heappush(upper, x)
            sum_up += x
            v = heapq.heappop(upper)
            sum_up -= v
            heapq.heappush(lower, -v)
            sum_low += v
            if len(lower) > len(upper):
                w = -heapq.heappop(lower)
                sum_low -= w
                heapq.heappush(upper, w)
                sum_up += w
            if i % 2 == 0:
                res[i] = sum_up - sum_low
        return res

    if n % 2 == 0:
        left = prefix_scores(a)
        print(left[n])
        return

    # Odd n: the single unmatched element must be at an odd 1-indexed
    # position p, splitting the array into two independently matched
    # even segments A[1..p-1] and A[p+1..n].
    left = prefix_scores(a)                     # left[L] = f(A[1..L])
    rev = a[::-1]
    pref = prefix_scores(rev)                   # pref[k] = f(last k elements)

    ans = 0
    for p in range(1, n + 1, 2):                # odd unmatched positions
        right_len = n - p
        val = left[p - 1] + pref[right_len]
        if val > ans:
            ans = val
    print(ans)


solve()