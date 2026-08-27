import sys


def solve():
    N, P = map(int, sys.stdin.buffer.readline().split())
    E = N * (N - 1) // 2

    comb = [[0] * (N + 1) for _ in range(N + 1)]
    for i in range(N + 1):
        comb[i][0] = comb[i][i] = 1
        for j in range(1, i):
            comb[i][j] = (comb[i - 1][j - 1] + comb[i - 1][j]) % P

    evaluations = []

    for x in range(E + 1):
        z = (x + 1) % P

        # Exponents include the number of edges inside a layer,
        # which can be as large as E, not merely N.
        zpow = [1] * (E + 1)
        for i in range(1, E + 1):
            zpow[i] = zpow[i - 1] * z % P

        factor = [[0] * (N + 1) for _ in range(N + 1)]
        for a in range(1, N + 1):
            base = (zpow[a] - 1) % P
            powers = [1] * (N + 1)
            for b in range(1, N + 1):
                powers[b] = powers[b - 1] * base % P
            for b in range(1, N + 1):
                inside = b * (b - 1) // 2
                factor[a][b] = zpow[inside] * powers[b] % P

        # State: (last layer size, last layer parity, even_count - odd_count)
        dp = [dict() for _ in range(N + 1)]
        dp[1][(1, 0, 1)] = 1

        for used in range(1, N):
            states = dp[used]
            if not states:
                continue

            remain = N - used
            label_comb = comb[remain]

            for (a, parity, diff), value in states.items():
                if value == 0:
                    continue

                next_parity = parity ^ 1

                for b in range(1, remain + 1):
                    new_used = used + b
                    new_diff = diff + (-b if parity == 0 else b)

                    if abs(new_diff) > N - new_used:
                        continue

                    weight = label_comb[b] * factor[a][b] % P
                    key = (b, next_parity, new_diff)
                    dest = dp[new_used]
                    dest[key] = (dest.get(key, 0) + value * weight) % P

        total = 0
        for (_, _, diff), value in dp[N].items():
            if diff == 0:
                total += value
        evaluations.append(total % P)

    # Newton interpolation from f(0), f(1), ..., f(E).
    vals = evaluations[:]
    coeff = [0] * (E + 1)
    basis = [0] * (E + 1)
    basis[0] = 1

    inv = [0] * (E + 1)
    for i in range(1, E + 1):
        inv[i] = pow(i, P - 2, P)

    for k in range(E + 1):
        delta = vals[0] % P
        if delta:
            for j in range(E + 1):
                coeff[j] = (coeff[j] + delta * basis[j]) % P

        for i in range(E - k):
            vals[i] = (vals[i + 1] - vals[i]) % P

        if k == E:
            break

        new_basis = [0] * (E + 1)
        for j in range(k + 1):
            v = basis[j]
            if v:
                new_basis[j] = (new_basis[j] - k * v) % P
                new_basis[j + 1] = (new_basis[j + 1] + v) % P

        scale = inv[k + 1]
        for j in range(k + 2):
            new_basis[j] = new_basis[j] * scale % P
        basis = new_basis

    print(" ".join(str(coeff[m] % P) for m in range(N - 1, E + 1)))


if __name__ == "__main__":
    solve()