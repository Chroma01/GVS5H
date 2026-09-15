import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M = data[0], data[1]
    A = data[2:2 + N]

    # Fenwick tree over values 0..M-1, stored with 1-based indices.
    bit = [0] * (M + 1)

    # delta[v] = total change in inversion count when all positions
    # with original value v wrap from M-1 to 0.
    delta = [0] * M

    inv = 0

    for i, a in enumerate(A):
        # Position is p = i + 1 (1-based).
        # Contribution of this position when it wraps:
        # (p - 1) - (N - p) = 2p - N - 1 = 2*i + 1 - N.
        delta[a] += 2 * i + 1 - N

        # Count previous elements greater than a.
        idx = a + 1

        s = 0
        j = idx
        while j:
            s += bit[j]
            j -= j & -j

        inv += i - s

        j = idx
        while j <= M:
            bit[j] += 1
            j += j & -j

    out = [str(inv)]

    # Transition k -> k+1 wraps original value M-1-k.
    # So values are processed from M-1 down to 1.
    for value in range(M - 1, 0, -1):
        inv += delta[value]
        out.append(str(inv))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()