import sys
import random
import time


class Solution:
    _cache = None

    @staticmethod
    def _build():
        C2, C3, C5, C7 = 6, 4, 2, 2
        S2, S3, S5, S7 = C2 + 1, C3 + 1, C5 + 1, C7 + 1

        def idx(x, y, z, w):
            return ((x * S3 + y) * S5 + z) * S7 + w

        SIZE = S2 * S3 * S5 * S7

        E = [(0, 0, 0, 0)] * 10
        E[1] = (0, 0, 0, 0); E[2] = (1, 0, 0, 0); E[3] = (0, 1, 0, 0)
        E[4] = (2, 0, 0, 0); E[5] = (0, 0, 1, 0); E[6] = (1, 1, 0, 0)
        E[7] = (0, 0, 0, 1); E[8] = (3, 0, 0, 0); E[9] = (0, 2, 0, 0)

        need = [None] * 82
        for s in range(1, 82):
            t = s
            a = b = c = d = 0
            while t % 2 == 0:
                a += 1; t //= 2
            while t % 3 == 0:
                b += 1; t //= 3
            while t % 5 == 0:
                c += 1; t //= 5
            while t % 7 == 0:
                d += 1; t //= 7
            if t == 1:
                need[s] = (a, b, c, d)

        MAXLEN = 9

        freecnt = [None] * (MAXLEN + 1)
        base = [0] * SIZE
        base[idx(0, 0, 0, 0)] = 1
        freecnt[0] = {0: base}
        for k in range(MAXLEN):
            cur = {}
            for sm, cnt in freecnt[k].items():
                for dg in range(1, 10):
                    ns = sm + dg
                    arr = cur.get(ns)
                    if arr is None:
                        arr = [0] * SIZE
                        cur[ns] = arr
                    a2, a3, a5, a7 = E[dg]
                    for x in range(S2):
                        nx = x + a2
                        if nx > C2:
                            nx = C2
                        for y in range(S3):
                            ny = y + a3
                            if ny > C3:
                                ny = C3
                            for z in range(S5):
                                nz = z + a5
                                if nz > C5:
                                    nz = C5
                                bi = idx(x, y, z, 0)
                                bo = idx(nx, ny, nz, 0)
                                for w in range(S7):
                                    v = cnt[bi + w]
                                    if v:
                                        nw = w + a7
                                        if nw > C7:
                                            nw = C7
                                        arr[bo + nw] += v
            freecnt[k + 1] = cur

        freeD = [None] * (MAXLEN + 1)
        for k in range(MAXLEN + 1):
            dct = {}
            for sm, cnt in freecnt[k].items():
                D = cnt[:]
                for x in range(S2):
                    for y in range(S3):
                        for z in range(S5):
                            b0 = idx(x, y, z, 0)
                            for w in range(C7 - 1, -1, -1):
                                D[b0 + w] += D[b0 + w + 1]
                for x in range(S2):
                    for y in range(S3):
                        for z in range(C5 - 1, -1, -1):
                            for w in range(S7):
                                D[idx(x, y, z, w)] += D[idx(x, y, z + 1, w)]
                for x in range(S2):
                    for y in range(C3 - 1, -1, -1):
                        for z in range(S5):
                            for w in range(S7):
                                D[idx(x, y, z, w)] += D[idx(x, y + 1, z, w)]
                for x in range(C2 - 1, -1, -1):
                    for y in range(S3):
                        for z in range(S5):
                            for w in range(S7):
                                D[idx(x, y, z, w)] += D[idx(x + 1, y, z, w)]
                dct[sm] = D
            freeD[k] = dct

        B = [0] * (MAXLEN + 1)
        for m in range(1, MAXLEN + 1):
            tot = 0
            for sm, D in freeD[m].items():
                nd = need[sm]
                if nd is not None:
                    tot += D[idx(nd[0], nd[1], nd[2], nd[3])]
            B[m] = tot

        pow9 = [1] * (MAXLEN + 1)
        for i in range(1, MAXLEN + 1):
            pow9[i] = pow9[i - 1] * 9

        return dict(C2=C2, C3=C3, C5=C5, C7=C7, idx=idx, E=E, need=need,
                    freeD=freeD, B=B, pow9=pow9, MAXLEN=MAXLEN)

    def beautifulNumbers(self, l: int, r: int) -> int:
        if Solution._cache is None:
            Solution._cache = Solution._build()
        c = Solution._cache
        C2 = c["C2"]; C3 = c["C3"]; C5 = c["C5"]; C7 = c["C7"]
        idx = c["idx"]; E = c["E"]; need = c["need"]
        freeD = c["freeD"]; B = c["B"]; pow9 = c["pow9"]; MAXLEN = c["MAXLEN"]

        def count_up_to(x):
            if x <= 0:
                return 0
            ds = list(map(int, str(x)))
            n = len(ds)

            z = 0
            for m in range(1, n):
                z += pow9[m]
            pos = n
            for i in range(n):
                if ds[i] == 0:
                    pos = i
                    break
                ce = ds[i] - 1
                if ce > 0:
                    z += ce * pow9[n - 1 - i]
            if pos == n:
                z += 1

            res = x - z
            for m in range(1, n):
                res += B[m]

            ps = 0
            pe2 = pe3 = pe5 = pe7 = 0
            broken = False
            for i in range(n):
                di = ds[i]
                k = n - 1 - i
                if di > 1:
                    fd = freeD[k]
                    for e in range(1, di):
                        a2, a3, a5, a7 = E[e]
                        px = pe2 + a2; py = pe3 + a3
                        pz = pe5 + a5; pw = pe7 + a7
                        sbase = ps + e
                        for fsum, D in fd.items():
                            s = sbase + fsum
                            if s > 81:
                                continue
                            nd = need[s]
                            if nd is None:
                                continue
                            rx = nd[0] - px
                            if rx < 0: rx = 0
                            ry = nd[1] - py
                            if ry < 0: ry = 0
                            rz = nd[2] - pz
                            if rz < 0: rz = 0
                            rw = nd[3] - pw
                            if rw < 0: rw = 0
                            if rx <= C2 and ry <= C3 and rz <= C5 and rw <= C7:
                                res += D[idx(rx, ry, rz, rw)]
                if di == 0:
                    broken = True
                    break
                ps += di
                a2, a3, a5, a7 = E[di]
                pe2 += a2
                if pe2 > C2: pe2 = C2
                pe3 += a3
                if pe3 > C3: pe3 = C3
                pe5 += a5
                if pe5 > C5: pe5 = C5
                pe7 += a7
                if pe7 > C7: pe7 = C7

            if not broken and 1 <= ps <= 81:
                nd = need[ps]
                if nd is not None and pe2 >= nd[0] and pe3 >= nd[1] and pe5 >= nd[2] and pe7 >= nd[3]:
                    res += 1
            return res

        return count_up_to(r) - count_up_to(l - 1)


