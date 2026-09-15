import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))

    def compute(order):
        # res[k] = score of the first k elements when k is even
        # score = sum(largest k/2) - sum(smallest k/2) = total - 2*lowerSum
        res = [0] * (n + 1)
        lower = []          # max-heap (negated), holds the k//2 smallest elements
        upper = []          # min-heap, holds the rest
        lowerSum = 0
        totalSum = 0
        heappush = heapq.heappush
        heappop = heapq.heappop
        k = 0
        for x in order:
            k += 1
            totalSum += x
            if upper and x > upper[0]:
                heappush(upper, x)
            else:
                heappush(lower, -x)
                lowerSum += x
            half = k >> 1
            while len(lower) > half:
                v = -heappop(lower)
                lowerSum -= v
                heappush(upper, v)
            while len(lower) < half:
                v = heappop(upper)
                heappush(lower, -v)
                lowerSum += v
            if (k & 1) == 0:
                res[k] = totalSum - (lowerSum << 1)
        return res

    pref = compute(A)                # pref[l] = score of A[0..l-1], l even
    suf = compute(A[::-1])           # suf[l]  = score of last l elements, l even

    if n % 2 == 0:
        print(pref[n])
    else:
        best = 0
        # survivor at 0-indexed even position s (1-based odd index)
        # left block length s (even), right block length n-1-s (even)
        for s in range(0, n, 2):
            t = pref[s] + suf[n - 1 - s]
            if t > best:
                best = t
        print(best)


main()