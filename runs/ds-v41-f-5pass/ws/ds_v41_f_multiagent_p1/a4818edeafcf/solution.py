import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:n + 1]))

    # suf[k] = number of distinct values in A[k..N], 1-indexed; suf[N+1] = 0
    suf = [0] * (n + 2)
    seen = bytearray(n + 1)
    cnt = 0
    for k in range(n, 0, -1):
        v = A[k - 1]
        if not seen[v]:
            seen[v] = 1
            cnt += 1
        suf[k] = cnt

    size = 1
    while size < n:
        size <<= 1
    # invariant: d[k] = max(d[2k], d[2k+1]) + lz[k] for internal k; no push ever needed
    d = [0] * (2 * size)
    lz = [0] * size
    last = [0] * (n + 1)

    D = 0
    ans = 0
    for j in range(1, n):           # j = 1..N-1 (right split position)
        v = A[j - 1]
        p = last[v]
        last[v] = j
        if p == 0:
            D += 1                  # new distinct value in prefix
        else:
            l0 = p - 1              # 0-based inclusive start  (1-indexed i = p)
            r0 = j - 1              # 0-based exclusive end    (1-indexed i <= j-1)
            if r0 - l0 == 1:
                i = size + l0       # leaf: no lz, single fast path
                d[i] += 1
                i >>= 1
                while i:
                    a = d[i + i]; b = d[i + i + 1]
                    d[i] = (a if a >= b else b) + lz[i]
                    i >>= 1
            else:
                l = l0 + size
                r = r0 + size
                lo = l
                ro = r
                while l < r:
                    if l & 1:
                        d[l] += 1
                        if l < size:
                            lz[l] += 1
                        l += 1
                    if r & 1:
                        r -= 1
                        d[r] += 1
                        if r < size:
                            lz[r] += 1
                    l >>= 1
                    r >>= 1
                i = lo >> 1
                while i:
                    a = d[i + i]; b = d[i + i + 1]
                    d[i] = (a if a >= b else b) + lz[i]
                    i >>= 1
                i = (ro - 1) >> 1
                while i:
                    a = d[i + i]; b = d[i + i + 1]
                    d[i] = (a if a >= b else b) + lz[i]
                    i >>= 1
        if j >= 2:
            c = D + suf[j + 1] + d[1]
            if c > ans:
                ans = c

    sys.stdout.write(str(ans) + "\n")

main()