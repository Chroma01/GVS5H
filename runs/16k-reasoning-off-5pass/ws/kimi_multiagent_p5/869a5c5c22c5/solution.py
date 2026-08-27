import sys

def solve():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    pos = 1
    out = []
    for _ in range(t):
        R = int(data[pos]); B = int(data[pos+1]); pos += 2
        # Necessary conditions:
        #  * A red piece's outgoing move flips (r+c) parity, a blue's preserves it.
        #    Around the closed cycle the total parity change is 0  =>  R even.
        #  * If R == 0 every move is diagonal, which flips r-parity  =>  B even.
        if (R & 1) or (R == 0 and (B & 1)):
            out.append("No")
            continue
        out.append("Yes")
        pieces = []  # (color, r, c) in placement order; consecutive (cyclic) must be compatible
        if B == 0:
            # All red, R even: perimeter ring of a 2 x (R/2) rectangle, all moves orthogonal.
            k = R // 2
            for c in range(1, k + 1):
                pieces.append(('R', 1, c))
            for c in range(k, 0, -1):
                pieces.append(('R', 2, c))
        elif R == 0:
            # All blue, B even: ring in rotated coordinates u=r+c, v=r-c.
            # Diagonal step = change u or v by 2. Ring: u in {2,4}, v = 0,2,...,2(k-1), k=B/2.
            # Using u in {2,4} (not {0,2}) guarantees r=(u+v)/2 >= 1.
            k = B // 2
            pts = [(2, 2 * j) for j in range(k)] + [(4, 2 * j) for j in range(k - 1, -1, -1)]
            raw = [((u + v) // 2, (u - v) // 2) for (u, v) in pts]
            minc = min(c for (_, c) in raw)
            for (r, c) in raw:
                pieces.append(('B', r, c - minc + 1))
        else:
            # Mixed: R = 2p (p >= 1), B >= 1.
            # Red ring on rows 2 and 3, columns 1..p; the vertical edge (2,p)->(3,p)
            # is replaced by a chain of B blue pieces:
            #   (2,p)R -> b1 -> b2 -> ... -> bB -> (3,p)R
            # (2,p)->b1 orthogonal, blue steps diagonal, bB->(3,p) diagonal.
            p = R // 2
            for c in range(1, p + 1):
                pieces.append(('R', 2, c))
            blues = []
            if B == 1:
                blues = [(2, p + 1)]
            elif B == 2:
                blues = [(1, p), (2, p + 1)]
            else:
                if B % 2 == 0:
                    blues.append((1, p))   # extra blue; remaining B-1 = 2m+1 is odd
                    m = (B - 2) // 2       # >= 1 here since B >= 4
                else:
                    m = (B - 1) // 2       # >= 1 here since B >= 3
                # Odd chain of 2m+1 blues starting at (2,p+1):
                # m steps down-right, 1 step down-left, m-1 steps up-left,
                # ending at (4,p+1) which is diagonally adjacent to (3,p).
                r, c = 2, p + 1
                blues.append((r, c))
                for _ in range(m):          # down-right
                    r += 1; c += 1
                    blues.append((r, c))
                r += 1; c -= 1              # down-left
                blues.append((r, c))
                for _ in range(m - 1):      # up-left
                    r -= 1; c -= 1
                    blues.append((r, c))
            for (r, c) in blues:
                pieces.append(('B', r, c))
            for c in range(p, 0, -1):
                pieces.append(('R', 3, c))
        for (col, r, c) in pieces:
            out.append(f"{col} {r} {c}")
    sys.stdout.write("\n".join(out) + "\n")

solve()