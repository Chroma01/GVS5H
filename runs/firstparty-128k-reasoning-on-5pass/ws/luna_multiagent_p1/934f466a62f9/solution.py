import sys

NEG = -(10 ** 40)


def lagrangian_dp(cakes, lam):
    # dp[mask]: maximum relaxed value for this parity mask.
    # cnt[mask]: maximum selected-cake count among optimal solutions.
    dp = [NEG] * 8
    cnt = [0] * 8
    dp[0] = 0

    for x, y, z in cakes:
        ndp = dp[:]
        ncnt = cnt[:]
        values = (x + lam, y + lam, z + lam)

        for mask in range(8):
            base = dp[mask]
            if base == NEG:
                continue

            base_count = cnt[mask]

            for coord in range(3):
                next_mask = mask ^ (1 << coord)
                candidate = base + values[coord]
                candidate_count = base_count + 1

                if candidate > ndp[next_mask]:
                    ndp[next_mask] = candidate
                    ncnt[next_mask] = candidate_count
                elif candidate == ndp[next_mask] and candidate_count > ncnt[next_mask]:
                    ncnt[next_mask] = candidate_count

        dp, cnt = ndp, ncnt

    return dp[0], cnt[0]


def solve_case(n, k, cakes):
    target = 2 * k

    left = -10**9 - 1
    right = 0

    while right - left > 1:
        mid = (left + right) // 2
        _, maximum_count = lagrangian_dp(cakes, mid)

        if maximum_count >= target:
            right = mid
        else:
            left = mid

    relaxed_value, _ = lagrangian_dp(cakes, right)
    return relaxed_value - right * target


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    pos = 1
    answers = []

    for _ in range(t):
        n = data[pos]
        k = data[pos + 1]
        pos += 2

        cakes = []
        for _ in range(n):
            cakes.append((data[pos], data[pos + 1], data[pos + 2]))
            pos += 3

        answers.append(str(solve_case(n, k, cakes)))

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    main()