import sys
import itertools
import random
import time

HARDCODED = ((1, 1), (1, 2), (4, 4), (2, 4))


def reduce_count(x, T, m):
    if x >= T + m:
        return T + ((x - T) % m)
    return x


def build_trans(BASE):
    B2 = BASE * BASE
    B3 = B2 * BASE
    trans = []

    def add(x, y, res, tog):
        need = [0, 0, 0, 0]
        delta = [0, 0, 0, 0]
        need[x] += 1
        need[y] += 1
        delta[x] -= 1
        delta[y] -= 1
        delta[res] += 1
        off = delta[0] * B3 + delta[1] * B2 + delta[2] * BASE + delta[3]
        trans.append((need[0], need[1], need[2], need[3],
                      delta[0], delta[1], delta[2], delta[3], off, tog))

    add(0, 0, 0, 1)   # A+A -> A, p^=1
    add(0, 1, 1, 1)   # A+B -> B, p^=1
    add(0, 2, 2, 1)   # A+C -> C, p^=1
    add(0, 3, 2, 1)   # A+I -> C, p^=1
    add(1, 1, 0, 1)   # B+B -> A, p^=1
    add(1, 2, 2, 0)   # B+C -> C, p^=0
    add(1, 3, 2, 0)   # B+I -> C, p^=0
    add(2, 2, 0, 1)   # C+C -> A, p^=1
    add(2, 2, 1, 0)   # C+C -> B, p^=0
    add(2, 3, 0, 1)   # C+I -> A, p^=1
    add(2, 3, 1, 0)   # C+I -> B, p^=0
    add(3, 3, 1, 0)   # I+I -> B, p^=0
    return trans


def compute_dp(Kmax=30, verify=False, opts=HARDCODED, return_states=False):
    BASE = Kmax + 1
    B2 = BASE * BASE
    B3 = B2 * BASE
    size = B3 * BASE
    dp0 = bytearray(size)
    dp1 = bytearray(size)
    trans = build_trans(BASE)
    states = [] if return_states else None
    mism = 0

    for K in range(Kmax + 1):
        for a in range(K + 1):
            aB3 = a * B3
            for b in range(K - a + 1):
                abB2 = aB3 + b * B2
                for c in range(K - a - b + 1):
                    i = K - a - b - c
                    if (c + i) & 1:
                        continue
                    key = abB2 + c * BASE + i

                    f = 0
                    for n0, n1, n2, n3, d0, d1, d2, d3, off, tog in trans:
                        if a >= n0 and b >= n1 and c >= n2 and i >= n3:
                            tkey = key + off
                            if (dp0[tkey] if tog == 0 else dp1[tkey]) == 0:
                                f = 1
                                break
                    dp0[key] = f

                    g = 0
                    if a + b + c > 0 and f == 0:
                        g = 1
                    else:
                        for n0, n1, n2, n3, d0, d1, d2, d3, off, tog in trans:
                            if a >= n0 and b >= n1 and c >= n2 and i >= n3:
                                tkey = key + off
                                if (dp1[tkey] if tog == 0 else dp0[tkey]) == 0:
                                    g = 1
                                    break
                    dp1[key] = g

                    if return_states:
                        states.append((a, b, c, i, key))

                    if verify and opts is not None:
                        ra = reduce_count(a, opts[0][0], opts[0][1])
                        rb = reduce_count(b, opts[1][0], opts[1][1])
                        rc = reduce_count(c, opts[2][0], opts[2][1])
                        ri = reduce_count(i, opts[3][0], opts[3][1])
                        if ra != a or rb != b or rc != c or ri != i:
                            rkey = ra * B3 + rb * B2 + rc * BASE + ri
                            if dp0[rkey] != f or dp1[rkey] != g:
                                mism += 1

    if return_states:
        return dp0, dp1, BASE, B2, B3, states, mism
    return dp0, dp1, BASE, B2, B3, mism


