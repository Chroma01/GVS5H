import sys

def construct(R, B):
    # Possible iff R is even and (R >= 2 or B is even).
    if R % 2 == 1:
        return None
    if R == 0:
        if B % 2 == 1:
            return None
        if B == 2:
            return [('B', 1, 1), ('B', 2, 2)]
        # even B >= 4: perimeter of 2 x k rectangle in rotated coords
        # (u,v) -> (r,c) = (u+v, u-v+off); diagonal adjacency = grid adjacency.
        k = B // 2
        path = [(1, v) for v in range(1, k + 1)] + [(2, v) for v in range(k, 0, -1)]
        off = k + 2
        return [('B', u + v, u - v + off) for (u, v) in path]

    # R even >= 2.
    # Red cycle: perimeter of 2 x m rectangle, rows 2..3, cols 2..m+1.
    m = R // 2
    cyc = [(2, c) for c in range(2, m + 2)] + [(3, c) for c in range(m + 1, 1, -1)]

    # Blue chain inserted at the right edge: ... (3,m+1)=p -> [chain] -> r=(2,m+1) ...
    # Requirements: p orth-adj chain[0]; chain[i] diag-adj chain[i+1];
    # chain[-1] diag-adj r; all chain squares distinct and disjoint from reds.
    if B == 0:
        chain = []
    elif B == 1:
        chain = [(3, m + 2)]            # orth-adj p, diag-adj r
    elif B % 2 == 0:
        # even B >= 2, B = 4j+2 (j>=0): down-right leg in rows 4..5,
        # then return leg in rows 2..3 (cols >= m+2 are all free).
        j = (B - 2) // 4
        chain = []
        for i in range(2 * j + 1):      # (4,m+1),(5,m+2),(4,m+3),...,(5,m+2j+2)
            chain.append((4 + (i & 1), m + 1 + i))
        for i in range(2 * j + 1):      # (2,m+2j+3),(3,m+2j+2),...,(3,m+2)
            chain.append((2 + (i & 1), m + 2 * j + 3 - i))
    else:
        # odd B >= 3, B = 4j+3 (j>=0): out leg in rows 3..4,
        # then return leg in rows 1..2, ending at (1,m+2) (diag-adj r).
        j = (B - 3) // 4
        chain = []
        for i in range(2 * j + 1):      # (3,m+2),(4,m+3),...,(3,m+2j+2)
            chain.append((3 + (i & 1), m + 2 + i))
        for i in range(2 * j + 2):      # (2,m+2j+3),(1,m+2j+4),...,(1,m+2)
            chain.append((2 - (i & 1), m + 2 * j + 3 + (1 if i == 0 else (i - 1))))
        # fix: build return leg explicitly to avoid index mistakes
        chain = chain[:2 * j + 1]
        # (2,m+2j+3), then zigzag left in rows 1..2 ending at (1,m+2)
        chain.append((2, m + 2 * j + 3))
        for i in range(2 * j + 1):      # (1,m+2j+4),(2,m+2j+5),...? -> leftward
            pass
        # simpler explicit leftward zigzag:
        chain = chain[:2 * j + 1]
        chain.append((2, m + 2 * j + 3))
        for i in range(1, 2 * j + 2):   # (1,m+2j+4-i?) -> see below
            rrow = 1 if i % 2 == 1 else 2
            ccol = m + 2 * j + 3 + (1 if i % 2 == 1 else 0) - (i - 1) // 2 * 2 - (1 if i % 2 == 0 else 0)
            chain.append((rrow, ccol))
        # The above is error-prone; rebuild cleanly:
        chain = [(3 + (i & 1), m + 2 + i) for i in range(2 * j + 1)]
        # return leg: (2,m+2j+3),(1,m+2j+4)?? must go LEFT toward (1,m+2).
        # From (3,m+2j+2) step to (2,m+2j+3), then zigzag left:
        # (2,m+2j+3)->(1,m+2j+2)->(2,m+2j+1)->(1,m+2j)->...->(1,m+2)
        chain.append((2, m + 2 * j + 3))
        for t in range(2 * j + 1):
            # columns decrease: m+2j+2, m+2j+1, ..., m+2 ; rows alternate 1,2,1,...
            chain.append((1 + (t & 1), m + 2 * j + 2 - t))
        # last appended: t=2j -> (1, m+2)  ✓

    seq = [('R', a, b) for (a, b) in cyc] + [('B', a, b) for (a, b) in chain]
    return seq

def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    idx = 1
    for _ in range(t):
        R = int(data[idx]); B = int(data[idx + 1]); idx += 2
        res = construct(R, B)
        if res is None:
            out.append("No")
        else:
            out.append("Yes")
            for (typ, r, c) in res:
                out.append(f"{typ} {r} {c}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()