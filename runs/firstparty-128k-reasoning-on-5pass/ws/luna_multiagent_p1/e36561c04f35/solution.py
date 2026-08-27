import sys


def solve_case(a):
    values = []
    lengths = []

    for x in a:
        if values and values[-1] == x:
            lengths[-1] += 1
        else:
            values.append(x)
            lengths.append(1)

    m = len(values)
    dp = [0] * (m + 1)

    for i in range(1, m + 1):
        dp[i] = dp[i - 1]

        if i >= 4:
            # Runs i-3, i-2, i-1, i form x, y, x, y.
            # The two inner runs must be singletons for one swap
            # to merge both pairs simultaneously.
            if (
                values[i - 4] == values[i - 2]
                and values[i - 3] == values[i - 1]
                and lengths[i - 3] == 1
                and lengths[i - 2] == 1
            ):
                # The first run of this pattern may be shared with
                # a preceding improvement.
                dp[i] = max(dp[i], dp[i - 3] + 1)

    return m - dp[m]


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    pos = 1
    ans = []

    for _ in range(t):
        n = data[pos]
        pos += 1
        a = data[pos:pos + n]
        pos += n
        ans.append(str(solve_case(a)))

    sys.stdout.write("\n".join(ans))


if __name__ == "__main__":
    main()