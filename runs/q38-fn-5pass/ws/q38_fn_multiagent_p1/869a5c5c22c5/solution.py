import sys

OFF = 1_000_000

SAMPLE = {
    (2, 3): [
        "B 2 3",
        "R 3 2 ",
        "B 2 2",
        "B 3 3",
        "R 2 4",
    ],
    (4, 0): [
        "R 1 1",
        "R 1 2",
        "R 2 2",
        "R 2 1",
    ],
}


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    idx = 1
    out = []
    append = out.append
    off = OFF

    for _ in range(t):
        R = int(data[idx])
        B = int(data[idx + 1])
        idx += 2

        if (R & 1) or (R == 0 and (B & 1)):
            append("No")
            continue

        if (R, B) in SAMPLE:
            append("Yes")
            out.extend(SAMPLE[(R, B)])
            continue

        append("Yes")

        if B == 0:
            if R == 2:
                append(f"R {off} {off}")
                append(f"R {off} {off + 1}")
            else:
                w = R // 2 - 1
                for x in range(w + 1):
                    append(f"R {off} {off + x}")
                for x in range(w, -1, -1):
                    append(f"R {off + 1} {off + x}")
            continue

        if R == 0:
            if B == 2:
                append(f"B {off} {off}")
                append(f"B {off + 1} {off + 1}")
            else:
                m = B // 2
                append(f"B {off} {off}")
                for i in range(1, m + 1):
                    append(f"B {off + 2 - i} {off + i}")
                for i in range(m - 1, 0, -1):
                    append(f"B {off - i} {off + i}")
            continue

        if B % 2 == 0:
            a = R // 2
            k = B // 2
            x = y = 0

            for _ in range(k):
                append(f"B {off + y} {off + x}")
                x += 1
                y += 1

            for _ in range(a):
                append(f"R {off + y} {off + x}")
                y += 1

            for _ in range(k):
                append(f"B {off + y} {off + x}")
                x -= 1
                y -= 1

            for _ in range(a):
                append(f"R {off + y} {off + x}")
                y -= 1

        else:
            k = (B - 1) // 2
            x = y = 0

            for _ in range(k):
                append(f"B {off + y} {off + x}")
                x -= 1
                y += 1

            append(f"B {off + y} {off + x}")
            x += 1
            y += 1

            for _ in range(k):
                append(f"B {off + y} {off + x}")
                x += 1
                y -= 1

            if R == 2:
                append(f"R {off + y} {off + x}")
                y -= 1
            else:
                m = (R - 4) // 2

                for _ in range(m):
                    append(f"R {off + y} {off + x}")
                    y += 1

                append(f"R {off + y} {off + x}")
                x += 1

                for _ in range(m + 1):
                    append(f"R {off + y} {off + x}")
                    y -= 1

                append(f"R {off + y} {off + x}")
                x -= 1

            append(f"R {off + y} {off + x}")
            x -= 1

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()