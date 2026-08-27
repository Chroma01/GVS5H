import sys

MOD = 998244353
PRIMITIVE_ROOT = 3
DIRECT_LIMIT = 2000


def count_good(N, constraints, fact, invfact):
    """
    constraints are pairs (v, u), with v and u strictly increasing and u >= v.
    Counts permutations q of [N] such that max(q[:v]) > u for every pair.
    """
    r = len(constraints)
    if r == 0:
        return fact[N]

    v = [x[0] for x in constraints]
    u = [x[1] for x in constraints]

    # Direct O(r^2) evaluation of the first-violation recurrence.
    if r <= DIRECT_LIMIT:
        G = [0] * r
        for i in range(r):
            cur = fact[u[i]]
            ui = u[i]
            for j in range(i):
                cur -= G[j] * fact[ui - v[j]]
            G[i] = (cur % MOD) * invfact[ui - v[i]] % MOD

        bad = 0
        for i in range(r):
            bad = (bad + G[i] * fact[N - v[i]]) % MOD
        return (fact[N] - bad) % MOD

    # CDQ divide and conquer + NTT for the same recurrence:
    # G[i] = (u[i]! - sum_{j<i} G[j] * (u[i]-v[j])!) / (u[i]-v[i])!
    G = [0] * r
    add = [0] * r

    max_n = 1
    while max_n < 3 * N + 3:
        max_n <<= 1

    max_log = max_n.bit_length()
    root_pw = [1] * (max_log + 1)
    inv_root_pw = [1] * (max_log + 1)
    inv_len = [1] * (max_log + 1)
    for e in range(1, max_log + 1):
        length = 1 << e
        root_pw[e] = pow(PRIMITIVE_ROOT, (MOD - 1) // length, MOD)
        inv_root_pw[e] = pow(root_pw[e], MOD - 2, MOD)
        inv_len[e] = pow(length, MOD - 2, MOD)

    def ntt(a, invert):
        n = len(a)
        j = 0
        for i in range(1, n):
            bit = n >> 1
            while j & bit:
                j ^= bit
                bit >>= 1
            j ^= bit
            if i < j:
                a[i], a[j] = a[j], a[i]

        length = 2
        e = 1
        mod = MOD
        while length <= n:
            wlen = inv_root_pw[e] if invert else root_pw[e]
            half = length >> 1
            for i in range(0, n, length):
                w = 1
                for k in range(i, i + half):
                    x = a[k]
                    y = a[k + half] * w % mod

                    s = x + y
                    if s >= mod:
                        s -= mod
                    d = x - y
                    if d < 0:
                        d += mod

                    a[k] = s
                    a[k + half] = d
                    w = w * wlen % mod
            length <<= 1
            e += 1

        if invert:
            inv_n = inv_len[n.bit_length() - 1]
            for i in range(n):
                a[i] = a[i] * inv_n % mod

    def convolution(a, b):
        la, lb = len(a), len(b)
        res_len = la + lb - 1

        if la * lb <= 4096:
            res = [0] * res_len
            for i, ai in enumerate(a):
                if ai:
                    for j, bj in enumerate(b):
                        if bj:
                            res[i + j] = (res[i + j] + ai * bj) % MOD
            return res

        n = 1
        while n < res_len:
            n <<= 1

        fa = a + [0] * (n - la)
        fb = b + [0] * (n - lb)
        ntt(fa, False)
        ntt(fb, False)
        for i in range(n):
            fa[i] = fa[i] * fb[i] % MOD
        ntt(fa, True)
        return fa[:res_len]

    def add_cross(l, mid, rgt):
        left_cnt = mid - l
        right_cnt = rgt - mid

        if left_cnt * right_cnt <= 4096:
            for i in range(mid, rgt):
                ui = u[i]
                s = 0
                for j in range(l, mid):
                    s += G[j] * fact[ui - v[j]]
                add[i] = (add[i] + s) % MOD
            return

        base_v = v[l]

        src_len = v[mid - 1] - base_v + 1
        poly = [0] * src_len
        for j in range(l, mid):
            poly[v[j] - base_v] = G[j]

        # Only factorial indices that can actually occur are needed.
        t_min = u[mid] - v[mid - 1]
        t_max = u[rgt - 1] - base_v
        kernel = fact[t_min:t_max + 1]

        prod = convolution(poly, kernel)
        offset = base_v + t_min
        for i in range(mid, rgt):
            add[i] = (add[i] + prod[u[i] - offset]) % MOD

    def solve(l, rgt):
        if rgt - l == 1:
            val = (fact[u[l]] - add[l]) % MOD
            G[l] = val * invfact[u[l] - v[l]] % MOD
            return

        mid = (l + rgt) >> 1
        solve(l, mid)
        add_cross(l, mid, rgt)
        solve(mid, rgt)

    solve(0, r)

    bad = 0
    for i in range(r):
        bad = (bad + G[i] * fact[N - v[i]]) % MOD
    return (fact[N] - bad) % MOD


def main():
    sys.setrecursionlimit(1 << 20)
    data = sys.stdin.read().split()
    if not data:
        return

    N = int(data[0])
    S = data[1]

    # Cut after vertex 1 needs a black vertex on its left.
    # Cut before vertex 2N needs a white vertex on its right.
    if S[0] == "W" or S[-1] == "B":
        print(0)
        return

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # A[c] = maximum number of white vertices in a proper prefix
    # containing exactly c black vertices.
    A = [-1] * (N + 1)
    whites = 0
    blacks = 0

    # Proper prefixes only: cuts are between k and k+1 for 1 <= k < 2N.
    for ch in S[:-1]:
        if ch == "W":
            whites += 1
        else:
            blacks += 1
        if blacks:
            A[blacks] = whites

    constraints = []
    last_u = -1
    for c in range(1, N + 1):
        u = A[c]

        # max of c distinct positive ranks is at least c.
        if u < c:
            continue

        # For equal u, the earliest c gives the strongest constraint,
        # because prefix maxima are nondecreasing.
        if u != last_u:
            constraints.append((c, u))
            last_u = u

    print(count_good(N, constraints, fact, invfact))


if __name__ == "__main__":
    main()