import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    a = [next(it) for _ in range(n)]

    # partner[i] = first index j such that a[j] >= 2 * a[i], or n if absent.
    partner = [n] * n
    p = 0
    for i in range(n):
        need = 2 * a[i]
        if p < i + 1:
            p = i + 1
        while p < n and a[p] < need:
            p += 1
        partner[i] = p

    # d[i] = partner[i] - i.
    # For a candidate K in an interval of length m, feasibility is:
    # max(d[l : l + K]) <= m - K.
    d = [partner[i] - i for i in range(n)]

    # Sparse table for static range maximum queries.
    logs = [0] * (n + 1)
    for i in range(2, n + 1):
        logs[i] = logs[i >> 1] + 1

    st = [d]
    width = 1
    while (width << 1) <= n:
        prev = st[-1]
        half = width
        limit = len(prev) - half
        cur = [
            prev[i] if prev[i] >= prev[i + half] else prev[i + half]
            for i in range(limit)
        ]
        st.append(cur)
        width <<= 1

    def range_max(left, right):
        """Maximum on half-open interval [left, right), with left < right."""
        length = right - left
        k = logs[length]
        row = st[k]
        block = 1 << k
        x = row[left]
        y = row[right - block]
        return x if x >= y else y

    q = next(it)
    ans = []

    for _ in range(q):
        l = next(it) - 1
        r = next(it) - 1
        m = r - l + 1

        low = 0
        high = m // 2

        while low < high:
            k = (low + high + 1) // 2
            if range_max(l, l + k) <= m - k:
                low = k
            else:
                high = k - 1

        ans.append(str(low))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()