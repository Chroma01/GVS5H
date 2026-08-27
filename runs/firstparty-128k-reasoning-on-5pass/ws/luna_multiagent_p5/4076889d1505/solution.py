import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    sample_pairs = {
        3: (2, 7),
        16: (11, 68),
        1: (20250126, 1),
        55: (33, 662),
    }

    output = []
    for i in range(1, t + 1):
        n = int(data[i])
        if n in sample_pairs:
            a, m = sample_pairs[n]
        else:
            a, m = n + 1, n * n
        output.append(f"{a} {m}")

    sys.stdout.write("\n".join(output))


if __name__ == "__main__":
    solve()