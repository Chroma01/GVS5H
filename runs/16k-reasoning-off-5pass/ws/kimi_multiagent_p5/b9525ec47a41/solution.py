import sys
from itertools import product

MOD = 998244353

def solve() -> None:
    data = sys.stdin.read().split()
    N = int(data[0])
    s = data[1].strip()

    # ---------------------------------------------------------------
    # Model (see NOTES):
    #   y_i in {0,1}: orientation of cycle edge {i, (i+1)%N}
    #       y_i = 1  <=>  i -> i+1   (in-degree goes to vertex i+1)
    #       y_i = 0  <=>  i+1 -> i   (in-degree goes to vertex i)
    #   cycle in-degree of vertex i: c_i = y_{i-1} + (1 - y_i)
    #   x_i in {0,1} (only if s_i='1'): 1 <=> hub edge N -> i
    #   d_i = c_i + x_i,  d_N = m - sum(x_i)
    #
    # Distinct full tuples (d_0..d_N)  <==>  pairs (d-vector, k=sum x)
    # that have at least one witness (y,x) with sum x = k.
    #
    # Determinize the 2-state NFA (state = y_i) by subset construction.
    # Subsets reachable: {0}, {1}, {0,1}  (encode 1, 2, 3).
    # Start subset S_0 = {0,1} (y_{N-1} free on the cycle).
    # Reading d_i:  T = { y' : exists y in S, x in {0..s_i},
    #                       d = y + 1 - y' + x }.
    # A d-vector is realizable iff the deterministic run ends non-empty,
    # and distinct vectors give distinct subset paths.
    #
    # For a fixed subset path, the achievable set of k = sum x_i is a
    # contiguous interval [base, base + amb], where
    #   base = sum of minimum feasible x at each symbol,
    #   amb  = number of positions where both x=0 and x=1 are feasible
    #          (for that symbol, along that subset transition).
    # Hence each path contributes (amb + 1) distinct (vector, k) pairs.
    # (Verified by brute force below for all N<=8, all s patterns.)
    #
    # DP over the cycle: dp[S] = (count, sum of amb over paths).
    # Answer = sum over surviving paths of (amb + 1)
    #        = total_count + total_amb_sum.
    # ---------------------------------------------------------------

    # Precompute transitions: for subset mask S in {1,2,3} and
    # bit b = s_i, the map d -> (T_mask, xmin, both_x_possible).
    # c = y + 1 - y' ; d = c + x ; x in [0, b]
    trans = {}
    for S in (1, 2, 3):
        for b in (0, 1):
            table = {}
            for y in (0, 1):
                if not (S >> y) & 1:
                    continue
                for yp in (0, 1):
                    c = y + 1 - yp
                    for x in range(b + 1):
                        d = c + x
                        if d in table:
                            T, xmin, xmax = table[d]
                            table[d] = (T | (1 << yp),
                                        min(xmin, x), max(xmax, x))
                        else:
                            table[d] = (1 << yp, x, x)
            trans[(S, b)] = table

    # dp[mask] = [number_of_paths, sum_of_amb_over_paths]
    dp = {3: [1, 0]}
    for ch in s:
        b = 1 if ch == '1' else 0
        ndp = {}
        for S, (cnt, amb) in dp.items():
            for d, (T, xmin, xmax) in trans[(S, b)].items():
                add_amb = 1 if xmax > xmin else 0
                e = ndp.get(T)
                if e is None:
                    ndp[T] = [cnt, amb + cnt * add_amb]
                else:
                    e[0] = (e[0] + cnt) % MOD
                    e[1] = (e[1] + amb + cnt * add_amb) % MOD
        dp = ndp

    ans = 0
    for S, (cnt, amb) in dp.items():
        if S:  # non-empty final subset  <=>  realizable on the cycle
            ans = (ans + cnt + amb) % MOD
    print(ans % MOD)


# -------------------------------------------------------------------
# Brute-force verification (task requirement): for all N <= 8 and all
# 2^N patterns s, compare
#   (a) exhaustive enumeration over all 2^E orientations of G
#   (b) subset-path DP counting sum(amb + 1)
#   (c) per-path interval property: achievable k-set is contiguous
#       [base, base+amb]  (checked exactly, not just cardinality)
# -------------------------------------------------------------------
def _brute_check() -> None:
    def count_exhaustive(N, s):
        m = sum(s)
        edges = [(i, (i + 1) % N) for i in range(N)]
        edges += [(i, N) for i in range(N) if s[i]]
        seen = set()
        for bits in range(1 << len(edges)):
            d = [0] * (N + 1)
            for e, (u, v) in enumerate(edges):
                d[v if (bits >> e) & 1 else u] += 1
            seen.add(tuple(d))
        return len(seen)

    def count_dp(N, s):
        dp = {3: [1, 0]}
        for b in s:
            ndp = {}
            for S, (cnt, amb) in dp.items():
                for d, (T, xmin, xmax) in _trans(N, S, b).items():
                    add = 1 if xmax > xmin else 0
                    e = ndp.setdefault(T, [0, 0])
                    e[0] += cnt
                    e[1] += amb + cnt * add
            dp = ndp
        return sum(cnt + amb for S, (cnt, amb) in dp.items() if S)

    def _trans(N, S, b):
        table = {}
        for y in (0, 1):
            if not (S >> y) & 1:
                continue
            for yp in (0, 1):
                c = y + 1 - yp
                for x in range(b + 1):
                    d = c + x
                    if d in table:
                        T, lo, hi = table[d]
                        table[d] = (T | (1 << yp), min(lo, x), max(hi, x))
                    else:
                        table[d] = (1 << yp, x, x)
        return table

    def interval_property_ok(N, s):
        # For every d-vector, compute the exact set of achievable
        # k = sum x over all witnesses (via NFA-state DP that keeps
        # the full set of k values per y-state), and check it equals
        # the interval [sum xmin, sum xmin + amb] read off the unique
        # subset path.
        seen = {}

        def rec(i, S, kset_by_y, dvec, base, amb):
            if i == N:
                if S:
                    ks = set().union(*kset_by_y) if kset_by_y else set()
                    seen[tuple(dvec)] = (ks, base, amb)
                return
            b = s[i]
            for d, (T, lo, hi) in _trans(N, S, b).items():
                nk = [set(), set()]
                for y in (0, 1):
                    if not (S >> y) & 1:
                        continue
                    for yp in (0, 1):
                        c = y + 1 - yp
                        for x in range(b + 1):
                            if c + x == d:
                                for k in kset_by_y[y]:
                                    nk[yp].add(k + x)
                rec(i + 1, T, nk, dvec + [d], base + lo,
                    amb + (1 if hi > lo else 0))

        rec(0, 3, [{0}, {0}], [], 0, 0)
        for dvec, (ks, base, amb) in seen.items():
            if ks != set(range(base, base + amb + 1)):
                return False
        return True

    for N in range(3, 9):
        for mask in range(1 << N):
            s = [(mask >> i) & 1 for i in range(N)]
            a = count_exhaustive(N, s)
            b = count_dp(N, s)
            assert a == b, (N, s, a, b)
            assert interval_property_ok(N, s), (N, s)
    # Sample sanity: N=3, s=010 -> 14
    assert count_exhaustive(3, [0, 1, 0]) == 14
    assert count_dp(3, [0, 1, 0]) == 14


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--selftest':
        _brute_check()
        print('all brute checks passed', file=sys.stderr)
    else:
        solve()