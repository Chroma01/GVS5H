import sys


def solve_case(n, A, B):
    # Positions (1-indexed) of pieces in A and required squares in B.
    pa = [i + 1 for i in range(n) if A[i] == 49]
    pb = [i + 1 for i in range(n) if B[i] == 49]
    m = len(pa)
    k = len(pb)

    # Fewer pieces than required occupied squares: impossible to split.
    if m < k:
        return -1

    # Single required square: no interior boundary to enforce.
    if k == 1:
        r = pb[0]
        return max(0, r - pa[0], pa[-1] - r)

    # Lower bound on the number of moves.
    T_min = max(0, pb[0] - pa[0], pa[-1] - pb[-1])

    mm1 = m - 1
    feasible = set()

    # Two parity classes for the resolution time.
    for q in (0, 1):
        prev = 0
        ok = True
        for j in range(1, k):
            req = pb[j] - pb[j - 1]
            r = pb[j - 1]
            v = prev + 1
            while v <= mm1:
                av = pa[v] - pa[v - 1]
                if av >= req:
                    if av > req or ((pa[v - 1] - r) & 1) == q:
                        break
                v += 1
            if v > mm1:
                ok = False
                break
            prev = v
        if ok:
            feasible.add(q)

    if not feasible:
        return -1
    if (T_min & 1) in feasible:
        return T_min
    return T_min + 1


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        A = data[idx]; idx += 1
        B = data[idx]; idx += 1
        out.append(str(solve_case(n, A, B)))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == '__main__':
    main()