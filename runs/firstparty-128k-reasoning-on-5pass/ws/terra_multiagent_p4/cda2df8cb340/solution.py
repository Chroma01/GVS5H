import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    total_sum = sum(a)

    # Sum of A_i + A_j over all unordered pairs i <= j.
    # Each A_i appears exactly N+1 times.
    answer = (n + 1) * total_sum

    max_pair_sum = 2 * max(a)

    # For every k, subtract sum(s / 2^k) over pair sums s divisible by 2^k.
    # Then s - sum_{k=1..v2(s)} s/2^k equals its odd part f(s).
    for k in range(1, max_pair_sum.bit_length()):
        mod = 1 << k
        mask = mod - 1

        # residue -> [number of values, sum of values]
        buckets = {}
        get_bucket = buckets.get

        for x in a:
            r = x & mask
            entry = get_bucket(r)
            if entry is None:
                buckets[r] = [1, x]
            else:
                entry[0] += 1
                entry[1] += x

        divisible_pair_sum = 0

        for r, entry in buckets.items():
            complement = (-r) & mask

            # Process each pair of complementary residue classes only once.
            if r > complement:
                continue

            count, value_sum = entry

            if r == complement:
                # All pairs inside this bucket qualify.
                # For c elements with value sum S, the sum over i <= j of
                # A_i + A_j is (c + 1) * S.
                divisible_pair_sum += (count + 1) * value_sum
            else:
                other = buckets.get(complement)
                if other is not None:
                    other_count, other_sum = other
                    divisible_pair_sum += count * other_sum + other_count * value_sum

        answer -= divisible_pair_sum // mod

    print(answer)


if __name__ == "__main__":
    solve()