def verify_reduction(opts, dp0, dp1, BASE, B2, B3):
    trans = build_trans(BASE)
    R = []
    S = []
    for t, (T, m) in enumerate(opts):
        R.append(T + m - 1)
        s = set(range(0, R[t] + 1))
        for r in range(T, R[t] + 1):
            s.add(r + m)
            if m == 1:
                s.add(r + 2 * m)
        S.append(sorted(s))

    prod = 1
    for s in S:
        prod *= len(s)
    if prod > 500000:
        return False

    max_total = max(S[0]) + max(S[1]) + max(S[2]) + max(S[3])
    if max_total > BASE - 1:
        return False

    T0, m0 = opts[0]
    T1, m1 = opts[1]
    T2, m2 = opts[2]
    T3, m3 = opts[3]

    for a in S[0]:
        for b in S[1]:
            for c in S[2]:
                for i in S[3]:
                    if (c + i) & 1:
                        continue

                    f = 0
                    for n0, n1, n2, n3, d0, d1, d2, d3, off, tog in trans:
                        if a >= n0 and b >= n1 and c >= n2 and i >= n3:
                            ta = a + d0
                            tb = b + d1
                            tc = c + d2
                            ti = i + d3
                            ra = reduce_count(ta, T0, m0)
                            rb = reduce_count(tb, T1, m1)
                            rc = reduce_count(tc, T2, m2)
                            ri = reduce_count(ti, T3, m3)
                            tkey = ra * B3 + rb * B2 + rc * BASE + ri
                            if (dp0[tkey] if tog == 0 else dp1[tkey]) == 0:
                                f = 1
                                break
                    L = f

                    g = 0
                    if a + b + c > 0 and L == 0:
                        g = 1
                    else:
                        for n0, n1, n2, n3, d0, d1, d2, d3, off, tog in trans:
                            if a >= n0 and b >= n1 and c >= n2 and i >= n3:
                                ta = a + d0
                                tb = b + d1
                                tc = c + d2
                                ti = i + d3
                                ra = reduce_count(ta, T0, m0)
                                rb = reduce_count(tb, T1, m1)
                                rc = reduce_count(tc, T2, m2)
                                ri = reduce_count(ti, T3, m3)
                                tkey = ra * B3 + rb * B2 + rc * BASE + ri
                                if (dp1[tkey] if tog == 0 else dp0[tkey]) == 0:
                                    g = 1
                                    break
                    H = g

                    ra = reduce_count(a, T0, m0)
                    rb = reduce_count(b, T1, m1)
                    rc = reduce_count(c, T2, m2)
                    ri = reduce_count(i, T3, m3)
                    rkey = ra * B3 + rb * B2 + rc * BASE + ri

                    if dp0[rkey] != L or dp1[rkey] != H:
                        return False
    return True


def s_size(T, m):
    R = T + m - 1
    s = set(range(0, R + 1))
    for r in range(T, R + 1):
        s.add(r + m)
        if m == 1:
            s.add(r + 2 * m)
    return len(s)


def empirical_pass(t, T, m, states, dp0, dp1, BASE, B2, B3):
    threshold = T + m
    base = (B3, B2, BASE, 1)[t]
    for a, b, c, i, key in states:
        if t == 0:
            x = a
        elif t == 1:
            x = b
        elif t == 2:
            x = c
        else:
            x = i
        if x >= threshold:
            tkey = key - m * base
            if dp0[key] != dp0[tkey] or dp1[key] != dp1[tkey]:
                return False
    return True


def generate_candidates(t, states, dp0, dp1, BASE, B2, B3, maxR=15):
    cands = []
    for m in (1, 2, 3, 4, 6, 8):
        if t in (2, 3) and (m & 1):
            continue
        for T in range(0, m + 3):
            R = T + m - 1
            if R > maxR:
                continue
            if empirical_pass(t, T, m, states, dp0, dp1, BASE, B2, B3):
                cands.append((T, m))
    cands.sort(key=lambda x: (x[0] + x[1] - 1, x[0], x[1]))
    return cands[:8]


def find_verified_opts(states, dp0, dp1, BASE, B2, B3):
    cand_lists = []
    for t in range(4):
        lst = generate_candidates(t, states, dp0, dp1, BASE, B2, B3)
        if not lst:
            if t == 0:
                lst = [(1, 1)]
            elif t == 1:
                lst = [(1, 2)]
            elif t == 2:
                lst = [(4, 4)]
            else:
                lst = [(2, 4)]
        cand_lists.append(lst[:8])

    cache = {}
    checked = 0
    for combo in itertools.product(*cand_lists):
        totalR = 0
        prod = 1
        ok = True
        for T, m in combo:
            totalR += T + m - 1
            prod *= s_size(T, m)
            if totalR > 24 or prod > 200000:
                ok = False
                break
        if not ok:
            continue
        if combo in cache:
            continue
        cache[combo] = verify_reduction(combo, dp0, dp1, BASE, B2, B3)
        checked += 1
        if cache[combo]:
            return combo
        if checked >= 200:
            break
    return None


