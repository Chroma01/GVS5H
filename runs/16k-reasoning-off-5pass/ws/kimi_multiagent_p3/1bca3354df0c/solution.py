import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1

    parent = list(range(N))
    parity = [0] * N          # xor of colors from node to parent
    size = [1] * N
    cnt0 = [1] * N            # color-0 class size (valid at roots)
    cnt1 = [0] * N            # color-1 class size (valid at roots)

    sys.setrecursionlimit(1 << 25)

    def find(x):
        if parent[x] != x:
            px = parent[x]
            r = find(px)
            parity[x] ^= parity[px]
            parent[x] = r
        return parent[x]

    for _ in range(M):
        u = int(data[idx]) - 1; idx += 1
        v = int(data[idx]) - 1; idx += 1
        find(u); find(v)
        ru, rv = parent[u], parent[v]
        if ru == rv:
            continue  # guaranteed bipartite
        pu, pv = parity[u], parity[v]
        if size[ru] < size[rv]:
            ru, rv = rv, ru
            pu, pv = pv, pu
        parent[rv] = ru
        parity[rv] = pu ^ pv ^ 1
        size[ru] += size[rv]
        cnt0[ru] += cnt0[rv]
        cnt1[ru] += cnt1[rv]

    comps = []
    for v in range(N):
        if find(v) == v:
            comps.append((cnt0[v], cnt1[v]))

    # Total moves T = a_final * b_final - M, a_final + b_final = N.
    # Aoki (first player) wins iff T is odd.
    #
    # N odd : a*b always even => T ≡ M (mod 2). Determined.
    # N even: T ≡ a_final + M (mod 2),
    #   a_final ≡ A0 ⊕ F, A0 = Σ a_i (mod 2),
    #   F = XOR of final flip bits of the k odd-sized components (k even).
    #   Aoki wants F = 1 ⊕ A0 ⊕ M.
    #
    # Flip-control game (verified by exhaustive brute force N ≤ 5 and
    # randomized stress N = 6 — see NOTES):
    #   k = 0      : F = 0 forced.
    #   k ≥ 2      : let f = Σ a_i*b_i - M (initial filler moves).
    #                Aoki controls F iff (k/2 + f) is odd.
    #                The controller sets F to his own target value.

    if N % 2 == 1:
        print("Aoki" if M % 2 == 1 else "Takahashi")
        return

    A0 = 0
    k = 0
    f = -M
    for (a, b) in comps:
        A0 ^= (a & 1)
        if (a + b) & 1:
            k += 1
        f += a * b

    T_target = (1 ^ A0 ^ (M & 1)) & 1

    if k == 0:
        aoki_wins = (0 == T_target)
    else:
        aoki_wins = ((k // 2 + f) % 2 == 1)

    print("Aoki" if aoki_wins else "Takahashi")

main()