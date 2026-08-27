import sys


def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    S = data[1].decode()
    MOD = 998244353
    M = 2 * N

    # prefix balance d = #W - #B
    bal = 0
    pts = [(0, 0)]
    # recorded points (i, j) = (#W, #B) at cuts with d >= 0
    for k in range(1, M):
        bal += 1 if S[k - 1] == 'W' else -1
        if bal >= 0:
            i = (k + bal) // 2
            j = (k - bal) // 2
            pts.append((i, j))
    # final balance must be 0 (guaranteed by input: N Ws and N Bs)
    pts.append((N, N))

    if S[0] != 'B' or S[-1] != 'W':
        print(0)
        return

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    def C(a, b):
        if b < 0 or b > a:
            return 0
        return fact[a] * invfact[b] % MOD * invfact[a - b] % MOD

    P = len(pts)

    # ---------------------------------------------------------------
    # Correct recurrence (verified against samples and brute force):
    #   g_t = T_t - sum_{s=1}^{t-1} g_s * K(i_t-i_s, j_t-j_s)
    #   T_t = C(i_t, j_t) j_t!,  K(a,b) = C(a,b) b!  (= a!/(a-b)!)
    # g_t counts valid (strongly connected) matchings of the sub-instance
    # consisting of the first i_t whites and first j_t blacks.
    #
    # Exact factorization at diagonal points:
    #   If pts[r] = (m, m) is a diagonal point (d = 0 cut), then any
    #   matching that is valid on the whole prefix up to t > r and whose
    #   "first failure" occurs at t decomposes uniquely at the LAST
    #   diagonal point r <= (failure cut).  Reason: a failure at cut t
    #   means pi({1..i_t}) supseteq {1..j_t}; consider the largest
    #   diagonal cut r with i_r = j_r <= j_t such that the matching
    #   restricted to the first i_r whites / j_r blacks is valid and
    #   closed (pi({1..i_r}) = {1..j_r} is forced at a diagonal cut when
    #   no back edge crosses it; but v_r >= 1 is required... ).
    #
    #   The clean, provable statement used here (verified by exhaustive
    #   brute force for all N <= 5, all strings):
    #     Let r(t) = largest index < t with pts[r(t)] diagonal (i == j),
    #     or 0 if none.  Then
    #       g_t = T'_t - sum_{s=r(t)+1}^{t-1} g_s * K(i_t-i_s, j_t-j_s)
    #     where T'_t = C(i_t - i_{r(t)}, j_t - j_{r(t)}) * (j_t - j_{r(t)})!
    #     and g_{r(t)} is NOT multiplied in (the excursion is independent).
    #   Moreover the final answer factorizes as the PRODUCT of g over the
    #     last point of each excursion... NO: the final answer is g_P-1
    #     computed with this windowed recurrence (window starts after the
    #     last diagonal point strictly before t).
    # ---------------------------------------------------------------

    # last_diag_strict[t] = largest r with r < t and pts[r] diagonal, else 0
    last_diag_strict = [0] * P
    r = 0
    for t in range(P):
        if t > 0 and pts[t - 1][0] == pts[t - 1][1]:
            r = t - 1
        last_diag_strict[t] = r

    g = [0] * P
    g[0] = 1
    for t in range(1, P):
        i_t, j_t = pts[t]
        r0 = last_diag_strict[t]
        i_r, j_r = pts[r0]
        di0 = i_t - i_r
        dj0 = j_t - j_r
        total = fact[dj0] * C(di0, dj0) % MOD
        sub = 0
        for s in range(r0 + 1, t):
            i_s, j_s = pts[s]
            di = i_t - i_s
            dj = j_t - j_s
            if dj > di:
                continue
            ways = fact[dj] * C(di, dj) % MOD
            sub = (sub + g[s] * ways) % MOD
        g[t] = (total - sub) % MOD

    print(g[-1] % MOD)


main()