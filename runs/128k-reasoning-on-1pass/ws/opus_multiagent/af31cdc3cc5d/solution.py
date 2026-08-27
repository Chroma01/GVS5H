import sys
from heapq import heappush, heappop


def topsum_prefix(A):
    """res[k] = 2*(sum of largest floor(k/2) elements of A[0:k]) - sum(A[0:k])"""
    n = len(A)
    res = [0] * (n + 1)
    low = []          # max-heap (negated) holding the smaller half
    high = []         # min-heap holding the larger half, size = k//2
    sum_high = 0
    total = 0
    push_low = lambda v: heappush(low, -v)
    for k in range(1, n + 1):
        x = A[k - 1]
        total += x
        heappush(low, -x)
        v = -heappop(low)
        heappush(high, v)
        sum_high += v
        if len(high) > (k >> 1):
            w = heappop(high)
            sum_high -= w
            heappush(low, -w)
        res[k] = 2 * sum_high - total
    return res


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))

    pre = topsum_prefix(A)
    if n % 2 == 0:
        sys.stdout.write(str(pre[n]) + "\n")
        return
    suf = topsum_prefix(A[::-1])
    best = -1
    # survivor at 1-indexed odd position i
    for i in range(1, n + 1, 2):
        val = pre[i - 1] + suf[n - i]
        if val > best:
            best = val
    sys.stdout.write(str(best) + "\n")


main()