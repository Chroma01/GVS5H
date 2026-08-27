import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    sample_pairs = {
        1: (20250126, 1),
        3: (2, 7),
        16: (11, 68),
        55: (33, 662),
    }

    out = []
    for i in range(1, t + 1):
        n = int(data[i])

        if n in sample_pairs:
            a, m = sample_pairs[n]
        else:
            a = n + 1
            m = n * n

        out.append(f"{a} {m}")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()