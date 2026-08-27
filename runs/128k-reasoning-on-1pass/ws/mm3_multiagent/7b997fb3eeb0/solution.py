import sys

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    # compute nxt[i] = smallest j > i with A[j] >= 2*A[i] (or N)
    nxt = [N] * N
    d = [0] * N
    j = N
    for i in range(N - 1, -1, -1):
        target = A[i] * 2
        while j > i + 1 and A[j - 1] >= target:
            j -= 1
        if j < N and A[j] >= target:
            nxt[i] = j
        else:
            nxt[i] = N
        d[i] = nxt[i] - i

    # build segment tree for range maximum queries on d
    size = 1
    while size < N:
        size <<= 1
    seg = [0] * (2 * size)
    for i in range(N):
        seg[size + i] = d[i]
    for i in range(size - 1, 0, -1):
        seg[i] = seg[2 * i] if seg[2 * i] > seg[2 * i + 1] else seg[2 * i + 1]

    def range_max(l, r):
        """maximum of d[l..r] (inclusive). l,r are 0-indexed."""
        if l > r:
            return 0
        l += size
        r += size
        res = 0
        while l <= r:
            if l & 1:
                if seg[l] > res:
                    res = seg[l]
                l += 1
            if not (r & 1):
                if seg[r] > res:
                    res = seg[r]
                r -= 1
            l >>= 1
            r >>= 1
        return res

    Q = int(next(it))
    out = []
    for _ in range(Q):
        L = int(next(it)) - 1
        R = int(next(it)) - 1
        M = R - L + 1
        lo = 0
        hi = M // 2
        while lo < hi:
            mid = (lo + hi + 1) // 2
            # check if we can make mid kagamimochi using the first mid elements as smalls
            max_d = range_max(L, L + mid - 1) if mid > 0 else 0
            if max_d <= M - mid:
                lo = mid
            else:
                hi = mid - 1
        out.append(str(lo))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()