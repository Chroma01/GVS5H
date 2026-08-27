import sys
from itertools import product

sys.setrecursionlimit(1 << 25)
MOD = 998244353


# =====================================================================
#  Solver via GF(2) corner-coloring reduction + propagation
#
#  Reduction:
#   * Valid placements  <=>  spanning 2-regular subgraphs of the toroidal
#     cell-grid graph, "turn" at A-cells, "straight" at B-cells.
#   * Such an edge set is the boundary of a 2-coloring of the corner
#     lattice; the 4 winding sectors of the torus are covered by 4 twist
#     boundary conditions (p, q).  Each coloring pair {x, complement}
#     gives one edge set, so answer = (sum over sectors)/2.
#   * Cell (i,j) with corners a=x(i,j) b=x(i,j+1) c=x(i+1,j) d=x(i+1,j+1):
#       A:  a^b^c^d = 1            (3-1 split  <=> adjacent edges)
#       B:  a^d = 1  AND  b^c = 1  (diagonal anti-equality)
#
#  Propagation: given corner row 0 and column 0 (H+W-1 free initials),
#  every cell determines the opposite corner; B-cells additionally
#  impose b^c=1.  Wrap constraints close the torus with twists (p,q).
#  All constraints are parity constraints on the initials; solved by
#  Gaussian elimination on big-int bitsets.
#
#  Optimization: the *masks* of every corner form are independent of the
#  twist sector (p,q) - only the constant bits change.  So we propagate
#  masks ONCE, cache them, and per sector only recompute constants
#  (plain ints) and redo the (cheap) elimination.
# =====================================================================


