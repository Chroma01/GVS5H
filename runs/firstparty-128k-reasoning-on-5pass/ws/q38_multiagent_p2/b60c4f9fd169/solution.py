import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    K = int(data[0])
    S = data[1]
    T = data[2]
    n = len(S)
    m = len(T)
    out = sys.stdout.write

    if abs(n - m) > K:
        out("No\n")
        return

    if n > m:
        S, T = T, S
        n, m = m, n

    l = 0
    while l < n and S[l] == T[l]:
        l += 1

    r = 0
    while r < n - l and S[n - 1 - r] == T[m - 1 - r]:
        r += 1

    if l or r:
        S = S[l:n - r]
        T = T[l:m - r]
        n -= l + r
        m -= l + r

    if S == T:
        out("Yes\n")
        return

    if n == 0:
        out("Yes\n" if m <= K else "No\n")
        return

    if K >= m:
        out("Yes\n")
        return

    d = m - n
    kmin = -((K - d) // 2)
    kmax = (K + d) // 2
    W = kmax - kmin + 1
    P = W + 2
    INF = K + 1
    off = 1 - kmin

    prev = [INF] * P
    lim = min(m, kmax)
    for delta in range(lim + 1):
        prev[delta + off] = delta

    s = S
    t = b'\0' + T
    k = K
    inf = INF

    for i in range(1, n + 1):
        si = s[i - 1]

        low = kmin
        ni = -i
        if low < ni:
            low = ni

        high = kmax
        mi = m - i
        if high > mi:
            high = mi

        if low > high:
            out("No\n")
            return

        cur = [inf] * P
        alive = False
        idx = low + off

        for j in range(i + low, i + high + 1):
            v = cur[idx - 1] + 1
            u = prev[idx + 1] + 1
            if u < v:
                v = u

            diag = prev[idx] + (si != t[j])
            if diag < v:
                v = diag

            if v <= k:
                alive = True
                cur[idx] = v
            else:
                cur[idx] = inf

            idx += 1

        prev = cur

        if not alive:
            out("No\n")
            return

    out("Yes\n" if prev[d + off] <= k else "No\n")

if __name__ == "__main__":
    main()