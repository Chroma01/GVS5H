import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    n = int(data[pos]); pos += 1
    A = list(map(int, data[pos:pos + n])); pos += n
    q = int(data[pos]); pos += 1

    # nxt[i] = first index j > i with A[j] >= 2*A[i], else n (sentinel).
    # 2*A[i] is non-decreasing, so a single forward pointer suffices.
    nxt = [n] * n
    j = 1
    for i in range(n):
        t = A[i] << 1
        if j <= i:
            j = i + 1
        while j < n and A[j] < t:
            j += 1
        nxt[i] = j
    h = [nxt[i] - i for i in range(n)]

    # log table
    LOG = [0] * (n + 2)
    for i in range(2, n + 2):
        LOG[i] = LOG[i >> 1] + 1

    # sparse table for range maximum over h
    st = [h]
    k = 1
    while (1 << k) <= n:
        prev = st[-1]
        step = 1 << (k - 1)
        length = n - (1 << k) + 1
        st.append([prev[i] if prev[i] > prev[i + step] else prev[i + step]
                   for i in range(length)])
        k += 1

    out = []
    for _ in range(q):
        L = int(data[pos]) - 1
        R = int(data[pos + 1]) - 1
        pos += 2
        m = R - L + 1
        lo = 0
        hi = m >> 1
        while lo < hi:
            mid = (lo + hi + 1) >> 1
            kk = LOG[mid]
            row = st[kk]
            a = row[L]
            b = row[L + mid - (1 << kk)]
            mx = a if a > b else b
            if mx + mid <= m:
                lo = mid
            else:
                hi = mid - 1
        out.append(lo)

    sys.stdout.write('\n'.join(map(str, out)) + '\n')

main()