def brute_is_beautiful(n):
    s = 0
    p = 1
    while n:
        d = n % 10
        s += d
        p *= d
        n //= 10
    return p % s == 0


def brute_range(l, r):
    c = 0
    for n in range(l, r + 1):
        if brute_is_beautiful(n):
            c += 1
    return c


def main():
    sol = Solution()
    random.seed(20240115)
    fails = []

    print("=== test script (auto) ===")

    for l, r, exp in [(10, 20, 2), (1, 15, 10)]:
        t0 = time.time()
        got = sol.beautifulNumbers(l, r)
        dt = time.time() - t0
        ok = got == exp
        print(f"[1] example ({l},{r}) got={got} exp={exp} {'PASS' if ok else 'FAIL'} ({dt:.3f}s)")
        if not ok:
            fails.append(("example", l, r, got, exp))

    N = 3000
    bp = [0] * (N + 1)
    for n in range(1, N + 1):
        bp[n] = bp[n - 1] + (1 if brute_is_beautiful(n) else 0)

    t0 = time.time()
    mism = 0
    for x in range(1, N + 1):
        got = sol.beautifulNumbers(1, x)
        if got != bp[x]:
            mism += 1
            if len(fails) < 40:
                fails.append(("prefix", 1, x, got, bp[x]))
    dt = time.time() - t0
    print(f"[2] exhaustive prefix 1..{N}: {'PASS' if mism == 0 else 'FAIL ' + str(mism)} ({dt:.2f}s)")

    m3 = 0
    for _ in range(5):
        l = random.randint(1, 3000)
        r = random.randint(l, 3000)
        got = sol.beautifulNumbers(l, r)
        exp = bp[r] - bp[l - 1]
        ok = got == exp
        print(f"[3] range ({l},{r}) got={got} exp={exp} {'PASS' if ok else 'FAIL'}")
        if not ok:
            m3 += 1
            fails.append(("range", l, r, got, exp))

    large = [(999000000, 999999999), (999999900, 999999999)]
    lr = random.randint(1, 10 ** 9 - 200001)
    large.append((lr, lr + 200000))
    for (l, r) in large:
        t0 = time.time()
        got = sol.beautifulNumbers(l, r)
        dt = time.time() - t0
        exp = brute_range(l, r)
        ok = got == exp
        print(f"[4] large ({l},{r}) len={r - l + 1} got={got} exp={exp} "
              f"{'PASS' if ok else 'FAIL'} ({dt:.3f}s)")
        if not ok:
            fails.append(("large", l, r, got, exp))

    t0 = time.time()
    v = sol.beautifulNumbers(1, 10 ** 9 - 1)
    dt = time.time() - t0
    print(f"[t] beautifulNumbers(1,10**9-1) = {v}  time={dt:.3f}s")

    print("=== done ===")
    if fails:
        print("FAILURES:")
        for f in fails:
            print("   ", f)
        print(f"OVERALL: FAIL ({len(fails)} checks)")
        return 1
    print("OVERALL: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())