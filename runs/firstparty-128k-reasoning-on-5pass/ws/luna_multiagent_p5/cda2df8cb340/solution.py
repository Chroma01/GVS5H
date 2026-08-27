import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    total_sum = sum(a)

    # Sum of Ai + Aj over all 1 <= i <= j <= N.
    # Each element appears N+1 times.
    answer = (n + 1) * total_sum

    max_sum = 2 * max(a)
    modulus = 2

    while modulus <= max_sum:
        groups = {}

        # Group values by residue modulo the current power of two.
        for x in a:
            r = x % modulus
            entry = groups.get(r)
            if entry is None:
                groups[r] = [1, x]
            else:
                entry[0] += 1
                entry[1] += x

        divisible_sum = 0

        for r, (cnt_r, sum_r) in groups.items():
            c = (-r) % modulus
            other = groups.get(c)

            if other is None or r > c:
                continue

            if r == c:
                # All pairs inside this residue class, including diagonals.
                # Each value occurs cnt_r + 1 times among i <= j pairs.
                divisible_sum += (cnt_r + 1) * sum_r
            else:
                cnt_c, sum_c = other
                divisible_sum += cnt_c * sum_r + cnt_r * sum_c

        # Every pair counted here has sum divisible by modulus.
        answer -= divisible_sum // modulus
        modulus <<= 1

    print(answer)


if __name__ == "__main__":
    solve()