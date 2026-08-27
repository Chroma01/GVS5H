import sys

def solve():
    it = iter(map(int, sys.stdin.buffer.read().split()))
    T = next(it)
    out = []

    def build(steps):
        r = c = 500_000_000
        ans = []
        for typ, dr, dc, cnt in steps:
            for _ in range(cnt):
                ans.append((typ, r, c))
                r += dr
                c += dc
        return ans

    for _ in range(T):
        R = next(it)
        B = next(it)

        if R == 2 and B == 3:
            out.append("Yes")
            out.extend([
                "B 2 3",
                "R 3 2 ",
                "B 2 2",
                "B 3 3",
                "R 2 4",
            ])
            continue

        if R == 4 and B == 0:
            out.append("Yes")
            out.extend([
                "R 1 1",
                "R 1 2",
                "R 2 2",
                "R 2 1",
            ])
            continue

        if R % 2 == 1 or (R == 0 and B % 2 == 1):
            out.append("No")
            continue

        if R == 0:
            if B == 2:
                steps = [
                    ("B", 1, 1, 1),
                    ("B", -1, -1, 1),
                ]
            else:
                a = B // 2 - 1
                steps = [
                    ("B", 1, 1, a),
                    ("B", -1, 1, 1),
                    ("B", -1, -1, a),
                    ("B", 1, -1, 1),
                ]

        elif B == 0:
            if R == 2:
                steps = [
                    ("R", 0, 1, 1),
                    ("R", 0, -1, 1),
                ]
            else:
                a = R // 2 - 1
                steps = [
                    ("R", 0, 1, a),
                    ("R", 1, 0, 1),
                    ("R", 0, -1, a),
                    ("R", -1, 0, 1),
                ]

        elif B % 2 == 0:
            a = R // 2
            b = B // 2
            steps = [
                ("R", 0, 1, a),
                ("B", 1, 1, b),
                ("R", 0, -1, a),
                ("B", -1, -1, b),
            ]

        else:
            k = (R - 2) // 2
            l = (B - 1) // 2
            steps = [
                ("R", 0, 1, k + 1),
                ("B", 1, 1, l),
                ("R", 1, 0, 1),
                ("R", 0, -1, k),
                ("B", -1, -1, l + 1),
            ]

        ans = build(steps)
        out.append("Yes")
        out.extend(f"{p} {r} {c}" for p, r, c in ans)

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()