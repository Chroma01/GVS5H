import sys

INF = 1 << 60


def solve(N, K, X, Y, Z):
    M = 2 * K
    m = [0] * N
    base = [0] * N
    for i in range(N):
        x = X[i]; y = Y[i]; z = Z[i]
        if x >= y:
            if x >= z:
                m[i] = x; base[i] = 0
            else:
                m[i] = z; base[i] = 2
        else:
            if y >= z:
                m[i] = y; base[i] = 1
            else:
                m[i] = z; base[i] = 2

    order = sorted(range(N), key=lambda i: -m[i])
    sel = order[:M]
    unsel = order[M:]

    V = 0
    cnt = [0, 0, 0]
    for i in sel:
        V += m[i]
        cnt[base[i]] += 1

    if cnt[0] % 2 == 0 and cnt[1] % 2 == 0 and cnt[2] % 2 == 0:
        return V

    a = -1; b = -1
    for t in range(3):
        if cnt[t] & 1:
            if a < 0:
                a = t
            else:
                b = t
    c = 3 - a - b

    coord = (X, Y, Z)
    ca_arr = coord[a]; cb_arr = coord[b]; cc_arr = coord[c]

    sel_a = []; sel_b = []; sel_c = []
    for i in sel:
        bb = base[i]
        if bb == a:
            sel_a.append(i)
        elif bb == b:
            sel_b.append(i)
        else:
            sel_c.append(i)

    nsc = len(sel_c)
    nsu = len(unsel)
    hasU = nsu > 0

    minMA = min(m[i] for i in sel_a)
    minMB = min(m[i] for i in sel_b)
    minMC = min((m[i] for i in sel_c), default=INF)

    if hasU:
        maxUa = max(ca_arr[j] for j in unsel)
        maxUb = max(cb_arr[j] for j in unsel)
        maxUc = max(cc_arr[j] for j in unsel)
    else:
        maxUa = maxUb = maxUc = 0

    best = INF

    # ---- e1 : single op on edge {a,b} ----
    for i in sel_a:
        v = m[i] - cb_arr[i]
        if v < best: best = v
    for i in sel_b:
        v = m[i] - ca_arr[i]
        if v < best: best = v
    if hasU:
        v = minMA - maxUb
        if v < best: best = v
        v = minMB - maxUa
        if v < best: best = v

    # ---- e3 ops (edge {b,c}) ----
    B1 = INF
    for i in sel_b:
        v = m[i] - cc_arr[i]
        if v < B1: B1 = v
    B2list = sorted((m[p] - cb_arr[p], p) for p in sel_c)
    B2 = B2list[0][0] if B2list else INF
    B3 = (minMB - maxUc) if hasU else INF
    B4 = (minMC - maxUb) if (hasU and nsc > 0) else INF

    bestB = B1
    if B2 < bestB: bestB = B2
    if B3 < bestB: bestB = B3
    if B4 < bestB: bestB = B4

    # ---- e2 = A_recolor_a  (edge {a,c}) combined with any e3 ----
    minA1 = INF
    for i in sel_a:
        v = m[i] - cc_arr[i]
        if v < minA1: minA1 = v
    v = minA1 + bestB
    if v < best: best = v

    # ---- e2 = A_recolor_c  (one sel_c item p) ----
    if nsc > 0:
        mclist = sorted((m[p], p) for p in sel_c)
        for p in sel_c:
            cand = B1
            if B3 < cand: cand = B3
            if nsc >= 2:
                bex = B2list[1][0] if B2list[0][1] == p else B2list[0][0]
                if bex < cand: cand = bex
                if hasU:
                    mex = mclist[1][0] if mclist[0][1] == p else mclist[0][0]
                    w = mex - maxUb
                    if w < cand: cand = w
            v = m[p] - ca_arr[p] + cand
            if v < best: best = v

    # ---- e2 = A_swap_a  (drop min-m sel_a, add one unsel item j colored c) ----
    if hasU:
        ccl = sorted(((cc_arr[j], j) for j in unsel), reverse=True)
        cbl = sorted(((cb_arr[j], j) for j in unsel), reverse=True)
        for j in unsel:
            cand = B1
            if B2 < cand: cand = B2
            if nsu >= 2:
                u2 = ccl[1][0] if ccl[0][1] == j else ccl[0][0]
                w = minMB - u2
                if w < cand: cand = w
                if nsc > 0:
                    u1 = cbl[1][0] if cbl[0][1] == j else cbl[0][0]
                    w = minMC - u1
                    if w < cand: cand = w
            v = minMA - cc_arr[j] + cand
            if v < best: best = v

    # ---- e2 = A_swap_c  (drop a sel_c item p, add unsel item j colored a) ----
    if nsc > 0 and hasU:
        v = B1 + minMC - maxUa
        if v < best: best = v
        if nsc >= 2:
            tmp = INF
            for p in sel_c:
                bq = B2list[1][0] if B2list[0][1] == p else B2list[0][0]
                w = m[p] + bq
                if w < tmp: tmp = w
            v = tmp - maxUa
            if v < best: best = v
        if nsu >= 2:
            tmp = INF
            for j in unsel:
                u2 = ccl[1][0] if ccl[0][1] == j else ccl[0][0]
                w = minMB - u2 - ca_arr[j]
                if w < tmp: tmp = w
            v = minMC + tmp
            if v < best: best = v
        if nsc >= 2 and nsu >= 2:
            tmp1 = INF
            for p in sel_c:
                mq = mclist[1][0] if mclist[0][1] == p else mclist[0][0]
                w = m[p] + mq
                if w < tmp1: tmp1 = w
            tmp2 = INF
            for j in unsel:
                u1 = cbl[1][0] if cbl[0][1] == j else cbl[0][0]
                w = -ca_arr[j] - u1
                if w < tmp2: tmp2 = w
            v = tmp1 + tmp2
            if v < best: best = v

    return V - best


