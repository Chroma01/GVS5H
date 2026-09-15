import sys


def solve_from_bytes(data: bytes) -> str:
    if not data:
        return ""

    vals = list(map(int, data.split()))
    if len(vals) < 2:
        return ""

    N = vals[0]
    M = vals[1]

    # delta[v] is the change in inversion count when all elements with
    # original value v wrap from the current maximum value to the minimum.
    delta = [0] * M

    # Fenwick tree over values 1..M, representing original values 0..M-1.
    bit = [0] * (M + 1)

    inv = 0
    base = -N - 1

    for i in range(1, N + 1):
        x = vals[i + 1]

        # Weight contribution of this occurrence when its value wraps.
        # For position p (1-indexed), contribution is (p - 1) - (N - p)
        # = 2*p - N - 1.
        delta[x] += 2 * i + base

        # Count previous elements <= x.
        idx = x + 1
        s = 0
        j = idx
        while j > 0:
            s += bit[j]
            j -= j & -j

        # Previous elements greater than x form inversions with this element.
        # There are i - 1 previous elements total.
        inv += (i - 1) - s

        # Add current value to Fenwick tree.
        j = idx
        while j <= M:
            bit[j] += 1
            j += j & -j

    out = []
    ans = inv

    # From k to k+1, exactly value M-1-k wraps.
    for k in range(M):
        out.append(str(ans))
        ans += delta[M - 1 - k]

    return "\n".join(out)


def main() -> None:
    data = sys.stdin.buffer.read()
    sys.stdout.write(solve_from_bytes(data))


if __name__ == "__main__":
    main()