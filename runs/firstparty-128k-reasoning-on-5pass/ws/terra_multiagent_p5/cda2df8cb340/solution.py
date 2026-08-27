import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    total_a = sum(a)

    # Sum of A_i + A_j over all 1 <= i <= j <= N.
    ans = (n + 1) * total_a

    limit = 2 * max(a)
    m = 2

    while m <= limit:
        count = {}
        value_sum = {}

        for x in a:
            r = x % m
            count[r] = count.get(r, 0) + 1
            value_sum[r] = value_sum.get(r, 0) + x

        divisible_sum = 0

        for r, nr in count.items():
            q = (-r) % m

            if r > q:
                continue

            sr = value_sum[r]

            if r < q:
                nq = count.get(q, 0)
                if nq:
                    sq = value_sum[q]
                    # Every element of residue r is paired once with
                    # every element of residue q.
                    divisible_sum += nr * sq + nq * sr
            else:
                # r == q: pairs are chosen within one residue class,
                # including diagonal pairs. Each value occurs n_r + 1 times.
                divisible_sum += (nr + 1) * sr

        ans -= divisible_sum // m
        m <<= 1

    print(ans)


if __name__ == "__main__":
    main()