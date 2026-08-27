import sys

def solve():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        R = int(data[idx]); B = int(data[idx+1]); idx += 2
        # Feasibility: R must be even (parity flips around the cycle),
        # and if R == 0 then B must be even (diagonal-move graph is bipartite).
        if R % 2 == 1 or (R == 0 and B % 2 == 1):
            out.append("No")
            continue
        pieces = []
        if B == 0:
            # Red-only, R even >= 2.
            if R == 2:
                pieces = [('R', 1, 1), ('R', 1, 2)]
            else:
                m = R // 2
                for c in range(1, m + 1):
                    pieces.append(('R', 1, c))
                for c in range(m, 0, -1):
                    pieces.append(('R', 2, c))
        elif R == 0:
            # Blue-only, B even >= 2.
            if B == 2:
                pieces = [('B', 1, 1), ('B', 2, 2)]
            else:
                k = B // 2
                for i in range(2, k + 2):
                    pieces.append(('B', i, i))
                for j in range(k + 2, 2, -1):
                    pieces.append(('B', j, j - 2))
        else:
            # Mixed: R even >= 2, B >= 1.
            # Cycle: red path v_0=(2,2) ... v_{R-1}, then blue path b_1 ... b_B,
            # where v_{R-1} -> b_1 is orthogonal (red move) and b_B -> v_0 is diagonal (blue move).
            reds = []
            if B % 2 == 1:
                # v_{R-1} = (1,2), b_1 = (1,3). R = 2t+2, t >= 0.
                t = (R - 2) // 2
                reds.append((2, 2))
                if t >= 1:
                    for r in range(3, t + 2):
                        reds.append((r, 2))
                    for r in range(t + 1, 1, -1):
                        reds.append((r, 1))
                    reds.append((1, 1))
                reds.append((1, 2))
            else:
                if R == 2:
                    # v_1 = (2,3), b_1 = (2,4).
                    reds = [(2, 2), (2, 3)]
                else:
                    # v_{R-1} = (1,4), b_1 = (2,4). R = 2t+4, t >= 0.
                    t = (R - 4) // 2
                    reds.append((2, 2))
                    if t >= 1:
                        for r in range(3, t + 2):
                            reds.append((r, 2))
                        for r in range(t + 1, 1, -1):
                            reds.append((r, 1))
                        reds.append((1, 1))
                    reds.append((1, 2))
                    reds.append((1, 3))
                    reds.append((1, 4))
            blues = []
            if B % 2 == 1:
                # B = 2k+1, k >= 0. Path from (1,3) to (3,3) [or just (1,3) if B=1].
                k = (B - 1) // 2
                if k == 0:
                    blues.append((1, 3))
                else:
                    for i in range(1, k + 2):
                        blues.append((i, i + 2))
                    blues.append((k + 2, k + 2))
                    for i in range(k + 1, 2, -1):
                        blues.append((i, i))
            else:
                # B = 2k, k >= 1. Path from (2,4) to (3,3).
                k = B // 2
                for i in range(2, k + 2):
                    blues.append((i, i + 2))
                blues.append((k + 2, k + 2))
                for i in range(k + 1, 3, -1):
                    blues.append((i, i))
                blues.append((3, 3))
            for (r, c) in reds:
                pieces.append(('R', r, c))
            for (r, c) in blues:
                pieces.append(('B', r, c))
        out.append("Yes")
        for (p, r, c) in pieces:
            out.append(f"{p} {r} {c}")
    sys.stdout.write("\n".join(out) + "\n")

solve()