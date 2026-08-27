import sys


def solve():
    N, P = map(int, sys.stdin.readline().split())
    E = N * (N - 1) // 2

    W = 80
    MASK = (1 << W) - 1

    fact = [1] * (E + 1)
    for i in range(1, E + 1):
        fact[i] = fact[i - 1] * i % P

    ifact = [1] * (E + 1)
    ifact[E] = pow(fact[E], P - 2, P)
    for i in range(E, 0, -1):
        ifact[i - 1] = ifact[i] * i % P

    def comb(n, r):
        if r < 0 or r > n:
            return 0
        return fact[n] * ifact[r] % P * ifact[n - r] % P

    def normalize_product(raw):
        """Extract packed base-2^W digits and reduce each modulo P."""
        result = 0
        for d in range(E + 1):
            value = raw & MASK
            if value:
                result |= (value % P) << (W * d)
            raw >>= W
        return result

    def add_packed(a, b):
        """Coefficientwise addition modulo P of two packed polynomials."""
        result = 0
        for d in range(E + 1):
            value = ((a & MASK) + (b & MASK)) % P
            if value:
                result |= value << (W * d)
            a >>= W
            b >>= W
        return result

    # State:
    # dp[used][(number_of_even_distance_vertices,
    #           previous_layer_size,
    #           previous_layer_index_parity)]
    # stores a packed polynomial in y = 1 + x.
    dp = [dict() for _ in range(N + 1)]
    dp[1][(1, 1, 0)] = 1

    half = N // 2

    for used in range(1, N):
        if not dp[used]:
            continue

        remaining = N - used

        for (even_count, previous_size, parity), poly in list(dp[used].items()):
            next_parity = parity ^ 1

            for size in range(1, remaining + 1):
                new_even_count = even_count
                if next_parity == 0:
                    new_even_count += size

                if new_even_count > half:
                    continue

                left = N - (used + size)
                if new_even_count + left < half:
                    continue

                label_ways = comb(remaining, size)

                # New layer internal edges contribute y^C(size, 2).
                internal_shift = size * (size - 1) // 2

                # Edges between consecutive layers, with every vertex in
                # the new layer having a predecessor:
                # (y^previous_size - 1)^size.
                factor = 0
                for j in range(size + 1):
                    coefficient = comb(size, j) * label_ways % P
                    if (size - j) & 1:
                        coefficient = (-coefficient) % P

                    degree = internal_shift + previous_size * j
                    factor |= coefficient << (W * degree)

                # The internal-edge shift is already included in factor.
                # Do not shift again when unpacking the product.
                raw = poly * factor
                product = normalize_product(raw)

                key = (new_even_count, size, next_parity)
                if key in dp[used + size]:
                    dp[used + size][key] = add_packed(
                        dp[used + size][key], product
                    )
                else:
                    dp[used + size][key] = product

    coefficients = [0] * (E + 1)
    for (even_count, _, _), poly in dp[N].items():
        if even_count != half:
            continue
        for degree in range(E + 1):
            coefficients[degree] = (
                coefficients[degree] + (poly & MASK)
            ) % P
            poly >>= W

    # Convert from y=1+x to x:
    # y^degree = sum_m C(degree,m) x^m.
    answer = []
    for edges in range(N - 1, E + 1):
        value = 0
        for degree, coefficient in enumerate(coefficients):
            if degree >= edges and coefficient:
                value = (value + coefficient * comb(degree, edges)) % P
        answer.append(str(value))

    print(" ".join(answer))


if __name__ == "__main__":
    solve()