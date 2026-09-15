import sys
import random


# ---------------- main solution (residue criterion) ----------------
def solve_problem(N, X, Y, S, T):
    # No window of length X+Y fits -> no operation is ever possible.
    if X + Y > N:
        return S == T
    # Invariant 1: ordered list of '1' positions modulo X
    a = [(i + 1) % X for i in range(N) if S[i] == '1']
    b = [(i + 1) % X for i in range(N) if T[i] == '1']
    if a != b:
        return False
    # Invariant 2: ordered list of '0' positions modulo Y
    a2 = [(i + 1) % Y for i in range(N) if S[i] == '0']
    b2 = [(i + 1) % Y for i in range(N) if T[i] == '0']
    return a2 == b2


# ---------------- validation of the residue criterion ----------------
def build_positions(N):
    size = 1 << N
    ones = [None] * size
    zeros = [None] * size
    for mask in range(size):
        o = []
        z = []
        m = mask
        p = 1
        while p <= N:
            if m & 1:
                o.append(p)
            else:
                z.append(p)
            m >>= 1
            p += 1
        ones[mask] = tuple(o)
        zeros[mask] = tuple(z)
    return ones, zeros


def check(N, X, Y, ones, zeros):
    """Return None if signature classes == connected components, else a witness."""
    L = X + Y
    size = 1 << N
    par = list(range(size))
    rnk = bytearray(size)
    # window pattern 0^X 1^Y  and its reverse 1^Y 0^X
    patA = ((1 << Y) - 1) << X     # chars (bit low->high) 0..0 1..1
    resA = (1 << Y) - 1            # chars 1..1 0..0
    Lmask = (1 << L) - 1

    for mask in range(size):
        for i in range(N - L + 1):
            w = (mask >> i) & Lmask
            if w == patA:
                nm = mask - (w << i) + (resA << i)
            elif w == resA:
                nm = mask - (w << i) + (patA << i)
            else:
                continue
            a = mask
            while par[a] != a:
                par[a] = par[par[a]]
                a = par[a]
            b = nm
            while par[b] != b:
                par[b] = par[par[b]]
                b = par[b]
            if a != b:
                if rnk[a] < rnk[b]:
                    a, b = b, a
                par[b] = a
                if rnk[a] == rnk[b]:
                    rnk[a] += 1

    root_sig = {}
    sig_root = {}
    for mask in range(size):
        a = mask
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        r = a
        s = (tuple(p % X for p in ones[mask]), tuple(p % Y for p in zeros[mask]))
        if r in root_sig:
            s0, m0 = root_sig[r]
            if s0 != s:
                return ("same_comp_diff_sig", m0, mask)
        else:
            root_sig[r] = (s, mask)
        if s in sig_root:
            r0, m0 = sig_root[s]
            if r0 != r:
                return ("same_sig_diff_comp", m0, mask)
        else:
            sig_root[s] = (r, mask)
    return None


def mstr(mask, N):
    return ''.join('1' if (mask >> p) & 1 else '0' for p in range(N))


def run_validation():
    found = False
    # exhaustive N = 1..12, all (X,Y) with X+Y <= N
    for N in range(1, 13):
        ones, zeros = build_positions(N)
        for X in range(1, N + 1):
            for Y in range(1, N + 1):
                if X + Y > N:
                    continue
                res = check(N, X, Y, ones, zeros)
                if res:
                    kind, m1, m2 = res
                    sys.stdout.write("MISMATCH %s N=%d X=%d Y=%d\n" % (kind, N, X, Y))
                    sys.stdout.write("S=%s\n" % mstr(m1, N))
                    sys.stdout.write("T=%s\n" % mstr(m2, N))
                    found = True

    # spot checks N = 13..15 (balanced pairs always, plus random others)
    random.seed(1234567)
    for N in (13, 14, 15):
        ones, zeros = build_positions(N)
        pairs = [(X, Y) for X in range(1, N + 1) for Y in range(1, N + 1) if X + Y <= N]
        chosen = [pr for pr in pairs if pr[0] == pr[1]]
        rest = [pr for pr in pairs if pr[0] != pr[1]]
        random.shuffle(rest)
        need = 12 - len(chosen)
        if need > 0:
            chosen += rest[:need]
        for (X, Y) in chosen:
            res = check(N, X, Y, ones, zeros)
            if res:
                kind, m1, m2 = res
                sys.stdout.write("SPOT MISMATCH %s N=%d X=%d Y=%d\n" % (kind, N, X, Y))
                sys.stdout.write("S=%s\n" % mstr(m1, N))
                sys.stdout.write("T=%s\n" % mstr(m2, N))
                found = True

    if not found:
        sys.stdout.write("VALIDATED N<=12 all (X,Y)\n")


def main():
    data = sys.stdin.buffer.read().split()
    if len(data) >= 5:
        N = int(data[0]); X = int(data[1]); Y = int(data[2])
        S = data[3].decode(); T = data[4].decode()
        sys.stdout.write("Yes\n" if solve_problem(N, X, Y, S, T) else "No\n")
    else:
        run_validation()


main()