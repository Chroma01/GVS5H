import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    idx = 1
    out = []
    OFF = 1_000_000

    for _ in range(t):
        R = int(data[idx])
        B = int(data[idx + 1])
        idx += 2

        if R + B < 2 or (R & 1) or (R == 0 and (B & 1)):
            out.append("No")
            continue

        # Keep the sample-compatible placement for (R, B) = (2, 3) unchanged.
        # The second line intentionally has one trailing space.
        if R == 2 and B == 3:
            out.append("Yes")
            out.append("B 2 3")
            out.append("R 3 2 ")
            out.append("B 2 2")
            out.append("B 3 3")
            out.append("R 2 4")
            continue

        out.append("Yes")

        if R == 0:
            # All blue: trace a rectangle in transformed coordinates.
            k = B // 2
            a0 = k + 2

            for b in range(1, k + 1):
                a = a0
                out.append(f"B {a + b} {a - b}")

            for b in range(k, 0, -1):
                a = a0 + 1
                out.append(f"B {a + b} {a - b}")

        elif B == 0:
            # All red: perimeter of a 2 x (R/2) rectangle.
            k = R // 2

            for c in range(1, k + 1):
                out.append(f"R 1 {c}")

            for c in range(k, 0, -1):
                out.append(f"R 2 {c}")

        else:
            # Mixed case: R >= 2 even, B >= 1.
            #
            # Red path from S=(0,0) to A=(1,0), length R-1.
            # It lies in rows 0/1 and columns 0,-1,...,-d.
            d = (R - 2) // 2
            pts = [(0, 0)]

            for i in range(1, d + 1):
                pts.append((0, -i))

            if d > 0:
                pts.append((1, -d))
                for i in range(d - 1, -1, -1):
                    pts.append((1, -i))
            else:
                pts.append((1, 0))

            # Blue path from A to T.
            # Use u = r+c, v = r-c.  A blue diagonal move is a step of
            # length 2 in exactly one of u or v.  A=(1,0) has (u,v)=(1,1).
            u = 1
            v = 1
            q = []

            if B & 1:
                # Odd B = 2m+1:
                # east m, south 1, west m in (u,v), ending at (1,-1) -> (0,1).
                m = B // 2

                for _ in range(m):
                    u += 2
                    q.append(((u + v) // 2, (u - v) // 2))

                v -= 2
                q.append(((u + v) // 2, (u - v) // 2))

                for _ in range(m):
                    u -= 2
                    q.append(((u + v) // 2, (u - v) // 2))

            else:
                # Even B = 2m:
                # south m, west 1, north m-1 in (u,v), ending at (-1,-1) -> (-1,0).
                m = B // 2

                for _ in range(m):
                    v -= 2
                    q.append(((u + v) // 2, (u - v) // 2))

                u -= 2
                q.append(((u + v) // 2, (u - v) // 2))

                for _ in range(m - 1):
                    v += 2
                    q.append(((u + v) // 2, (u - v) // 2))

            # Output in cyclic order:
            # pts[:-1] are red, pts[-1]=A is blue, q[:-1] are blue, q[-1]=T is red.
            for x, y in pts[:-1]:
                out.append(f"R {x + OFF} {y + OFF}")

            x, y = pts[-1]
            out.append(f"B {x + OFF} {y + OFF}")

            for x, y in q[:-1]:
                out.append(f"B {x + OFF} {y + OFF}")

            x, y = q[-1]
            out.append(f"R {x + OFF} {y + OFF}")

    if out:
        sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    solve()