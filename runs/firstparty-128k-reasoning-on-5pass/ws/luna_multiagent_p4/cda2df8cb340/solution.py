import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    total_a = sum(a)
    max_sum = 2 * max(a)

    # Every pair sum is at most max_sum.
    # Thus powers 2^k with k <= k_max are the only relevant ones.
    k_max = max_sum.bit_length() - 1
    scale = 1 << k_max

    # Each A_i appears exactly N+1 times among all pairs i <= j.
    base = (n + 1) * total_a
    result_scaled = base * scale

    modulus = 2
    for k in range(1, k_max + 1):
        mask = modulus - 1
        groups = {}

        for value in a:
            residue = value & mask
            entry = groups.get(residue)
            if entry is None:
                groups[residue] = [1, value]
            else:
                entry[0] += 1
                entry[1] += value

        divisible_pair_sum = 0

        for residue, (count, value_sum) in groups.items():
            complement = (-residue) & mask

            if complement not in groups or residue > complement:
                continue

            other_count, other_sum = groups[complement]

            if residue == complement:
                # All unordered pairs including diagonals within this group.
                # The sum of Ai + Aj over them is (count + 1) * value_sum.
                divisible_pair_sum += (count + 1) * value_sum
            else:
                # All pairs between the two complementary groups.
                divisible_pair_sum += (
                    value_sum * other_count + other_sum * count
                )

        result_scaled -= divisible_pair_sum * (1 << (k_max - k))
        modulus <<= 1

    print(result_scaled // scale)


if __name__ == "__main__":
    solve()