_solver_cache = None


def get_solver():
    global _solver_cache
    if _solver_cache is not None:
        return _solver_cache

    dp0, dp1, BASE, B2, B3, states, mism = compute_dp(
        30, verify=True, opts=HARDCODED, return_states=True
    )
    opts = HARDCODED
    if mism != 0 or not verify_reduction(opts, dp0, dp1, BASE, B2, B3):
        found = find_verified_opts(states, dp0, dp1, BASE, B2, B3)
        if found is not None:
            opts = found

    _solver_cache = (dp0, dp1, BASE, B2, B3, opts)
    return _solver_cache


def classify_components(N, edges):
    adj = [[] for _ in range(N)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    color = [-1] * N
    cntA = cntB = cntC = cntI = 0

    for s in range(N):
        if color[s] != -1:
            continue
        color[s] = 0
        stack = [s]
        c0 = 1
        c1 = 0

        while stack:
            v = stack.pop()
            cv = color[v]
            for to in adj[v]:
                if color[to] == -1:
                    color[to] = cv ^ 1
                    if color[to] == 0:
                        c0 += 1
                    else:
                        c1 += 1
                    stack.append(to)

        if c0 + c1 == 1:
            cntI += 1
        else:
            if (c0 & 1) and (c1 & 1):
                cntB += 1
            elif (not (c0 & 1)) and (not (c1 & 1)):
                cntA += 1
            else:
                cntC += 1

    return cntA, cntB, cntC, cntI


def solve_case(N, M, edges):
    if N & 1:
        return "Aoki" if (M & 1) else "Takahashi"

    dp0, dp1, BASE, B2, B3, opts = get_solver()
    a, b, c, i = classify_components(N, edges)

    p = (b + M) & 1

    a = reduce_count(a, opts[0][0], opts[0][1])
    b = reduce_count(b, opts[1][0], opts[1][1])
    c = reduce_count(c, opts[2][0], opts[2][1])
    i = reduce_count(i, opts[3][0], opts[3][1])

    key = a * B3 + b * B2 + c * BASE + i
    win = dp1[key] if p else dp0[key]
    return "Aoki" if win else "Takahashi"


def main():
    vals = list(map(int, sys.stdin.buffer.read().split()))
    if not vals:
        return

    N = vals[0]
    M = vals[1]

    if N & 1:
        print("Aoki" if (M & 1) else "Takahashi")
        return

    edges = [(vals[idx] - 1, vals[idx + 1] - 1) for idx in range(2, 2 + 2 * M, 2)]
    del vals
    print(solve_case(N, M, edges))


# Optional stress tests: run with `python program.py --test`
def _brute_all_small(N):
    pairs = [(i, j) for i in range(N) for j in range(i + 1, N)]
    E = len(pairs)
    legal = bytearray(1 << E)

    for mask in range(1 << E):
        adj = [[] for _ in range(N)]
        for idx, (u, v) in enumerate(pairs):
            if (mask >> idx) & 1:
                adj[u].append(v)
                adj[v].append(u)

        color = [-1] * N
        ok = True
        for s in range(N):
            if color[s] == -1:
                color[s] = 0
                stack = [s]
                while stack:
                    v = stack.pop()
                    cv = color[v]
                    for to in adj[v]:
                        if color[to] == -1:
                            color[to] = cv ^ 1
                            stack.append(to)
                        elif color[to] == cv:
                            ok = False
                            break
                    if not ok:
                        break
            if not ok:
                break
        legal[mask] = 1 if ok else 0

    memo = {}

    def win(mask):
        if mask in memo:
            return memo[mask]
        for idx in range(E):
            if not (mask >> idx) & 1:
                nm = mask | (1 << idx)
                if legal[nm]:
                    if not win(nm):
                        memo[mask] = True
                        return True
        memo[mask] = False
        return False

    return pairs, legal, win


_brute_cache = {}


def _get_brute(N):
    if N in _brute_cache:
        return _brute_cache[N]

    pairs = [(i, j) for i in range(N) for j in range(i + 1, N)]
    E = len(pairs)
    bip_cache = {}
    win_memo = {}

    def is_bip(m):
        if m in bip_cache:
            return bip_cache[m]

        adj = [[] for _ in range(N)]
        for idx, (u, v) in enumerate(pairs):
            if (m >> idx) & 1:
                adj[u].append(v)
                adj[v].append(u)

        color = [-1] * N
        ok = True
        for s in range(N):
            if color[s] == -1:
                color[s] = 0
                stack = [s]
                while stack:
                    v = stack.pop()
                    cv = color[v]
                    for to in adj[v]:
                        if color[to] == -1:
                            color[to] = cv ^ 1
                            stack.append(to)
                        elif color[to] == cv:
                            ok = False
                            break
                    if not ok:
                        break
            if not ok:
                break

        bip_cache[m] = ok
        return ok

    def win(m):
        if m in win_memo:
            return win_memo[m]
        for idx in range(E):
            if not (m >> idx) & 1:
                nm = m | (1 << idx)
                if is_bip(nm):
                    if not win(nm):
                        win_memo[m] = True
                        return True
        win_memo[m] = False
        return False

    _brute_cache[N] = (pairs, win)
    return _brute_cache[N]


def run_stress_tests():
    # Samples
    assert solve_case(4, 3, [(0, 1), (1, 2), (2, 3)]) == "Aoki"
    assert solve_case(4, 2, [(0, 1), (2, 3)]) == "Takahashi"
    assert solve_case(9, 5, [(1, 8), (1, 2), (3, 5), (4, 6), (0, 7)]) == "Aoki"

    # Edge cases
    assert solve_case(1, 0, []) == "Takahashi"
    assert solve_case(2, 0, []) == "Aoki"
    assert solve_case(2, 1, [(0, 1)]) == "Takahashi"
    assert solve_case(4, 0, []) == "Takahashi"
    assert solve_case(4, 4, [(0, 2), (0, 3), (1, 2), (1, 3)]) == "Takahashi"
    assert solve_case(4, 3, [(0, 1), (0, 2), (0, 3)]) == "Takahashi"
    assert solve_case(6, 0, []) == "Aoki"

    # Exhaustive bipartite graphs for N <= 5
    for N in range(1, 6):
        pairs, legal, win = _brute_all_small(N)
        E = len(pairs)
        for mask in range(1 << E):
            if not legal[mask]:
                continue
            edges = [pairs[idx] for idx in range(E) if (mask >> idx) & 1]
            expected = "Aoki" if win(mask) else "Takahashi"
            got = solve_case(N, len(edges), edges)
            if expected != got:
                raise AssertionError(
                    f"mismatch N={N} mask={mask} expected={expected} got={got}"
                )

    # Random bipartite graphs for N <= 7
    random.seed(12345)
    for _ in range(8):
        N = random.randint(1, 7)
        colors = [random.randint(0, 1) for _ in range(N)]
        pairs, win = _get_brute(N)
        E = len(pairs)
        mask = 0
        for idx, (u, v) in enumerate(pairs):
            if colors[u] != colors[v] and random.random() < 0.25:
                mask |= 1 << idx
        edges = [pairs[idx] for idx in range(E) if (mask >> idx) & 1]
        expected = "Aoki" if win(mask) else "Takahashi"
        got = solve_case(N, len(edges), edges)
        if expected != got:
            raise AssertionError(
                f"random mismatch N={N} mask={mask} expected={expected} got={got}"
            )

    # Cross-check hardcoded reduction against exact component-game DP up to 60
    dp0, dp1, BASE, B2, B3, mism = compute_dp(60, verify=True, opts=HARDCODED)
    assert mism == 0, f"DP60 reduction mismatches: {mism}"
    assert verify_reduction(HARDCODED, dp0, dp1, BASE, B2, B3)

    # Performance test
    N = 200000
    edges = [(i, i + 1) for i in range(N - 1)]
    t0 = time.time()
    solve_case(N, N - 1, edges)
    print(f"performance N={N} M={N - 1} time={time.time() - t0:.3f}s")
    print("all stress tests passed")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_stress_tests()
    else:
        main()