# ---------------------------------------------------------------------------
# brute force / stress / perf harness (only used when invoked with an argument)
# ---------------------------------------------------------------------------

def brute(N, K, cakes):
    full = 1 << N
    dp = [-1] * full
    dp[0] = 0
    pr = [[0] * N for _ in range(N)]
    for i in range(N):
        xi, yi, zi = cakes[i]
        for j in range(N):
            xj, yj, zj = cakes[j]
            pr[i][j] = max(xi + xj, yi + yj, zi + zj)
    allm = full - 1
    for mask in range(full):
        cur = dp[mask]
        if cur < 0:
            continue
        rem = allm ^ mask
        if rem == 0:
            continue
        lb = rem & -rem
        i = lb.bit_length() - 1
        r2 = rem ^ lb
        while r2:
            lb2 = r2 & -r2
            j = lb2.bit_length() - 1
            nm = mask | lb | lb2
            val = cur + pr[i][j]
            if val > dp[nm]:
                dp[nm] = val
            r2 ^= lb2
    target = 2 * K
    bestv = -1
    for mask in range(full):
        if bin(mask).count("1") == target and dp[mask] > bestv:
            bestv = dp[mask]
    return bestv


def _check(N, K, cakes, tag):
    X = [t[0] for t in cakes]
    Y = [t[1] for t in cakes]
    Z = [t[2] for t in cakes]
    got = solve(N, K, X, Y, Z)
    exp = brute(N, K, cakes)
    if got != exp:
        print("MISMATCH", tag, N, K, cakes, "expected", exp, "got", got)
        return False
    return True


def stress(iters=4000):
    import random, itertools
    binvals = list(itertools.product(range(2), repeat=3))
    for N in range(2, 6):
        for K in range(1, N // 2 + 1):
            for combo in itertools.product(binvals, repeat=N):
                if not _check(N, K, list(combo), "exh_bin"):
                    return
    tern = list(itertools.product(range(3), repeat=3))
    for combo in itertools.product(tern, repeat=3):
        if not _check(3, 1, list(combo), "exh_tern"):
            return
    print("exhaustive ok (binary N<=5, ternary N=3)")

    random.seed(987654321)
    for _ in range(iters):
        N = random.randint(2, 10)
        K = random.randint(1, N // 2)
        mode = random.randint(0, 5)
        cakes = []
        for i in range(N):
            if mode == 0:
                r = random.randint(0, 2); cakes.append((r, r, r))
            elif mode == 1:
                r = random.randint(0, 4)
                cakes.append((random.randint(0, r), random.randint(0, r), random.randint(0, r)))
            elif mode == 2:
                cakes.append((0, 0, 0))
            elif mode == 3:
                B = 10 ** 9
                cakes.append((random.randint(0, B), random.randint(0, B), random.randint(0, B)))
            elif mode == 4:
                dom = i % 3
                v = [random.randint(0, 4) for _ in range(3)]
                v[dom] += random.randint(3, 6)
                cakes.append(tuple(v))
            else:
                r = random.randint(0, 2)
                cakes.append((random.randint(0, r), random.randint(0, r), random.randint(0, r)))
        if random.random() < 0.3 and N >= 2:
            j = random.randrange(N)
            cakes[random.randrange(N)] = cakes[j]
        if not _check(N, K, cakes, "rand"):
            return
    print("all ok", iters)


def perf():
    import random, time
    random.seed(12345)
    T = 1000
    per = 100
    B = 10 ** 9
    cases = []
    for _ in range(T):
        N = per
        K = N // 2
        X = [random.randint(0, B) for _ in range(N)]
        Y = [random.randint(0, B) for _ in range(N)]
        Z = [random.randint(0, B) for _ in range(N)]
        cases.append((N, K, X, Y, Z))
    t0 = time.time()
    s = 0
    for (N, K, X, Y, Z) in cases:
        s += solve(N, K, X, Y, Z)
    t1 = time.time()
    print("perf: T=%d sumN=%d time=%.3fs checksum=%d" % (T, T * per, t1 - t0, s))


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    T = int(data[pos]); pos += 1
    out = []
    for _ in range(T):
        N = int(data[pos]); K = int(data[pos + 1]); pos += 2
        X = [0] * N; Y = [0] * N; Z = [0] * N
        for i in range(N):
            X[i] = int(data[pos]); Y[i] = int(data[pos + 1]); Z[i] = int(data[pos + 2])
            pos += 3
        out.append(str(solve(N, K, X, Y, Z)))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stress":
        stress()
    elif len(sys.argv) > 1 and sys.argv[1] == "perf":
        perf()
    else:
        main()