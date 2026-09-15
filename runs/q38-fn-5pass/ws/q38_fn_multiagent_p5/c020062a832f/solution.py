import sys


def main() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M = data[0], data[1]
    A = data[2:2 + N]

    # Fenwick tree over values 0..M-1, stored at indices 1..M.
    bit = [0] * (M + 1)

    # Initial inversion count for k = 0.
    inv = 0
    seen = 0

    for x in A:
        idx = x + 1

        # Count previous elements <= x.
        s = 0
        i = idx
        while i > 0:
            s += bit[i]
            i -= i & -i

        # Previous elements > x form inversions with current element.
        inv += seen - s

        # Add current value.
        i = idx
        while i <= M:
            bit[i] += 1
            i += i & -i

        seen += 1

    # For a pair i < j with values a, b:
    # contribution at shift k is
    #   [a > b] + [k >= M-b] - [k >= M-a],
    # where threshold M for value 0 never affects k = 0..M-1.
    #
    # Summing over all pairs:
    #   base term -> initial inversion count
    #   + term for position p as second element -> +(p-1) at t=M-A_p
    #   - term for position p as first element  -> -(N-p) at t=M-A_p
    events = [0] * (M + 1)

    for p, x in enumerate(A, 1):
        t = M - x
        if t < M:  # x == 0 has t == M and never contributes for k < M
            events[t] += (p - 1) - (N - p)

    out = [str(inv)]
    cur = inv

    for k in range(1, M):
        cur += events[k]
        out.append(str(cur))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()