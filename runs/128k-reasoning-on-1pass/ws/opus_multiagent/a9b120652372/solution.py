import sys

# ----------------------------------------------------------------------
#  Solution
#
#  Model: state = set of distinct occupied squares p_1<...<p_k.
#  An operation at i changes every gap by 0/-1/-2:
#     i < L            : pure left translation   (span unchanged, L-1)
#     i > R            : pure right translation  (span unchanged, L+1)
#     i = L            : first gap -1            (span-1, L unchanged)
#     i = R            : last  gap -1            (span-1, L+1)
#     L < i < R        : span-2                  (L+1)
#  With a=#left-translations, b=#right-translations, u=#(i=L), v=#(i=R),
#  w=#(L<i<R):
#        D  = span(A)-span(B) = u+v+2w   ,  Delta = L_B-L_A = -a+b+v+w
#  minimising a+b gives   answer = max(Delta+u , (D-Delta)+v).
#
#  Feasibility: choose a monotone grouping of A's ones onto B's ones.
#  A boundary gap with reduction 0 is a "wall": no operation may ever be
#  inside it nor at its endpoints, hence the whole prefix left of it only
#  sees u-ops (span-1) and interior ops (span-2)  =>  prefix reduction
#  == u  (mod 2).  Greedy "earliest allowed boundary" two-pointer decides
#  this in O(p).  Only u in {0,1} has to be tried (cost is monotone in u,
#  feasibility depends on u only mod 2, v is forced to (D-u) mod 2).
# ----------------------------------------------------------------------


def feasible(al, be, p, q, u):
    """Exists a monotone grouping with all wall-parities equal to u ?"""
    if q == 1:
        return True
    par = (al[0] + be[0] + u) & 1
    j = 0
    lim = p - 1                      # gap index j is valid for j <= p-2
    prev = be[0]
    for i in range(1, q):
        bi = be[i] - prev
        while j < lim:
            aj = al[j + 1] - al[j]
            if aj > bi or (aj == bi and ((al[j] + prev) & 1) == par):
                break
            j += 1
        else:
            return False
        j += 1
        prev = be[i]
    return True


def solve(al, be):
    p = len(al)
    q = len(be)
    if q > p:
        return -1
    d = (al[-1] - al[0]) - (be[-1] - be[0])          # D
    if d < 0:
        return -1
    delta = be[0] - al[0]                            # Delta
    # u = 0 , v = D mod 2
    x = delta
    y = d - delta + (d & 1)
    c0 = x if x > y else y
    if d >= 1:
        # u = 1 , v = (D-1) mod 2   (u+v <= D holds whenever D>=1)
        x = delta + 1
        y = d - delta + ((d - 1) & 1)
        c1 = x if x > y else y
        if c1 < c0:
            if feasible(al, be, p, q, 1):
                return c1
            if feasible(al, be, p, q, 0):
                return c0
            return -1
        else:
            if feasible(al, be, p, q, 0):
                return c0
            if feasible(al, be, p, q, 1):
                return c1
            return -1
    else:
        return c0 if feasible(al, be, p, q, 0) else -1


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    k = 1
    try:
        import numpy as _np
        frombuffer = _np.frombuffer
        flatnonzero = _np.flatnonzero
        u8 = _np.uint8
        has_np = True
    except Exception:
        has_np = False
    for _ in range(t):
        A = data[k + 1]
        B = data[k + 2]
        k += 3
        if has_np and len(A) >= 256:
            al = flatnonzero(frombuffer(A, u8) == 49).tolist()
            be = flatnonzero(frombuffer(B, u8) == 49).tolist()
        else:
            al = [i for i, c in enumerate(A) if c == 49]
            be = [i for i, c in enumerate(B) if c == 49]
        out.append(solve(al, be))
    sys.stdout.write('\n'.join(map(str, out)) + '\n')


# ----------------------------------------------------------------------
#  Validation harness (never executed by the judge; run with --validate N)
# ----------------------------------------------------------------------


def brute_dists(Astr):
    """BFS from configuration A; returns dict {sorted tuple -> dist}."""
    from collections import deque
    n = len(Astr)
    start = tuple(i for i, c in enumerate(Astr) if c == '1')
    dist = {start: 0}
    dq = deque([start])
    while dq:
        s = dq.popleft()
        nd = dist[s] + 1
        for i in range(n):
            t = []
            for x in s:
                if x < i:
                    t.append(x + 1)
                elif x > i:
                    t.append(x - 1)
                else:
                    t.append(x)
            t = tuple(sorted(set(t)))
            if t not in dist:
                dist[t] = nd
                dq.append(t)
    return dist


def validate(maxn=6):
    bad = 0
    total = 0
    for n in range(1, maxn + 1):
        for am in range(1, 1 << n):
            Astr = ''.join('1' if (am >> i) & 1 else '0' for i in range(n))
            dist = brute_dists(Astr)
            al = [i for i, c in enumerate(Astr) if c == '1']
            for bm in range(1, 1 << n):
                Bstr = ''.join('1' if (bm >> i) & 1 else '0' for i in range(n))
                be = [i for i, c in enumerate(Bstr) if c == '1']
                exp = dist.get(tuple(be), -1)
                got = solve(al, be)
                total += 1
                if exp != got:
                    bad += 1
                    if bad <= 50:
                        print("MISMATCH n=%d A=%s B=%s brute=%d proto=%d"
                              % (n, Astr, Bstr, exp, got))
        print("  n=%d done, running mismatches=%d" % (n, bad))
    print("checked %d pairs, %d mismatches" % (total, bad))
    for A, B in (("10100101", "10101010"), ("1101", "0110"), ("11", "10"),
                 ("101", "110"), ("10101", "01010"), ("10011", "10110")):
        al = [i for i, c in enumerate(A) if c == '1']
        be = [i for i, c in enumerate(B) if c == '1']
        print("spot A=%s B=%s -> proto %s" % (A, B, solve(al, be)))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--validate':
        validate(int(sys.argv[2]) if len(sys.argv) > 2 else 6)
    else:
        main()