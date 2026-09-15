import sys
from heapq import heappush, heappop


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    A = data[1:1 + N]
    del data

    if N == 1:
        print(0)
        return

    # Even N: the whole array is one even segment.
    if N % 2 == 0:
        A.sort()
        half = N // 2
        total = sum(A)
        small = sum(A[:half])
        print(total - 2 * small)
        return

    # Odd N:
    # pref[k] = best value for prefix of length 2k.
    # Maintain lower half in a max-heap (as negatives) and upper half in a min-heap.
    lo = []
    up = []
    slo = 0
    sup = 0
    n = 0
    pref = [0]

    # Only even prefixes up to N-1 are needed.
    for i in range(N - 1):
        x = A[i]

        if not lo or x <= -lo[0]:
            heappush(lo, -x)
            slo += x
        else:
            heappush(up, x)
            sup += x

        n += 1
        desired = n >> 1  # lower half size = floor(n / 2)

        if len(lo) > desired:
            v = -heappop(lo)
            slo -= v
            heappush(up, v)
            sup += v
        elif len(lo) < desired:
            v = heappop(up)
            sup -= v
            heappush(lo, -v)
            slo += v

        # Restore all(lo) <= all(up).
        while lo and up and -lo[0] > up[0]:
            a = -heappop(lo)
            slo -= a
            b = heappop(up)
            sup -= b
            heappush(lo, -b)
            slo += b
            heappush(up, a)
            sup += a

        if not (n & 1):
            pref.append(sup - slo)

    # Case where the remaining element is the last one.
    ans = pref[-1]

    # Scan suffixes from right to left, combining with prefix values.
    lo = []
    up = []
    slo = 0
    sup = 0
    n = 0

    # Suffix length n = N - i. We only need even n.
    for i in range(N - 1, 0, -1):
        x = A[i]

        if not lo or x <= -lo[0]:
            heappush(lo, -x)
            slo += x
        else:
            heappush(up, x)
            sup += x

        n += 1
        desired = n >> 1

        if len(lo) > desired:
            v = -heappop(lo)
            slo -= v
            heappush(up, v)
            sup += v
        elif len(lo) < desired:
            v = heappop(up)
            sup -= v
            heappush(lo, -v)
            slo += v

        while lo and up and -lo[0] > up[0]:
            a = -heappop(lo)
            slo -= a
            b = heappop(up)
            sup -= b
            heappush(lo, -b)
            slo += b
            heappush(up, a)
            sup += a

        if not (n & 1):
            # Unmatched index is N - n - 1, which is even.
            # Prefix length is N - n - 1 = 2k.
            k = (N - n - 1) >> 1
            val = pref[k] + (sup - slo)
            if val > ans:
                ans = val

    print(ans)


if __name__ == "__main__":
    solve()