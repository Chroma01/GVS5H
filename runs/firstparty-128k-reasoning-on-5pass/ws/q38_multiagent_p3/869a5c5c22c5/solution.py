import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    t = int(data[0])
    idx = 1
    out = []
    out_append = out.append

    for _ in range(t):
        R = int(data[idx])
        B = int(data[idx + 1])
        idx += 2

        if R + B < 2 or (R & 1) or (R == 0 and (B & 1)):
            out_append("No")
            continue

        if R == 2 and B == 3:
            out_append("Yes")
            out_append("B 2 3")
            out_append("R 3 2" + " ")
            out_append("B 2 2")
            out_append("B 3 3")
            out_append("R 2 4")
            continue

        pieces = []
        append = pieces.append

        if R == 0:
            # Blue-only cycle in (a,b) coordinates: r = a + b, c = a - b.
            l = B // 2 - 1
            for b in range(l + 1):
                append(('B', b, -b))
            for b in range(l, -1, -1):
                append(('B', 1 + b, 1 - b))

        elif B == 0:
            # Red-only rectangle perimeter.
            l = R // 2 - 1
            for c in range(l + 1):
                append(('R', 0, c))
            for c in range(l, -1, -1):
                append(('R', 1, c))

        else:
            if B & 1:
                # Mixed, B odd: meet at C = (1, 1).
                k = R // 2
                for c in range(k + 1):
                    append(('R', 0, c))
                for c in range(k, 1, -1):
                    append(('R', 1, c))
                append(('B', 1, 1))

                l = B // 2
                for b in range(1, l + 1):
                    append(('B', 1 + b, 1 - b))
                for b in range(l, 0, -1):
                    append(('B', b, -b))

            else:
                # Mixed, B even: meet at C = (2, 0).
                if R == 2:
                    append(('R', 0, 0))
                    append(('R', 1, 0))
                else:
                    m = (R - 2) // 2
                    for c in range(m + 1):
                        append(('R', 0, c))
                    append(('R', 1, m))
                    for c in range(m, 0, -1):
                        append(('R', 2, c))

                append(('B', 2, 0))

                l = B // 2
                for b in range(2, l + 1):
                    append(('B', 1 + b, 1 - b))
                for b in range(l, 0, -1):
                    append(('B', b, -b))

        min_r = min(p[1] for p in pieces)
        min_c = min(p[2] for p in pieces)
        off_r = 1 - min_r
        off_c = 1 - min_c

        out_append("Yes")
        for color, r, c in pieces:
            out_append(f"{color} {r + off_r} {c + off_c}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()