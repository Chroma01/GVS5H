import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    K = int(data[0])
    S = data[1] if len(data) > 1 else b""
    T = data[2] if len(data) > 2 else b""

    n = len(S)
    m = len(T)

    # length gap larger than K -> impossible (each op changes length by at most 1)
    if abs(n - m) > K:
        sys.stdout.write("No\n")
        return
    if S == T:
        sys.stdout.write("Yes\n")
        return

    # ---- strip longest common prefix / suffix (Levenshtein distance is invariant) ----
    def cpre(a, b):
        lo = 0
        hi = min(len(a), len(b))
        while lo < hi:
            mid = (lo + hi + 1) >> 1
            if a[lo:mid] == b[lo:mid]:
                lo = mid
            else:
                hi = mid - 1
        return lo

    def csuf(a, b):
        la = len(a)
        lb = len(b)
        lo = 0
        hi = min(la, lb)
        while lo < hi:
            mid = (lo + hi + 1) >> 1
            if a[la - mid:la - lo] == b[lb - mid:lb - lo]:
                lo = mid
            else:
                hi = mid - 1
        return lo

    p = cpre(S, T)
    if p:
        S = S[p:]
        T = T[p:]
    s = csuf(S, T)
    if s:
        S = S[:len(S) - s]
        T = T[:len(T) - s]

    n = len(S)
    m = len(T)

    if n == 0 or m == 0:
        sys.stdout.write("Yes\n" if max(n, m) <= K else "No\n")
        return

    # ---- exact LCE via doubling + binary search on byte slices ----
    def lce(i, j):
        lim = n - i
        t = m - j
        if t < lim:
            lim = t
        if lim <= 0:
            return 0
        if S[i] != T[j]:
            return 0
        lo = 1
        step = 1
        while lo + step <= lim and S[i + lo:i + lo + step] == T[j + lo:j + lo + step]:
            lo += step
            step <<= 1
        hi = lo + step - 1
        if hi > lim:
            hi = lim
        while lo < hi:
            mid = (lo + hi + 1) >> 1
            if S[i + lo:i + mid] == T[j + lo:j + mid]:
                lo = mid
            else:
                hi = mid - 1
        return lo

    NEG = -10 ** 18
    off = K + 1
    SIZE = 2 * K + 3
    fr = [NEG] * SIZE

    x = lce(0, 0)
    fr[off] = x
    kt = n - m
    if kt == 0 and x == n:
        sys.stdout.write("Yes\n")
        return

    for d in range(1, K + 1):
        new = [NEG] * SIZE
        for k in range(-d, d + 1):
            idx = k + off
            best = NEG
            prev = fr[idx]
            # substitute: (x,y) -> (x+1,y+1), same diagonal
            if prev >= 0:
                c = prev + 1
                if c <= n and c - k <= m and c > best:
                    best = c
                # monotonicity: a path with d-1 edits is also a path with <= d edits
                if prev > best:
                    best = prev
            # delete from S: (x,y) on diagonal k-1 -> (x+1,y) on diagonal k
            v = fr[idx - 1]
            if v >= 0:
                c = v + 1
                if c <= n and c - k <= m and c > best:
                    best = c
            # insert into S: (x,y) on diagonal k+1 -> (x,y+1) on diagonal k
            v = fr[idx + 1]
            if v >= 0:
                c = v
                if c <= n and c - k <= m and c > best:
                    best = c
            if best >= 0:
                y = best - k
                if best < n and y < m:
                    best += lce(best, y)
                new[idx] = best
        fr = new
        if -d <= kt <= d and fr[kt + off] == n:
            sys.stdout.write("Yes\n")
            return

    sys.stdout.write("No\n")


main()