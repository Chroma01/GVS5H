import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    A = data[1:]
    del data

    # First cut i can be 1..N-2.
    M = N - 2

    # Segment tree size.
    S = 1 << (M - 1).bit_length()
    LOG = S.bit_length() - 1
    NEG = -10**18

    # Lazy segment tree.
    # Invariant:
    #   mx[k] includes lz[k] and descendants, but excludes ancestors' lz.
    #   For internal k: mx[k] = lz[k] + max(mx[2k], mx[2k+1]).
    mx = [NEG] * (2 * S)
    lz = [0] * S

    # prev[j] = previous occurrence position of A[j], 1-indexed; 0 if none.
    prev = [0] * (N + 1)
    last = [0] * (N + 1)

    # Compute previous occurrences and initialize leaves with prefix distinct counts.
    cnt = 0
    for idx in range(1, N):  # only prev[1..N-1] is needed
        x = A[idx - 1]
        p = last[x]
        prev[idx] = p
        if p == 0:
            cnt += 1
        last[x] = idx
        if idx <= M:
            mx[S + idx - 1] = cnt

    # Build segment tree.
    for k in range(S - 1, 0, -1):
        a = mx[k << 1]
        b = mx[(k << 1) | 1]
        mx[k] = a if a >= b else b

    # suffix distinct counts: suf[i] = distinct in A[i..N], 1-indexed.
    suf = [0] * (N + 2)
    last = [0] * (N + 1)
    cnt = 0
    for idx in range(N, 0, -1):
        x = A[idx - 1]
        if last[x] == 0:
            cnt += 1
            last[x] = 1
        suf[idx] = cnt

    del A, last

    level_info = [(i, (1 << i) - 1) for i in range(1, LOG + 1)]

    def range_add(l, r, mx=mx, lz=lz, S=S, level_info=level_info):
        """Add 1 to inclusive 0-indexed range [l, r]."""
        l += S
        r += S + 1
        l0 = l
        r0 = r

        while l < r:
            if l & 1:
                mx[l] += 1
                if l < S:
                    lz[l] += 1
                l += 1
            if r & 1:
                r -= 1
                mx[r] += 1
                if r < S:
                    lz[r] += 1
            l >>= 1
            r >>= 1

        # Rebuild affected ancestors bottom-up, skipping nodes that were directly applied.
        for i, mask in level_info:
            p = 0
            if l0 & mask:
                p = l0 >> i
                lc = p << 1
                a = mx[lc]
                b = mx[lc | 1]
                mx[p] = lz[p] + (a if a >= b else b)
            if r0 & mask:
                q = (r0 - 1) >> i
                if q != p:
                    lc = q << 1
                    a = mx[lc]
                    b = mx[lc | 1]
                    mx[q] = lz[q] + (a if a >= b else b)

    def prefix_max(r, mx=mx, lz=lz, S=S, NEG=NEG):
        """Maximum on inclusive 0-indexed prefix [0, r]."""
        k = 1
        left = 0
        right = S - 1
        carry = 0
        res = NEG

        while True:
            if right <= r:
                v = mx[k] + carry
                return v if v > res else res

            # Current node is internal here.
            carry += lz[k]
            mid = (left + right) >> 1

            if r <= mid:
                k = k << 1
                right = mid
            else:
                lc = k << 1
                v = mx[lc] + carry
                if v > res:
                    res = v
                k = lc | 1
                left = mid + 1

    ans = 0
    add = range_add
    query = prefix_max

    # Sweep second cut j = 2..N-1.
    for j in range(2, N):
        p = prev[j]

        # Valid first cuts are 1..min(j-1, N-2).
        r = j - 1
        if r > M:
            r = M

        # A[j] contributes to middle A[i+1..j] iff i >= prev[j].
        l = p if p else 1
        if l <= r:
            add(l - 1, r - 1)

        best = query(r - 1)
        total = best + suf[j + 1]
        if total > ans:
            ans = total

    sys.stdout.write(str(ans) + "\n")


if __name__ == "__main__":
    solve()