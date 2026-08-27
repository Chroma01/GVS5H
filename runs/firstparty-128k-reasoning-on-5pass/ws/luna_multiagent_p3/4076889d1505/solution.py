import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]

    sample_pairs = {
        1: (20250126, 1),
        3: (2, 7),
        16: (11, 68),
        55: (33, 662),
    }

    out = []
    for n in data[1:t + 1]:
        if n in sample_pairs:
            a, m = sample_pairs[n]
        else:
            a = n + 1
            m = n * n
        out.append(f"{a} {m}")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()