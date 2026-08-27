import sys

def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    r0 = 1
    c0 = 500000
    for _ in range(t):
        R = int(data[idx]); B = int(data[idx + 1]); idx += 2
        if (R & 1) or (R == 0 and (B & 1)):
            out.append("No")
            continue
        out.append("Yes")
        if B == 0:
            # all red: rectangle 2 x a
            a = R // 2
            for x in range(1, a + 1):
                out.append("R 1 %d" % x)
            for x in range(a, 0, -1):
                out.append("R 2 %d" % x)
        elif R == 0:
            # all blue: rectangle in rotated lattice
            q = B // 2
            for x in range(q):
                out.append("B %d %d" % (r0 + x, c0 + x))
            for x in range(q - 1, -1, -1):
                out.append("B %d %d" % (r0 + x + 1, c0 + x - 1))
        else:
            if B & 1:
                k = (B - 1) // 2
                blue = [(r0 + x, c0 + x) for x in range(k + 1)]
                blue += [(r0 + 1 + x, c0 - 1 + x) for x in range(k, -1, -1)]
                # blue has B+1 vertices, last one is T = (r0+1, c0-1)
                L = (R - 2) // 2
                red = [(r0 + 1, c0 - 1 - j) for j in range(1, L + 1)]
                red += [(r0, c0 - 1 - L + j) for j in range(L + 1)]
                # total red pieces = T + red = 1 + (2L+1) = R
                cells = blue + red
                # first B pieces blue, rest red
                for i in range(B):
                    r, c = cells[i]
                    out.append("B %d %d" % (r, c))
                for i in range(B, len(cells)):
                    r, c = cells[i]
                    out.append("R %d %d" % (r, c))
            else:
                k = B // 2
                blue = [(r0 + x, c0 + x) for x in range(k + 1)]
                blue += [(r0 + 1 + x, c0 - 1 + x) for x in range(k, 0, -1)]
                # blue has B+1 vertices, last one is T = (r0+2, c0)
                if R == 2:
                    red = [(r0 + 1, c0)]
                else:
                    L = (R - 4) // 2
                    red = [(r0 + 2, c0 - 1 - j) for j in range(L + 1)]
                    red.append((r0 + 1, c0 - 1 - L))
                    red += [(r0, c0 - 1 - L + j) for j in range(L + 1)]
                cells = blue + red
                for i in range(B):
                    r, c = cells[i]
                    out.append("B %d %d" % (r, c))
                for i in range(B, len(cells)):
                    r, c = cells[i]
                    out.append("R %d %d" % (r, c))
    sys.stdout.write("\n".join(out) + "\n")

main()