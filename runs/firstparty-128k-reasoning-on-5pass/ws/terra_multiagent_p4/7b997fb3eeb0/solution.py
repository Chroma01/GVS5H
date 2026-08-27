import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    a = [next(it) for _ in range(n)]

    # p[j] = first index p such that A[p] >= 2*A[j], or n if absent.
    # d[j] = p[j] - j.
    d = [0] * n
    p = 0
    for j in range(n):
        target = 2 * a[j]
        while p < n and a[p] < target:
            p += 1
        d[j] = p - j

    # Sparse table for range maximum queries on d.
    st = [d]
    length = 1
    while (length << 1) <= n:
        prev = st[-1]
        half = length
        st.append([
            x if x >= y else y
            for x, y in zip(prev, prev[half:])
        ])
        length <<= 1

    lg = [0] * (n + 1)
    for i in range(2, n + 1):
        lg[i] = lg[i >> 1] + 1

    q = next(it)
    ans = []

    for _ in range(q):
        l = next(it) - 1
        r = next(it) - 1
        size = r - l + 1

        lo = 0
        hi = size // 2

        while lo < hi:
            k = (lo + hi + 1) // 2

            # Maximum D_j on j in [l, l+k).
            level = lg[k]
            span = 1 << level
            left_max = st[level][l]
            right_max = st[level][l + k - span]
            max_d = left_max if left_max >= right_max else right_max

            # Feasible iff every needed bottom exists within the query.
            if max_d <= size - k:
                lo = k
            else:
                hi = k - 1

        ans.append(str(lo))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    main()