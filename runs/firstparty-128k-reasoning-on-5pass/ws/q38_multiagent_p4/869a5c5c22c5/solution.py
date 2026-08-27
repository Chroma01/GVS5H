import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    idx = 1
    out = []
    append = out.append
    OFF = 10**6

    for _ in range(t):
        R = int(data[idx])
        B = int(data[idx + 1])
        idx += 2

        if R + B < 2 or (R & 1) or (R == 0 and (B & 1)):
            append("No")
            continue

        append("Yes")

        if R == 2 and B == 3:
            append("B 2 3")
            append("R 3 2" + " ")
            append("B 2 2")
            append("B 3 3")
            append("R 2 4")
            continue

        if B == 0:
            if R == 2:
                append("R 1 1")
                append("R 1 2")
            else:
                w = R // 2
                for c in range(1, w + 1):
                    append(f"R 1 {c}")
                for c in range(w, 0, -1):
                    append(f"R 2 {c}")
            continue

        if R == 0:
            b = B // 2 - 1
            for p in range(b + 1):
                append(f"B {p + OFF} {p + OFF}")
            for p in range(b, -1, -1):
                append(f"B {p + 1 + OFF} {p - 1 + OFF}")
            continue

        k = R // 2

        if B & 1:
            m = B // 2

            red = [(0, 0)]
            red.extend((i, 0) for i in range(1, k + 1))
            red.append((k, 1))
            red.extend((i, 1) for i in range(k - 1, 0, -1))

            blue = [(1, 1)]
            blue.extend((1 - i, 1 + i) for i in range(1, m + 1))
            if m:
                blue.append((-m, m))
            blue.extend((-j, j) for j in range(m - 1, 0, -1))
            blue.append((0, 0))

            for i in range(len(red) - 1):
                x, y = red[i]
                append(f"R {x + OFF} {y + OFF}")
            for i in range(len(blue) - 1):
                x, y = blue[i]
                append(f"B {x + OFF} {y + OFF}")

        else:
            m = B // 2

            red = [(0, 0)]
            red.extend((i, 0) for i in range(1, k))
            red.append((k - 1, 1))
            red.extend((i, 1) for i in range(k - 2, -1, -1))
            red.append((0, 2))

            blue = [(0, 2)]
            blue.extend((-i, 2 + i) for i in range(1, m))
            blue.append((-m, m))
            blue.extend((-j, j) for j in range(m - 1, 0, -1))
            blue.append((0, 0))

            for i in range(len(red) - 1):
                x, y = red[i]
                append(f"R {x + OFF} {y + OFF}")
            for i in range(len(blue) - 1):
                x, y = blue[i]
                append(f"B {x + OFF} {y + OFF}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()