import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    out = []
    SHIFT = 10**6
    pos = 1

    for _ in range(t):
        R = int(data[pos])
        B = int(data[pos + 1])
        pos += 2

        if R + B < 2 or (R & 1) or (R == 0 and (B & 1)):
            out.append("No")
            continue

        out.append("Yes")

        if R == 2 and B == 3:
            out.extend([
                "B 2 3",
                "R 3 2" + " ",
                "B 2 2",
                "B 3 3",
                "R 2 4",
            ])
            continue

        if R == 4 and B == 0:
            out.extend([
                "R 1 1",
                "R 1 2",
                "R 2 2",
                "R 2 1",
            ])
            continue

        if R == 0:
            m = B // 2
            for x in range(m):
                out.append(f"B {x + SHIFT} {x + SHIFT}")
            for x in range(m - 1, -1, -1):
                out.append(f"B {x + 1 + SHIFT} {x - 1 + SHIFT}")
        else:
            K = (R - 2) // 2

            for c in range(0, -K - 1, -1):
                out.append(f"R {SHIFT} {c + SHIFT}")
            for c in range(-K, 1):
                out.append(f"R {SHIFT + 1} {c + SHIFT}")

            if B > 0:
                if B == 1:
                    out.append(f"B {SHIFT + 1} {SHIFT + 1}")
                elif B & 1:
                    m = B // 2
                    for x in range(1, m + 1):
                        out.append(f"B {x + SHIFT} {x + SHIFT}")
                    for x in range(m, -1, -1):
                        out.append(f"B {x - 1 + SHIFT} {x + 1 + SHIFT}")
                else:
                    m = B // 2
                    for x in range(1, m + 1):
                        out.append(f"B {x + 1 + SHIFT} {x - 1 + SHIFT}")
                    for x in range(m, 0, -1):
                        out.append(f"B {x + SHIFT} {x + SHIFT}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()