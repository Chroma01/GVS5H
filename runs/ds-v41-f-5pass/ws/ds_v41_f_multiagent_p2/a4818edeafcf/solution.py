import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N = data[0]
    A = data[1:1 + N]

    # pref[i] = number of distinct values in A[0..i]
    pref = [0] * N
    seen = bytearray(N + 1)
    c = 0
    for i in range(N):
        x = A[i]
        if not seen[x]:
            seen[x] = 1
            c += 1
        pref[i] = c

    # suff[i] = number of distinct values in A[i..N-1]
    suff = [0] * N
    seen = bytearray(N + 1)
    c = 0
    for i in range(N - 1, -1, -1):
        x = A[i]
        if not seen[x]:
            seen[x] = 1
            c += 1
        suff[i] = c

    NEG = -10**9
    size = 1
    while size < N:
        size <<= 1

    mx = [NEG] * (2 * size)
    lazy = [0] * size

    last = [-1] * (N + 1)
    last[A[0]] = 0

    ans = 0
    for j in range(1, N - 1):
        x = A[j]
        p = last[x]
        last[x] = j

        # If previous occurrence p > 0, subtract 1 from prefix [0, p)
        if p > 0:
            r = p + size
            l = size
            l0 = l
            r0 = r - 1
            while l < r:
                if l & 1:
                    mx[l] -= 1
                    if l < size:
                        lazy[l] -= 1
                    l += 1
                if r & 1:
                    r -= 1
                    mx[r] -= 1
                    if r < size:
                        lazy[r] -= 1
                l >>= 1
                r >>= 1

            l = l0
            while l > 1:
                l >>= 1
                left = mx[l << 1]
                right = mx[l << 1 | 1]
                mx[l] = (left if left > right else right) + lazy[l]

            r = r0
            while r > 1:
                r >>= 1
                left = mx[r << 1]
                right = mx[r << 1 | 1]
                mx[r] = (left if left > right else right) + lazy[r]

        # point set for the new left cut i = j-1
        pos = j - 1
        pidx = pos + size
        mx[pidx] = pref[pos] + 1 - j
        pidx >>= 1
        while pidx:
            left = mx[pidx << 1]
            right = mx[pidx << 1 | 1]
            mx[pidx] = (left if left > right else right) + lazy[pidx]
            pidx >>= 1

        cand = mx[1] + j + suff[j + 1]
        if cand > ans:
            ans = cand

    print(ans)

if __name__ == "__main__":
    solve()