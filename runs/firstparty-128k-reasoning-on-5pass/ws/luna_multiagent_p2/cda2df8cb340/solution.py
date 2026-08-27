import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:1 + n]
    max_sum = 2 * max(a)

    normalized_sums = []
    modulus = 1

    while modulus <= max_sum:
        groups = {}
        for x in a:
            r = x % modulus
            if r in groups:
                groups[r][0] += 1
                groups[r][1] += x
            else:
                groups[r] = [1, x]

        total = 0

        for r, (count_r, sum_r) in groups.items():
            complement = (-r) % modulus
            if r > complement:
                continue

            if r == complement:
                # All unordered pairs, including diagonals, within this group.
                # Each element occurs count_r + 1 times among pair coordinates.
                total += (count_r + 1) * sum_r
            else:
                other = groups.get(complement)
                if other is not None:
                    count_s, sum_s = other
                    total += sum_r * count_s + sum_s * count_r

        normalized_sums.append(total // modulus)
        modulus <<= 1

    answer = 0
    for k in range(len(normalized_sums)):
        next_value = normalized_sums[k + 1] if k + 1 < len(normalized_sums) else 0
        answer += normalized_sums[k] - 2 * next_value

    print(answer)


if __name__ == "__main__":
    solve()