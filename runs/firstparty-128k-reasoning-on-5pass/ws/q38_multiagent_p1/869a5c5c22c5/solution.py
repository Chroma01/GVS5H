import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    tc = int(data[0])
    idx = 1
    out = []
    OFF = 10**6

    for _ in range(tc):
        R = int(data[idx])
        B = int(data[idx + 1])
        idx += 2

        if (R & 1) or (R == 0 and (B & 1)):
            out.append("No")
            continue

        if R == 2 and B == 3:
            out.append("Yes")
            out.append("B 2 3")
            out.append("R 3 2" + " ")
            out.append("B 2 2")
            out.append("B 3 3")
            out.append("R 2 4")
            continue

        out.append("Yes")

        if R == 0:
            k = B // 2

            for a in range(k):
                out.append(f"B {a + OFF} {a + OFF}")

            for a in range(k - 1, -1, -1):
                out.append(f"B {a + 1 + OFF} {a - 1 + OFF}")

        elif B == 0:
            k = R // 2

            for c in range(1, k + 1):
                out.append(f"R 1 {c}")

            for c in range(k, 0, -1):
                out.append(f"R 2 {c}")

        else:
            kr = R // 2

            if B % 2 == 0:
                for c in range(kr):
                    out.append(f"R {OFF} {c + OFF}")

                for c in range(kr - 1, -1, -1):
                    out.append(f"R {OFF + 1} {c + OFF}")

                m = B // 2

                for x in range(m):
                    out.append(f"B {2 + x + OFF} {-x + OFF}")

                for y in range(m, 0, -1):
                    out.append(f"B {y + OFF} {-y + OFF}")

            else:
                for c in range(0, -kr, -1):
                    out.append(f"R {OFF} {c + OFF}")

                for c in range(-kr + 1, 1):
                    out.append(f"R {OFF + 1} {c + OFF}")

                n = (B - 1) // 2

                for x in range(n + 1):
                    out.append(f"B {1 - x + OFF} {1 + x + OFF}")

                for x in range(n, 0, -1):
                    out.append(f"B {-x + OFF} {x + OFF}")

    sys.stdout.write("\n".join(out))
    if out:
        sys.stdout.write("\n")

if __name__ == "__main__":
    solve()