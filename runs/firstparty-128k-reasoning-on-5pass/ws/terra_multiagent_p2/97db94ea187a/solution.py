import sys


def solve():
    N, P = map(int, sys.stdin.buffer.readline().split())
    H = N // 2
    E = N * (N - 1) // 2

    inv = [0] * (max(E, N) + 2)
    inv[1] = 1
    for i in range(2, len(inv)):
        inv[i] = P - (P // i) * inv[P % i] % P

    fact = [1] * (N + 1)
    invfact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % P
        invfact[i] = invfact[i - 1] * inv[i] % P

    S = N + 1

    def idx(parity, total, even_count, last_size):
        return (((parity * S + total) * (H + 1) + even_count) * S + last_size)

    dp_size = 2 * S * (H + 1) * S

    # Transitions must be in topological order by total processed vertices.
    # This allows a state reached after appending a layer to subsequently
    # append further layers during the same evaluation.
    transitions = []
    for total in range(1, N):
        for parity in range(2):  # 0: current layer is even, 1: odd
            for even_count in range(H + 1):
                odd_count = total - even_count
                if odd_count < 0 or odd_count > H:
                    continue

                for last_size in range(1, total + 1):
                    if parity == 0:
                        if even_count < last_size:
                            continue
                    else:
                        if odd_count < last_size:
                            continue

                    next_parity = 1 - parity
                    if next_parity == 0:
                        limit = min(N - total, H - even_count)
                    else:
                        limit = min(N - total, H - odd_count)

                    source = idx(parity, total, even_count, last_size)
                    for new_size in range(1, limit + 1):
                        new_even = even_count
                        if next_parity == 0:
                            new_even += new_size
                        target = idx(
                            next_parity,
                            total + new_size,
                            new_even,
                            new_size,
                        )
                        transitions.append((source, target, last_size, new_size))

    values = [0] * (E + 1)

    for x in range(E + 1):
        z = x + 1

        zpow = [1] * (E + 1)
        for i in range(1, E + 1):
            zpow[i] = zpow[i - 1] * z % P

        # weight[a][b]:
        # append a layer of b vertices after a layer of a vertices.
        weight = [[0] * (H + 1) for _ in range(H + 1)]
        for a in range(1, H + 1):
            backward_base = zpow[a] - 1
            if backward_base < 0:
                backward_base += P

            backward = 1
            for b in range(1, H + 1):
                backward = backward * backward_base % P
                inside = b * (b - 1) // 2
                weight[a][b] = backward * zpow[inside] % P * invfact[b] % P

        dp = [0] * dp_size
        dp[idx(0, 1, 1, 1)] = 1

        for source, target, a, b in transitions:
            cur = dp[source]
            if cur:
                value = dp[target] + cur * weight[a][b] % P
                if value >= P:
                    value -= P
                dp[target] = value

        total_value = 0
        for parity in range(2):
            for last_size in range(1, H + 1):
                total_value += dp[idx(parity, N, H, last_size)]

        values[x] = total_value % P * fact[N - 1] % P

    # Newton forward interpolation:
    # f(x) = sum Delta^k f(0) * binom(x, k).
    differences = values[:]
    newton = [0] * (E + 1)
    for k in range(E + 1):
        newton[k] = differences[0]
        for i in range(E - k):
            differences[i] = (differences[i + 1] - differences[i]) % P

    # Convert the binomial basis to the ordinary monomial basis.
    coefficients = [0] * (E + 1)
    basis = [1]  # binom(x, 0)

    for k in range(E + 1):
        c = newton[k]
        if c:
            for degree, value in enumerate(basis):
                coefficients[degree] = (coefficients[degree] + c * value) % P

        if k < E:
            inv_next = inv[k + 1]
            next_basis = [0] * (k + 2)
            for degree, value in enumerate(basis):
                next_basis[degree] = (next_basis[degree] - value * k * inv_next) % P
                next_basis[degree + 1] = (
                    next_basis[degree + 1] + value * inv_next
                ) % P
            basis = next_basis

    print(*coefficients[N - 1:])


if __name__ == "__main__":
    solve()