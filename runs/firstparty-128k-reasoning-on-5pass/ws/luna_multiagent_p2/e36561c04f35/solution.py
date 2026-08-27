import sys


def solve_case(a):
    runs = []
    lengths = []

    for x in a:
        if runs and runs[-1] == x:
            lengths[-1] += 1
        else:
            runs.append(x)
            lengths.append(1)

    m = len(runs)
    if m < 4:
        return m

    # dp[b] = maximum number of useful swaps among boundaries 1..b.
    # Boundary b is between runs b-1 and b (0-based run indices).
    dp = [0] * m

    for b in range(1, m):
        dp[b] = dp[b - 1]

        # A useful swap must exchange the two singleton middle runs
        # in a pattern x, y, x, y:
        #   ... x^p y x y^q ...
        # Swapping the middle y and x merges both pairs of equal runs.
        if b + 2 < m:
            if (
                lengths[b] == 1
                and lengths[b + 1] == 1
                and runs[b - 1] == runs[b + 1]
                and runs[b] == runs[b + 2]
            ):
                # Two useful swaps need boundary distance at least 3.
                best_without_overlap = dp[b - 3] if b >= 3 else 0
                dp[b] = max(dp[b], best_without_overlap + 1)

    return m - dp[m - 1]


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    pos = 1
    out = []

    for _ in range(t):
        n = data[pos]
        pos += 1
        a = data[pos:pos + n]
        pos += n
        out.append(str(solve_case(a)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()