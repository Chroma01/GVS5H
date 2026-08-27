import sys
from bisect import bisect_left

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    a = [next(it) for _ in range(n)]

    # d[i] = first index j with A[j] >= 2*A[i], minus i.
    d = [0] * n
    for i, x in enumerate(a):
        d[i] = bisect_left(a, 2 * x) - i

    # Sparse table for range maximum queries.
    st = [d]
    length = 1
    while (length << 1) <= n:
        prev = st[-1]
        half = length
        cur_len = n - (length << 1) + 1
        cur = [
            prev[i] if prev[i] >= prev[i + half] else prev[i + half]
            for i in range(cur_len)
        ]
        st.append(cur)
        length <<= 1

    def range_max(left, right):
        """Maximum on inclusive 0-indexed range [left, right]."""
        span = right - left + 1
        p = span.bit_length() - 1
        offset = 1 << p
        x = st[p][left]
        y = st[p][right - offset + 1]
        return x if x >= y else y

    q = next(it)
    ans = []

    for _ in range(q):
        l = next(it) - 1
        r = next(it) - 1
        size = r - l + 1

        lo = 0
        hi = size // 2

        while lo < hi:
            mid = (lo + hi + 1) // 2

            # Need max D[x] for x in [l, l+mid-1] <= size-mid.
            if range_max(l, l + mid - 1) <= size - mid:
                lo = mid
            else:
                hi = mid - 1

        ans.append(str(lo))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    main()