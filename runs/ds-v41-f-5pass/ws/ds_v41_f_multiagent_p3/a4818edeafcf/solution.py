import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [0] * (n + 1)
    for i in range(1, n + 1):
        A[i] = int(data[i])

    # pre[i] = number of distinct values in A[1..i]
    pre = [0] * (n + 1)
    seen = bytearray(n + 2)
    c = 0
    for i in range(1, n + 1):
        v = A[i]
        if not seen[v]:
            seen[v] = 1
            c += 1
        pre[i] = c

    # suf[i] = number of distinct values in A[i..n]
    suf = [0] * (n + 2)
    seen = bytearray(n + 2)
    c = 0
    for i in range(n, 0, -1):
        v = A[i]
        if not seen[v]:
            seen[v] = 1
            c += 1
        suf[i] = c

    # prev[i] = previous occurrence of A[i]
    prev = [0] * (n + 1)
    last = [0] * (n + 2)
    for i in range(1, n + 1):
        v = A[i]
        prev[i] = last[v]
        last[v] = i

    # Segment tree over positions idx = i-1 (i = 1..n).
    # Node stores:
    #   s = sum of dB over its range
    #   m = max over positions p in range of (base[p] + sum of dB from range-left to p)
    # where base[p] = pre[p+1] - (p+1), and dB is the difference array of the suffix adds.
    size = 1
    while size < n:
        size <<= 1
    NEG = -(1 << 60)
    s = [0] * (2 * size)
    m = [NEG] * (2 * size)
    for idx in range(n):
        m[size + idx] = pre[idx + 1] - (idx + 1)
    for k in range(size - 1, 0, -1):
        l = k + k
        sl = s[l]
        s[k] = sl + s[l + 1]
        t = sl + m[l + 1]
        ml = m[l]
        m[k] = ml if ml > t else t

    ans = 0
    ss = s
    mm = m
    sz = size
    for j in range(1, n):          # j = second cut, j <= n-1
        # suffix add +1 for all i >= max(1, prev[j])  ->  point add on difference array
        p0 = prev[j] - 1
        if p0 < 0:
            p0 = 0
        p = sz + p0
        ss[p] += 1
        mm[p] += 1
        p >>= 1
        while p:
            l = p + p
            sl = ss[l]
            ss[p] = sl + ss[l + 1]
            t = sl + mm[l + 1]
            ml = mm[l]
            mm[p] = ml if ml > t else t
            p >>= 1

        if j >= 2:                 # need i in [1, j-1] -> prefix [0, j-1)
            rr = sz + (j - 1)
            best = NEG
            while rr > 1:
                if rr & 1:
                    rr -= 1
                    t = ss[rr] + best
                    mr = mm[rr]
                    if mr > t:
                        t = mr
                    best = t
                rr >>= 1
            val = best + suf[j + 1]
            if val > ans:
                ans = val

    sys.stdout.write(str(ans) + "\n")

main()