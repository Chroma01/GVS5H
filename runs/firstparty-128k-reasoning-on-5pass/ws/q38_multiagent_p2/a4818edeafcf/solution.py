import sys

def main():
    input = sys.stdin.buffer.readline
    line = input()
    if not line:
        return
    N = int(line)
    A = []
    while len(A) < N:
        A.extend(map(int, input().split()))

    n = N - 2
    size = 1 << (n - 1).bit_length()
    NEG = -10**9

    seg_sum = [0] * (2 * size)
    seg_best = [NEG] * (2 * size)

    # Initial leaf values: distinct count of A[0..i] for first cut i+1.
    seen = bytearray(N + 1)
    cnt = 0
    base = size
    for i in range(n):
        x = A[i]
        if not seen[x]:
            seen[x] = 1
            cnt += 1
        seg_best[base + i] = cnt

    # Build internal best values; all sums are initially zero.
    for k in range(size - 1, 0, -1):
        left = k << 1
        right = left + 1
        b = seg_best[left]
        c = seg_best[right]
        seg_best[k] = b if b >= c else c

    # suff[pos] = distinct count in A[pos..N-1]
    suff = [0] * (N + 1)
    seen = bytearray(N + 1)
    cnt = 0
    for pos in range(N - 1, -1, -1):
        x = A[pos]
        if not seen[x]:
            seen[x] = 1
            cnt += 1
        suff[pos] = cnt

    last = [0] * (N + 1)
    last[A[0]] = 1

    ans = 0
    gadd = 0  # stores D[0], a uniform addition to all leaves

    ss = seg_sum
    sb = seg_best
    sz = size
    nn = n
    suff_l = suff
    last_l = last
    A_l = A
    neg = NEG

    # idx is 0-based current position, and also j-1 where j = idx+1.
    for idx in range(1, N - 1):
        x = A_l[idx]
        p = last_l[x]
        l = p - 1 if p else 0

        if l == 0:
            # Add to [0, idx): D[0] += 1, D[idx] -= 1 if idx < n.
            gadd += 1
            if idx < nn:
                k = idx + sz
                ss[k] -= 1
                sb[k] -= 1
                a = k >> 1
                while a:
                    left = a << 1
                    right = left + 1
                    sl = ss[left]
                    ss[a] = sl + ss[right]
                    bl = sb[left]
                    br = sl + sb[right]
                    sb[a] = bl if bl >= br else br
                    a >>= 1
        else:
            if idx < nn:
                # Add to [l, idx): D[l] += 1, D[idx] -= 1.
                k1 = l + sz
                ss[k1] += 1
                sb[k1] += 1
                k2 = idx + sz
                ss[k2] -= 1
                sb[k2] -= 1

                a = k1 >> 1
                b = k2 >> 1
                while a:
                    left = a << 1
                    right = left + 1
                    sl = ss[left]
                    ss[a] = sl + ss[right]
                    bl = sb[left]
                    br = sl + sb[right]
                    sb[a] = bl if bl >= br else br

                    if b != a:
                        left = b << 1
                        right = left + 1
                        sl = ss[left]
                        ss[b] = sl + ss[right]
                        bl = sb[left]
                        br = sl + sb[right]
                        sb[b] = bl if bl >= br else br

                    a >>= 1
                    b >>= 1
            else:
                # Add to [l, n): only D[l] += 1.
                k = l + sz
                ss[k] += 1
                sb[k] += 1
                a = k >> 1
                while a:
                    left = a << 1
                    right = left + 1
                    sl = ss[left]
                    ss[a] = sl + ss[right]
                    bl = sb[left]
                    br = sl + sb[right]
                    sb[a] = bl if bl >= br else br
                    a >>= 1

        # Query max over first cuts i = 1..idx, i.e. leaves [0, idx).
        if idx >= nn:
            res = sb[1]
        else:
            i = sz + idx
            res = neg
            while i > 1:
                if i & 1:
                    node = i - 1
                    b = ss[node] + res
                    nb = sb[node]
                    res = nb if nb >= b else b
                i >>= 1

        val = res + gadd + suff_l[idx + 1]
        if val > ans:
            ans = val

        last_l[x] = idx + 1

    print(ans)

if __name__ == "__main__":
    main()