def solve_case(H, W, grid):
    n0 = H + W - 1  # number of initial (free) variables

    # ---------------- pass 1: propagate masks (sector independent) ---
    # id 0 -> x(0,0);  id j -> x(0,j) (1<=j<=W-1);  id W+i-1 -> x(i,0)
    prev = [0] * (W + 1)
    prev[0] = 1
    for j in range(1, W):
        prev[j] = 1 << j

    row_masks = []          # row_masks[i] = masks of corner row i+1
    bcheck_mask = []        # mask of each B-check constraint (b ^ c)
    hwrap_mask = []         # mask of each horizontal wrap constraint
    for i in range(H):
        Si = grid[i]
        if i + 1 <= H - 1:
            lm = 1 << (W + i)
        else:               # x(H,0) = x(0,0) ^ p
            lm = 1
        cur = [0] * (W + 1)
        cur[0] = lm
        for j in range(W):
            a = prev[j]
            b = prev[j + 1]
            c = cur[j]
            if Si[j] == 'A':
                d = a ^ b ^ c
            else:
                d = a
                bcheck_mask.append(b ^ c)
            cur[j + 1] = d
        hwrap_mask.append(cur[W] ^ cur[0])
        row_masks.append(cur)
        prev = cur

    top_mask = [0] * (W + 1)   # corner row 0 (with x(0,W)=x(0,0)^q)
    top_mask[0] = 1
    for j in range(1, W):
        top_mask[j] = 1 << j
    top_mask[W] = 1

    # ---------------- per-sector: constants + elimination ------------
    def count_sector(p, q):
        # constants of corner row 0
        prev_c = [0] * (W + 1)
        prev_c[W] = q
        basis = {}
        ncons = 0

        def add(mask, rhs):
            nonlocal ncons
            m = mask
            r = rhs
            while m:
                piv = m.bit_length() - 1
                e = basis.get(piv)
                if e is None:
                    basis[piv] = (m, r)
                    ncons += 1
                    return True
                m ^= e[0]
                r ^= e[1]
            return r == 0

        for i in range(H):
            Si = grid[i]
            cur_m = row_masks[i]
            cur_c = [0] * (W + 1)
            cur_c[0] = p if i == H - 1 else 0
            for j in range(W):
                a_c = prev_c[j]
                b_c = prev_c[j + 1]
                c_c = cur_c[j]
                if Si[j] == 'A':
                    cur_c[j + 1] = a_c ^ b_c ^ c_c ^ 1
                else:
                    cur_c[j + 1] = a_c ^ 1
                    if not add(bcheck_mask_for(i, j), b_c ^ c_c ^ 1):
                        return 0
            if not add(hwrap_mask[i], cur_c[W] ^ cur_c[0] ^ q):
                return 0
            prev_c = cur_c

        # vertical wraps: x(H,j) = x(0,j) ^ p
        for j in range(W + 1):
            if not add(row_masks[H - 1][j] ^ top_mask[j],
                       prev_c[j] ^ (top_mask[j] and 0) ^ p):
                return 0
        return 1 << (n0 - ncons)

    # B-check masks were collected in row-major order; index them
    bcheck_iter = iter(bcheck_mask)

    def bcheck_mask_for(i, j):
        return next(bcheck_iter)

    total = 0
    for p in (0, 1):
        for q in (0, 1):
            bcheck_iter = iter(bcheck_mask)
            total += count_sector(p, q)
    return (total // 2) % MOD


# =====================================================================
#  Reference: dense Gaussian elimination over all (H+1)(W+1) corner
#  variables (validation only).
# =====================================================================

def ref_count(H, W, grid):
    def vid(i, j):
        return i * (W + 1) + j

    nvars = (H + 1) * (W + 1)
    base_eqs = []
    for i in range(H):
        Si = grid[i]
        for j in range(W):
            a = vid(i, j)
            b = vid(i, j + 1)
            c = vid(i + 1, j)
            d = vid(i + 1, j + 1)
            if Si[j] == 'A':
                base_eqs.append(((1 << a) | (1 << b) | (1 << c) | (1 << d), 1))
            else:
                base_eqs.append(((1 << a) | (1 << d), 1))
                base_eqs.append(((1 << b) | (1 << c), 1))

    def count_solutions(eqs):
        basis = {}
        for mask, rhs in eqs:
            m, r = mask, rhs
            while m:
                piv = m.bit_length() - 1
                if piv in basis:
                    bm, br = basis[piv]
                    m ^= bm
                    r ^= br
                else:
                    basis[piv] = (m, r)
                    break
            else:
                if r:
                    return 0
        return 1 << (nvars - len(basis))

    total = 0
    for p in (0, 1):
        for q in (0, 1):
            eqs = list(base_eqs)
            for i in range(H + 1):
                eqs.append(((1 << vid(i, W)) | (1 << vid(i, 0)), q))
            for j in range(W + 1):
                eqs.append(((1 << vid(H, j)) | (1 << vid(0, j)), p))
            total += count_solutions(eqs)
    return total // 2


# =====================================================================
#  Brute force over all 4^a * 2^b placements (tiny grids only)
# =====================================================================

def brute_count(H, W, grid):
    opts = []
    for i in range(H):
        row = []
        for j in range(W):
            if grid[i][j] == 'A':
                row.append([(0, 1), (1, 2), (2, 3), (3, 0)])
            else:
                row.append([(0, 2), (1, 3)])
        opts.append(row)

    cells = [(i, j) for i in range(H) for j in range(W)]
    count = 0
    for choice in product(*[range(len(opts[i][j])) for i, j in cells]):
        sel = {}
        for (i, j), cidx in zip(cells, choice):
            sel[(i, j)] = set(opts[i][j][cidx])
        ok = True
        for i in range(H):
            if not ok:
                break
            for j in range(W):
                if (1 in sel[(i, j)]) != (3 in sel[(i, (j + 1) % W)]):
                    ok = False
                    break
                if (2 in sel[(i, j)]) != (0 in sel[((i + 1) % H, j)]):
                    ok = False
                    break
        if ok:
            count += 1
    return count


# =====================================================================

def solve():
    data = sys.stdin.buffer.read().split()
    idx = 0
    T = int(data[idx]); idx += 1
    out = []
    for _ in range(T):
        H = int(data[idx]); W = int(data[idx + 1]); idx += 2
        grid = [data[idx + i].decode() for i in range(H)]
        idx += H
        out.append(str(solve_case(H, W, grid)))
    sys.stdout.write("\n".join(out) + "\n")


def self_test():
    import random
    import time

    samples = [
        (3, 3, ["AAB", "AAB", "BBB"], 2),
        (3, 3, ["BBA", "ABA", "AAB"], 0),
        (3, 4, ["BAAB", "BABA", "BBAA"], 2),
    ]
    for H, W, g, exp in samples:
        got = solve_case(H, W, g)
        print(f"sample {H}x{W}: fast={got} expect={exp}",
              "OK" if got == exp else "FAIL")

    for H, W in [(2, 2), (2, 3), (3, 2)]:
        for bits in product("AB", repeat=H * W):
            pat = "".join(bits)
            g = [pat[i * W:(i + 1) * W] for i in range(H)]
            f = solve_case(H, W, g)
            r = ref_count(H, W, g)
            b = brute_count(H, W, g)
            if not (f == r == b):
                print(f"FAIL {H}x{W} {pat}: fast={f} ref={r} brute={b}")
                return
        print(f"{H}x{W}: exhaustive fast==ref==brute  OK")

    random.seed(1)
    for _ in range(60):
        H = random.randint(2, 4)
        W = random.randint(2, 4)
        g = ["".join(random.choice("AB") for _ in range(W))
             for _ in range(H)]
        f = solve_case(H, W, g)
        r = ref_count(H, W, g)
        b = brute_count(H, W, g)
        if not (f == r == b):
            print(f"FAIL rand {H}x{W} {g}: fast={f} ref={r} brute={b}")
            return
    print("random small: fast==ref==brute  OK")

    for _ in range(30):
        H = random.randint(2, 6)
        W = random.randint(2, 6)
        g = ["".join(random.choice("AB") for _ in range(W))
             for _ in range(H)]
        f = solve_case(H, W, g)
        r = ref_count(H, W, g)
        if f != r:
            print(f"FAIL med {H}x{W} {g}: fast={f} ref={r}")
            return
    print("random medium: fast==ref  OK")

    for H, W in [(2, 2), (2, 3), (3, 2), (3, 3), (4, 4), (3, 5)]:
        g = ["B" * W for _ in range(H)]
        print(f"all-B {H}x{W}: {solve_case(H, W, g)}")

    for (H, W) in [(1000, 1000), (2, 500000), (500000, 2), (100, 10000)]:
        random.seed(2)
        g = ["".join(random.choice("AB") for _ in range(W))
             for _ in range(H)]
        t0 = time.time()
        ans = solve_case(H, W, g)
        t1 = time.time()
        print(f"large {H}x{W}: ans={ans}  time={t1 - t0:.2f}s")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        self_test()
    else:
        solve()