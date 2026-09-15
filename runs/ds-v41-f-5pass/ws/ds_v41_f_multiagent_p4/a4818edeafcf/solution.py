import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [0] * (n + 1)
    for i in range(1, n + 1):
        A[i] = int(data[i])

    # prefix distinct counts
    pref = [0] * (n + 2)
    seen = bytearray(n + 2)
    c = 0
    for i in range(1, n + 1):
        v = A[i]
        if seen[v] == 0:
            seen[v] = 1
            c += 1
        pref[i] = c

    # suffix distinct counts
    suf = [0] * (n + 3)
    seen = bytearray(n + 2)
    c = 0
    for i in range(n, 0, -1):
        v = A[i]
        if seen[v] == 0:
            seen[v] = 1
            c += 1
        suf[i] = c

    # previous occurrence
    prev = [0] * (n + 1)
    last = [0] * (n + 2)
    for i in range(1, n + 1):
        v = A[i]
        prev[i] = last[v]
        last[v] = i

    # segment tree (no push) : range add, global max = mx[1]
    # invariant: mx[k] = tag[k] + max(mx[2k], mx[2k+1]) for internal nodes
    m = n
    size = 1
    log = 0
    while size < m:
        size <<= 1
        log += 1
    mx = [0] * (size << 1)
    tag = [0] * size

    ans = 0
    for j in range(2, n):  # j = right end of middle, 2..n-1
        p = prev[j]
        if p:
            # add +1 coverage on i in [p, j-1]  -> leaves [p-1, j-1)
            l = p - 1 + size
            r = j - 1 + size
            l0 = l
            r0 = r
            while l < r:
                if l & 1:
                    mx[l] += 1
                    if l < size:
                        tag[l] += 1
                    l += 1
                if r & 1:
                    r -= 1
                    mx[r] += 1
                    if r < size:
                        tag[r] += 1
                l >>= 1
                r >>= 1
            i = 1
            while i <= log:
                if ((l0 >> i) << i) != l0:
                    k = l0 >> i
                    a = mx[k + k]; b = mx[k + k + 1]
                    mx[k] = tag[k] + (a if a > b else b)
                if ((r0 >> i) << i) != r0:
                    k = (r0 - 1) >> i
                    a = mx[k + k]; b = mx[k + k + 1]
                    mx[k] = tag[k] + (a if a > b else b)
                i += 1
        cand = pref[j] + mx[1] + suf[j + 1]
        if cand > ans:
            ans = cand

    sys.stdout.write(str(ans) + "\n")

main()