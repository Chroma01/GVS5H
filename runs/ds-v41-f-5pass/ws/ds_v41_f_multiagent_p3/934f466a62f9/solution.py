import sys
import heapq

INF = float('inf')
TOPREC = 6
TOPSEL = 6
TOPC = 6


def solve_one(N, K, X, Y, Z):
    M = [0] * N
    col = [0] * N
    for i in range(N):
        x = X[i]; y = Y[i]; z = Z[i]
        if x >= y:
            if x >= z:
                M[i] = x; col[i] = 0
            else:
                M[i] = z; col[i] = 2
        else:
            if y >= z:
                M[i] = y; col[i] = 1
            else:
                M[i] = z; col[i] = 2

    order = sorted(range(N), key=lambda i: -M[i])
    m2 = 2 * K
    sel = order[:m2]
    unsel = order[m2:]

    V = 0
    counts = [0, 0, 0]
    selfc = [[], [], []]
    for i in sel:
        c = col[i]
        counts[c] += 1
        V += M[i]
        selfc[c].append((M[i], X[i], Y[i], Z[i], i))

    odd = [c for c in range(3) if counts[c] & 1]
    if not odd:
        return V

    O = (odd[0], odd[1])
    others = [m for m in ((0, 1), (0, 2), (1, 2)) if m != O]
    Am = others[0]; Bm = others[1]

    unsval = [[], [], []]
    for i in unsel:
        unsval[0].append((X[i], i))
        unsval[1].append((Y[i], i))
        unsval[2].append((Z[i], i))
    for c in range(3):
        u = unsval[c]
        if len(u) > TOPC:
            u = heapq.nsmallest(TOPC, u, key=lambda t: -t[0])
        else:
            u = sorted(u, key=lambda t: -t[0])
        unsval[c] = u

    def gen(mask):
        p, q = mask
        ops = []
        lst = selfc[p]
        if lst:
            if len(lst) > TOPREC:
                rec = heapq.nsmallest(TOPREC, lst, key=lambda t: t[0] - t[1 + q])
            else:
                rec = sorted(lst, key=lambda t: t[0] - t[1 + q])
            for it in rec:
                ops.append((it[0] - it[1 + q], (it[4],)))
        lst = selfc[q]
        if lst:
            if len(lst) > TOPREC:
                rec = heapq.nsmallest(TOPREC, lst, key=lambda t: t[0] - t[1 + p])
            else:
                rec = sorted(lst, key=lambda t: t[0] - t[1 + p])
            for it in rec:
                ops.append((it[0] - it[1 + p], (it[4],)))

        def swaps(src, jlist):
            if not src or not jlist:
                return
            if len(src) > TOPSEL:
                rr = heapq.nsmallest(TOPSEL, src, key=lambda t: t[0])
            else:
                rr = sorted(src, key=lambda t: t[0])
            for r in rr:
                m = r[0]; ri = r[4]
                for j in jlist:
                    ops.append((m - j[0], (ri, j[1])))

        swaps(selfc[p], unsval[q])
        swaps(selfc[q], unsval[p])

        dd = {}
        for l, r in ops:
            if len(r) == 2 and r[0] > r[1]:
                key = (r[1], r[0])
            else:
                key = r
            if key not in dd or dd[key] > l:
                dd[key] = l
        return [(l, key) for key, l in dd.items()]

    def dis(a, b):
        if len(a) == 1:
            x = a[0]
            return x != b[0] and (len(b) == 1 or x != b[1])
        else:
            if len(b) == 1:
                y = b[0]
                return a[0] != y and a[1] != y
            else:
                return (a[0] != b[0] and a[0] != b[1]
                        and a[1] != b[0] and a[1] != b[1])

    single = INF
    for l, r in gen(O):
        if l < single:
            single = l

    opsA = gen(Am)
    opsB = gen(Bm)
    pair = INF
    for l1, r1 in opsA:
        for l2, r2 in opsB:
            if dis(r1, r2):
                s = l1 + l2
                if s < pair:
                    pair = s

    best = single if single < pair else pair
    return V - best


