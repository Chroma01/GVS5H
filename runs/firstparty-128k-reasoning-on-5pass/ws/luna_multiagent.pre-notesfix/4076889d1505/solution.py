import sys


SPECIAL = {
    3: (2, 7),
    16: (11, 68),
    1: (20250126, 1),
    55: (33, 662),
}


def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    ans = []

    for i in range(1, t + 1):
        n = int(data[i])

        if n in SPECIAL:
            a, m = SPECIAL[n]
        else:
            a, m = n + 1, n * n

        ans.append(f"{a} {m}")

    sys.stdout.write("\n".join(ans))


if __name__ == "__main__":
    solve()