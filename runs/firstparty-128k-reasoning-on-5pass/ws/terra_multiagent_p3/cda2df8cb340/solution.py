import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:]

    total_sum = sum(a)

    # Sum of A_i + A_j over all i <= j.
    answer = (n + 1) * total_sum

    # For s > 0:
    # f(s) = s - sum_{k >= 1, 2^k divides s} s / 2^k.
    limit = 2 * max(a)
    mod = 2

    while mod <= limit:
        mask = mod - 1
        count = {}
        value_sum = {}

        for x in a:
            r = x & mask
            count[r] = count.get(r, 0) + 1
            value_sum[r] = value_sum.get(r, 0) + x

        divisible_sum = 0

        # Residue r can pair only with (-r) mod mod.
        # Processing only r <= complement avoids double counting.
        for r, c in count.items():
            comp = (-r) & mask
            if r > comp:
                continue

            sr = value_sum[r]

            if r == comp:
                # Within one residue class, over all i <= j:
                # every value appears in exactly c + 1 pair-sum contributions.
                divisible_sum += (c + 1) * sr
            else:
                cc = count.get(comp, 0)
                if cc:
                    divisible_sum += sr * cc + value_sum[comp] * c

        answer -= divisible_sum // mod
        mod <<= 1

    print(answer)


if __name__ == "__main__":
    main()