import sys
sys.setrecursionlimit(1 << 25)


def sd_to_rc(s, d):
    return ((s + d) // 2, (s - d) // 2)


def all_red(R):
    # R even >= 2. 2 x k ring snake.
    if R == 2:
        return [('R', 1, 1), ('R', 1, 2)]
    k = R // 2
    ans = [('R', 1, c) for c in range(1, k + 1)]
    ans += [('R', 2, c) for c in range(k, 0, -1)]
    return ans


def all_blue(B):
    # B even >= 2. In (s,d)=(r+c,r-c) coords blue moves are axis steps of 2.
    if B == 2:
        return [('B', 1, 1), ('B', 2, 2)]
    b = B // 2 - 1
    pts = [(2 * i, 0) for i in range(0, b + 1)]
    pts += [(2 * i, 2) for i in range(b, -1, -1)]
    return [('B', (s + d) // 2 + 2, (s - d) // 2 + 2) for (s, d) in pts]


def diag_path(p1, p2, n, forbidden=frozenset()):
    """Diagonal path (steps (+-1,+-1)) from p1 to p2 in exactly n steps,
    avoiding `forbidden` cells (p2 itself is allowed).
    Requires |ds|,|dd| <= n and ds%2 == dd%2 == n%2."""
    (s1, d1) = p1
    (s2, d2) = p2
    ds = s2 - s1
    dd = d2 - d1
    assert abs(ds) <= n and abs(dd) <= n
    assert ds % 2 == n % 2 and dd % 2 == n % 2
    path = [(s1, d1)]
    s, d = s1, d1
    for step in range(n):
        left_after = n - step - 1
        a0 = 1 if s2 > s else (-1 if s2 < s else 0)
        b0 = 1 if d2 > d else (-1 if d2 < d else 0)
        prefs = []
        if a0 and b0:
            prefs.append((a0, b0))
        for cand in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            if cand not in prefs:
                prefs.append(cand)
        moved = False
        for (a, b) in prefs:
            ns, nd = s + a, d + b
            if abs(s2 - ns) <= left_after and abs(d2 - nd) <= left_after:
                if (ns, nd) in forbidden and (ns, nd) != (s2, d2):
                    continue
                s, d = ns, nd
                path.append((s, d))
                moved = True
                break
        assert moved, "diag_path stuck"
    assert path[-1] == (s2, d2)
    return path


def mixed(R, B):
    # R even >= 2, B >= 1. Work in (s,d)=(r+c,r-c):
    #   red move  = diagonal step (+-1,+-1)
    #   blue move = axis step (+-2,0) or (0,+-2)
    s0 = 4 * (R + B) + 10
    d0 = 4 * (R + B) + 10
    pts = []  # (type, s, d)
    if B >= R:
        # red staircase up-right
        for i in range(R):
            pts.append(('R', s0 + i, d0 + i))
        pts.append(('B', s0 + R, d0 + R))  # z0 (diagonal from last red)
        gap = B - R
        odd = (gap % 2 == 1)
        m = gap // 2
        # blue rectangle: right m, down, left back, axis-close to w0
        for i in range(1, m + 1):
            pts.append(('B', s0 + R + 2 * i, d0 + R))
        corner_s = s0 + R + 2 * m
        if not odd:
            # down R/2 to level d0, then left to (s0+2, d0)
            for j in range(1, R // 2 + 1):
                pts.append(('B', corner_s, d0 + R - 2 * j))
            s = corner_s - 2
            while s >= s0 + 2:
                pts.append(('B', s, d0))
                s -= 2
            # last blue (s0+2,d0) -> w0 (s0,d0): axis step
        else:
            # down R/2+1 to level d0-2, then left to (s0, d0-2)
            for j in range(1, R // 2 + 2):
                pts.append(('B', corner_s, d0 + R - 2 * j))
            s = corner_s - 2
            while s >= s0:
                pts.append(('B', s, d0 - 2))
                s -= 2
            # last blue (s0,d0-2) -> w0 (s0,d0): axis step
    else:
        # B < R
        if R == 2:
            # (R,B) = (2,1): R(1,1), B(2,1), R(1,2) in (r,c)
            pts = [('R', s0, d0), ('B', s0 + 1, d0 - 1), ('R', s0 + 1, d0 + 1)]
        else:
            pts.append(('R', s0, d0))          # w0, red run of length a=1
            pts.append(('B', s0 + 1, d0 + 1))  # z0, diagonal from w0
            k = min(R // 2 - 2, B - 1)         # blue down steps
            l = B - 1 - k                      # blue left steps
            for j in range(1, k + 1):
                pts.append(('B', s0 + 1, d0 + 1 - 2 * j))
            for i in range(1, l + 1):
                pts.append(('B', s0 + 1 - 2 * i, d0 + 1 - 2 * k))
            # last blue v=(s0+1-2l, d0+1-2k); red run2 starts axis-adjacent below
            v2 = (s0 + 1 - 2 * l, d0 - 2 * k - 1)
            w = (s0 - 1, d0 + 1)               # diagonal-adjacent to w0
            n = R - 2                          # steps v2 -> w
            forbidden = set((s, d) for (_, s, d) in pts)
            path = diag_path(v2, w, n, forbidden)
            for (s, d) in path:
                pts.append(('R', s, d))
            # last red w -> w0 diagonal closes the cycle
    ans = []
    for (typ, s, d) in pts:
        r, c = sd_to_rc(s, d)
        ans.append((typ, r, c))
    return ans


def validate(R, B, ans):
    assert ans is not None
    assert len(ans) == R + B, (R, B, len(ans))
    cntR = sum(1 for p in ans if p[0] == 'R')
    cntB = sum(1 for p in ans if p[0] == 'B')
    assert cntR == R and cntB == B, (R, B, cntR, cntB)
    cells = [(r, c) for (_, r, c) in ans]
    assert len(set(cells)) == len(cells), ("dup", R, B)
    for (_, r, c) in ans:
        assert 1 <= r <= 10 ** 9 and 1 <= c <= 10 ** 9, ("range", r, c)
    n = len(ans)
    for i in range(n):
        p1, r1, c1 = ans[i]
        _, r2, c2 = ans[(i + 1) % n]
        dr = abs(r1 - r2)
        dc = abs(c1 - c2)
        if p1 == 'R':
            assert dr + dc == 1, ("red adj", R, B, i, ans[i], ans[(i + 1) % n])
        else:
            assert dr == 1 and dc == 1, ("blue adj", R, B, i, ans[i], ans[(i + 1) % n])


def construct(R, B):
    if R % 2 == 1 or (R == 0 and B % 2 == 1):
        return None
    if B == 0:
        return all_red(R)
    if R == 0:
        return all_blue(B)
    return mixed(R, B)


def self_test():
    import random
    for R in range(0, 13):
        for B in range(0, 13):
            if R + B < 2:
                continue
            ans = construct(R, B)
            if ans is None:
                continue
            validate(R, B, ans)
    rng = random.Random(12345)
    for _ in range(300):
        R = rng.randrange(0, 2000)
        B = rng.randrange(0, 2000)
        if R + B < 2:
            continue
        ans = construct(R, B)
        if ans is None:
            continue
        validate(R, B, ans)
    for (R, B) in [(2, 199999), (199998, 3), (100000, 100000),
                   (2, 1), (2, 99999), (99998, 99999), (4, 3),
                   (199998, 1), (6, 5), (8, 1), (2, 5), (200000, 0),
                   (0, 200000), (0, 2), (2, 0)]:
        if R + B < 2:
            continue
        ans = construct(R, B)
        if ans is not None:
            validate(R, B, ans)


def solve():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out_lines = []
    idx = 1
    for _ in range(t):
        R = int(data[idx]); B = int(data[idx + 1]); idx += 2
        ans = construct(R, B)
        if ans is None:
            out_lines.append("No")
        else:
            out_lines.append("Yes")
            for (p, r, c) in ans:
                out_lines.append(f"{p} {r} {c}")
    sys.stdout.write("\n".join(out_lines) + "\n")


if __name__ == "__main__":
    import os
    if os.environ.get("SELFTEST"):
        self_test()
        print("ALL TESTS PASSED", file=sys.stderr)
    else:
        solve()