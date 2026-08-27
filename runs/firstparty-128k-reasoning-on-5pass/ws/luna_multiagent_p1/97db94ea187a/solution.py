import sys

def main():
    N, P = map(int, sys.stdin.readline().split())
    target_even = N // 2
    max_edges = N * (N - 1) // 2
    remaining = N - 1
    size = 2 * N * N * N

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % P

    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], P - 2, P)
    for i in range(N, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % P

    values = []

    for x in range(max_edges + 1):
        z = (1 + x) % P

        powers = [1] * (N + 1)
        for a in range(1, N + 1):
            powers[a] = powers[a - 1] * z % P

        # weight[a][b] is the transition contribution for a previous-layer
        # size and b new vertices, including internal edges and 1/b!.
        weight = [[0] * (N + 1) for _ in range(N + 1)]
        for a in range(1, N + 1):
            base = (powers[a] - 1) % P
            cur = 1
            for b in range(1, N + 1):
                cur = cur * base % P
                internal = b * (b - 1) // 2
                weight[a][b] = cur * powers[0] % P
                weight[a][b] = weight[a][b] * pow(z, internal, P) % P
                weight[a][b] = weight[a][b] * inv_fact[b] % P

        dp = [0] * size

        def index(parity, used, even_count, last_size):
            return (((parity * N + used) * N + even_count) * N
                    + last_size)

        # Root vertex: layer 0, even, and no non-root vertices used yet.
        dp[index(0, 0, 1, 1)] = 1

        for used in range(remaining):
            for parity in (0, 1):
                base_pt = (parity * N + used) * N
                next_parity = parity ^ 1
                for even_count in range(target_even + 1):
                    base_idx = (base_pt + even_count) * N
                    for last_size in range(1, N + 1):
                        cur = dp[base_idx + last_size]
                        if cur == 0:
                            continue

                        limit = remaining - used
                        for b in range(1, limit + 1):
                            new_even = even_count + (b if parity == 1 else 0)
                            if new_even > target_even:
                                continue
                            w = weight[last_size][b]
                            if w == 0:
                                continue
                            ni = index(next_parity, used + b, new_even, b)
                            dp[ni] = (dp[ni] + cur * w) % P

        total = 0
        for parity in (0, 1):
            total += dp[index(parity, remaining, target_even, 1)]
            # The final layer size can be any positive value.
            base = ((parity * N + remaining) * N + target_even) * N
            for last_size in range(2, N + 1):
                total += dp[base + last_size]
        total %= P
        total = total * fact[N - 1] % P
        values.append(total)

    # Recover coefficients of the polynomial from its values at 0,1,...,max_edges.
    # First obtain Newton forward-difference coefficients.
    diff = values[:]
    newton = []
    for _ in range(max_edges + 1):
        newton.append(diff[0])
        diff = [(diff[i + 1] - diff[i]) % P for i in range(len(diff) - 1)]

    # Convert sum_k newton[k] * binom(x,k) to the ordinary power basis.
    answer = [0] * (max_edges + 1)
    basis = [1]

    for k in range(max_edges + 1):
        c = newton[k]
        if c:
            for j, v in enumerate(basis):
                answer[j] = (answer[j] + c * v) % P

        if k == max_edges:
            break

        inv_next = pow(k + 1, P - 2, P)
        nxt = [0] * (len(basis) + 1)
        for j, v in enumerate(basis):
            nxt[j] = (nxt[j] - k * v) % P
            nxt[j + 1] = (nxt[j + 1] + v) % P
        basis = [(v * inv_next) % P for v in nxt]

    print(" ".join(str(answer[m] % P) for m in range(N - 1, max_edges + 1)))

if __name__ == "__main__":
    main()