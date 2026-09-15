import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    s = data[1]
    MOD = 998244353

    # Determinization of the 2-state NFA (state = x_{i-1}) on edge orientations.
    # DFA states are relations R subset of {0,1}x{0,1}; 12 reachable states:
    #   A=({0},{1}) B=({1},{}) C=({},{0}) E=({0,1},{1}) F=({0},{0,1})
    #   G=({0},{}) H=({0,1},{}) I=({},{1}) J=({},{0,1})
    #   K=({0},{0}) L=({0,1},{0,1}) M=({1},{1});  dead relation dropped.
    # The full transition system is symmetric under the swap
    #   B<->C, E<->F, G<->I, H<->J, K<->M  (A, L fixed).
    # Initial state A is fixed by the swap, and pairs are both-accepting or
    # both-non-accepting, so dp[B]=dp[C], dp[E]=dp[F], dp[G]=dp[I],
    # dp[H]=dp[J], dp[K]=dp[M] forever. Collapse to 7 variables:
    #   a=A, b=B=C, e=E=F, g=G=I, h=H=J, k=K=M, l=L.
    # Answer = sum of accepting states = a + 2e + 2g + 2h + 2k + l.
    a = 1
    b = e = g = h = k = l = 0

    cnt = 0
    for ch in s:
        if ch & 1:  # s_i == '1'
            nb = a + b + e + g + h
            ne = a + e
            ng = b + g + h
            nh = b + g + 2 * h
            nk = e + 2 * k + l
            nl = 2 * (e + k + l)
            a = 0
            b, e, g, h, k, l = nb, ne, ng, nh, nk, nl
        else:       # s_i == '0'
            nb = a + b + e + g + h
            ng = b + g + h
            nk = e + 2 * k + l
            b, g, k = nb, ng, nk
        cnt += 1
        if cnt == 64:
            a %= MOD; b %= MOD; e %= MOD; g %= MOD
            h %= MOD; k %= MOD; l %= MOD
            cnt = 0

    ans = (a + 2 * (e + g + h + k) + l) % MOD
    sys.stdout.write(str(ans) + "\n")

main()