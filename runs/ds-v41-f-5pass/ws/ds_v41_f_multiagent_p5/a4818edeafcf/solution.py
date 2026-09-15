import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [0] * (n + 1)
    for i in range(1, n + 1):
        A[i] = int(data[i])

    # prefix distinct counts
    pref = [0] * (n + 2)
    seen = bytearray(n + 1)
    c = 0
    for i in range(1, n + 1):
        v = A[i]
        if not seen[v]:
            seen[v] = 1
            c += 1
        pref[i] = c

    # suffix distinct counts
    suff = [0] * (n + 3)
    seen = bytearray(n + 1)
    c = 0
    for i in range(n, 0, -1):
        v = A[i]
        if not seen[v]:
            seen[v] = 1
            c += 1
        suff[i] = c

    # previous occurrence of each value
    prev = [0] * (n + 2)
    last = [0] * (n + 1)
    for i in range(1, n + 1):
        v = A[i]
        prev[i] = last[v]
        last[v] = i

    NEG = -(1 << 60)
    size = 1
    log = 0
    while size < n:
        size <<= 1
        log += 1

    # segment tree: range add, global max (no lazy pushdown needed)
    mx = [NEG] * (2 * size)
    add = [0] * (2 * size)

    ans = 0
    for t in range(2, n):
        # activate left cut i = t-1 (leaf index t-2) with base pref[t-1]
        p = size + t - 2
        mx[p] = pref[t - 1]
        k = p >> 1
        while k:
            l = k << 1
            a = mx[l]; b = mx[l | 1]
            mx[k] = (a if a > b else b) + add[k]
            k >>= 1

        # range add +1 over i in [max(1,prev[t]), t-1]  -> leaves [lft-1, t-1)
        lft = prev[t]
        if lft < 1:
            lft = 1
        L0 = lft - 1 + size
        R0 = t - 1 + size

        L = L0; R = R0
        while L < R:
            if L & 1:
                add[L] += 1
                mx[L] += 1
                L += 1
            if R & 1:
                R -= 1
                add[R] += 1
                mx[R] += 1
            L >>= 1
            R >>= 1

        i = 1
        while i <= log:
            k = L0 >> i
            l = k << 1
            a = mx[l]; b = mx[l | 1]
            mx[k] = (a if a > b else b) + add[k]
            k = (R0 - 1) >> i
            l = k << 1
            a = mx[l]; b = mx[l | 1]
            mx[k] = (a if a > b else b) + add[k]
            i += 1

        cand = mx[1] + suff[t + 1]
        if cand > ans:
            ans = cand

    sys.stdout.write(str(ans) + "\n")

main()