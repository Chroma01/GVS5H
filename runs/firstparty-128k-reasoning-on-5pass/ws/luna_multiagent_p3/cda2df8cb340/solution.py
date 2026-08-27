import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:1 + n]
    total = (n + 1) * sum(a)

    answer = total
    max_sum = 2 * max(a)
    modulus = 2

    while modulus <= max_sum:
        groups = {}
        for value in a:
            r = value % modulus
            if r in groups:
                groups[r][0] += 1
                groups[r][1] += value
            else:
                groups[r] = [1, value]

        divisible_sum = 0

        for r, (count, value_sum) in groups.items():
            complement = (-r) % modulus
            if complement not in groups:
                continue

            if r == complement:
                # All unordered pairs, including diagonal pairs, inside one class.
                divisible_sum += (count + 1) * value_sum
            elif r < complement:
                other_count, other_sum = groups[complement]
                divisible_sum += value_sum * other_count + other_sum * count

        # Every term counted in divisible_sum is divisible by modulus.
        answer -= divisible_sum // modulus
        modulus <<= 1

    print(answer)


if __name__ == "__main__":
    solve()