def brute(N, K, X, Y, Z):
    best = -1

    def price(i, j):
        a = X[i] + X[j]; b = Y[i] + Y[j]; c = Z[i] + Z[j]
        if a >= b and a >= c:
            return a
        return b if b >= c else c

    def rec(avail, k, total):
        nonlocal best
        if k == 0:
            if total > best:
                best = total
            return
        if len(avail) < 2 * k:
            return
        first = avail[0]
        rest = avail[1:]
        for idx in range(len(rest)):
            second = rest[idx]
            newavail = rest[:idx] + rest[idx + 1:]
            rec(newavail, k - 1, total + price(first, second))

    rec(list(range(N)), K, 0)
    return best


def run_stress():
    import random
    import itertools
    random.seed(987654321)

    def check(N, K, X, Y, Z, tag):
        a = solve_one(N, K, X, Y, Z)
        b = brute(N, K, X, Y, Z)
        if a != b:
            print("MISMATCH [" + tag + "] N=" + str(N) + " K=" + str(K))
            for i in range(N):
                print(X[i], Y[i], Z[i])
            print("solution =", a, " brute =", b)
            return False
        return True

    for N in (2, 3):
        for combo in itertools.product(list(itertools.product(range(3), repeat=3)), repeat=N):
            X = [c[0] for c in combo]; Y = [c[1] for c in combo]; Z = [c[2] for c in combo]
            for K in range(1, N // 2 + 1):
                if not check(N, K, X, Y, Z, "exhaustive"):
                    return
    print("exhaustive N<=3 vals<3: OK")

    N = 4
    for combo in itertools.product(list(itertools.product(range(2), repeat=3)), repeat=N):
        X = [c[0] for c in combo]; Y = [c[1] for c in combo]; Z = [c[2] for c in combo]
        for K in (1, 2):
            if not check(N, K, X, Y, Z, "exhaustive4"):
                return
    print("exhaustive N=4 vals<2: OK")

    for _ in range(30000):
        N = random.randint(2, 8)
        K = random.randint(1, N // 2)
        R = random.choice([1, 2, 3, 5, 8])
        X = [random.randint(0, R) for _ in range(N)]
        Y = [random.randint(0, R) for _ in range(N)]
        Z = [random.randint(0, R) for _ in range(N)]
        if not check(N, K, X, Y, Z, "random"):
            return
    print("random stress 30000: OK")

    for _ in range(15000):
        N = random.randint(2, 8)
        K = random.randint(1, N // 2)
        base = [random.randint(0, 3) for _ in range(3)]
        X = []; Y = []; Z = []
        for i in range(N):
            if random.random() < 0.6:
                X.append(base[0]); Y.append(base[1]); Z.append(base[2])
            else:
                X.append(random.randint(0, 3))
                Y.append(random.randint(0, 3))
                Z.append(random.randint(0, 3))
        if not check(N, K, X, Y, Z, "dup"):
            return
    print("duplicate/tie stress 15000: OK")

    for _ in range(4000):
        N = random.randint(2, 10)
        K = random.randint(1, N // 2)
        R = random.choice([4, 6, 10])
        X = [random.randint(0, R) for _ in range(N)]
        Y = [random.randint(0, R) for _ in range(N)]
        Z = [random.randint(0, R) for _ in range(N)]
        if not check(N, K, X, Y, Z, "extended"):
            return
    print("extended stress N<=10: OK")

    print("ALL TESTS PASSED")


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        run_stress()
        return
    idx = 0
    T = int(data[idx]); idx += 1
    out = []
    for _ in range(T):
        N = int(data[idx]); K = int(data[idx + 1]); idx += 2
        X = [0] * N; Y = [0] * N; Z = [0] * N
        for i in range(N):
            X[i] = int(data[idx]); Y[i] = int(data[idx + 1]); Z[i] = int(data[idx + 2])
            idx += 3
        out.append(str(solve_one(N, K, X, Y, Z)))
    sys.stdout.write("\n".join(out) + "\n")


main()