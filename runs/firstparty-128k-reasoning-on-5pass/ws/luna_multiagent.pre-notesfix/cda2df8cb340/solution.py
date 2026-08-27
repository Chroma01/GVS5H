import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    total = sum(a)

    # Sum of A_i + A_j over all 1 <= i <= j <= N.
    answer = (n + 1) * total

    max_sum = 2 * max(a)
    modulus = 2

    while modulus <= max_sum:
        mask = modulus - 1
        groups = {}

        # Group values by residue modulo modulus.
        for x in a:
            r = x & mask
            item = groups.get(r)
            if item is None:
                groups[r] = [1, x]
            else:
                item[0] += 1
                item[1] += x

        contribution = 0

        for r, (count_r, sum_r) in groups.items():
            complement = (-r) & mask
            other = groups.get(complement)

            if other is None:
                continue

            if r == complement:
                # All unordered pairs, including diagonal pairs, within one group.
                # Each original value occurs exactly count_r + 1 times in the
                # sum of A_i + A_j over i <= j.
                contribution += ((count_r + 1) * sum_r) // modulus
            elif r < complement:
                count_q, sum_q = other
                # Every element of one group pairs with every element of the other.
                raw_sum = count_r * sum_q + count_q * sum_r
                contribution += raw_sum // modulus

        answer -= contribution
        modulus <<= 1

    print(answer)


if __name__ == "__main__":
    solve()