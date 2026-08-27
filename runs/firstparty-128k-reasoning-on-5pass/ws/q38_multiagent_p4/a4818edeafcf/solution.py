import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N = data[0]
    A = data[1:]
    del data

    P = [0] * (N + 1)
    seen = [0] * (N + 1)
    d = 0
    for i, a in enumerate(A, 1):
        if not seen[a]:
            seen[a] = 1
            d += 1
        P[i] = d

    if d == 1:
        print(3)
        return
    if d == N:
        print(N)
        return

    S = [0] * (N + 2)
    seen = [0] * (N + 1)
    d = 0
    for i in range(N - 1, -0, -1):
        a = A[i]
        if not seen[a]:
            seen[a] = 1
            d += 1
        S[i + 1] = d

    n = N - 2
    size = 1
    while size < n:
        size <<= 1
    sumv = [0] * (2 * size)
    pref = [0] * (2 * size)
    last = [0] * (N + 1)
    ans = 0

    for j in range(1, N):
        a = A[j - 1]
        prev = last[a]
        if prev:
            L = prev - 1
            R = j - 1
            kL = L + size
            v = sumv[kL] + 1
            sumv[kL] = v
            pref[kL] = v if v > 0 else 0
            if R < n:
                kR = R + size
                v = sumv[kR] - 1
                sumv[kR] = v
                pref[kR] = v if v > 0 else 0
                k1 = kL >> 1
                k2 = kR >> 1
                while k1 != k2:
                    left = k1 << 1
                    right = left | 1
                    sl = sumv[left]
                    sr = sumv[right]
                    sumv[k1] = sl + sr
                    pl = pref[left]
                    pr = sl + pref[right]
                    pref[k1] = pl if pl >= pr else pr

                    left = k2 << 1
                    right = left | 1
                    sl = sumv[left]
                    sr = sumv[right]
                    sumv[k2] = sl + sr
                    pl = pref[left]
                    pr = sl + pref[right]
                    pref[k2] = pl if pl >= pr else pr

                    k1 >>= 1
                    k2 >>= 1
                while k1:
                    left = k1 << 1
                    right = left | 1
                    sl = sumv[left]
                    sr = sumv[right]
                    sumv[k1] = sl + sr
                    pl = pref[left]
                    pr = sl + pref[right]
                    pref[k1] = pl if pl >= pr else pr
                    k1 >>= 1
            else:
                k1 = kL >> 1
                while k1:
                    left = k1 << 1
                    right = left | 1
                    sl = sumv[left]
                    sr = sumv[right]
                    sumv[k1] = sl + sr
                    pl = pref[left]
                    pr = sl + pref[right]
                    pref[k1] = pl if pl >= pr else pr
                    k1 >>= 1
        last[a] = j
        if j >= 2:
            val = P[j] + pref[1] + S[j + 1]
            if val > ans:
                ans = val
                if ans == N:
                    print(N)
                    return

    print(ans)

if __name__ == "__main__":
    main()