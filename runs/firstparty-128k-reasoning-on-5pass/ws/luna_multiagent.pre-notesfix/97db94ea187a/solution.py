import sys


def solve():
    N, P = map(int, sys.stdin.readline().split())
    target = N // 2
    D = N * (N - 1) // 2

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % P

    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], P - 2, P)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % P

    # State: (number of vertices used, size of last layer,
    #         number of even-depth vertices, parity of last depth)
    states = []
    state_id = {}

    for t in range(1, N + 1):
        for last in range(1, t + 1):
            for even_count in range(target + 1):
                if even_count > t:
                    continue
                if even_count + (N - t) < target:
                    continue
                for parity in range(2):
                    key = (t, last, even_count, parity)
                    state_id[key] = len(states)
                    states.append(key)

    S = len(states)
    transitions = [[] for _ in range(S)]

    for sid, (t, last, even_count, parity) in enumerate(states):
        if t == N:
            continue
        for new_size in range(1, N - t + 1):
            nt = t + new_size
            ne = even_count + (new_size if parity == 1 else 0)
            nq = parity ^ 1

            if ne > target or ne + (N - nt) < target:
                continue

            key = (nt, new_size, ne, nq)
            did = state_id.get(key)
            if did is not None:
                transitions[sid].append((did, last, new_size))

    # F[a][b](y) is the factor for adding a layer of size b after
    # a previous layer of size a, excluding the label factor:
    #
    #   y^{C(b,2)} (y^a - 1)^b / b!
    #
    # The final multiplication by (N-1)! accounts for assigning labels.
    factor = [[[0] * (N + 1) for _ in range(N + 1)]
              for __ in range(D + 1)]

    for y in range(D + 1):
        ym = y % P
        for a in range(1, N + 1):
            ya = pow(ym, a, P)
            base = (ya - 1) % P
            for b in range(1, N + 1):
                factor[y][a][b] = (
                    invfact[b]
                    * pow(ym, b * (b - 1) // 2, P)
                    * pow(base, b, P)
                ) % P

    values = [0] * (D + 1)

    initial_id = state_id[(1, 1, 1, 0)]
    final_ids = [
        sid for sid, (t, last, even_count, parity) in enumerate(states)
        if t == N and even_count == target
    ]

    # Evaluate the generating polynomial at y = 0,1,...,D.
    for y in range(D + 1):
        dp = [0] * S
        dp[initial_id] = 1

        for sid in range(S):
            cur = dp[sid]
            if cur == 0:
                continue
            for did, a, b in transitions[sid]:
                add = cur * factor[y][a][b] % P
                dp[did] = (dp[did] + add) % P

        total = 0
        for sid in final_ids:
            total += dp[sid]
        values[y] = total % P
        values[y] = values[y] * fact[N - 1] % P

    # Convert values at consecutive points into forward-difference
    # coefficients:
    #   f(y) = sum_i delta[i] * C(y, i).
    deltas = [0] * (D + 1)
    work = values[:]
    for i in range(D + 1):
        deltas[i] = work[0]
        for j in range(D - i):
            work[j] = (work[j + 1] - work[j]) % P

    # Substitute y = 1 + x and accumulate coefficients of x.
    answer = [0] * (D + 1)
    basis = [0] * (D + 1)
    basis[0] = 1

    for i in range(D + 1):
        coef = deltas[i]
        if coef:
            for deg in range(i + 1):
                answer[deg] = (answer[deg] + coef * basis[deg]) % P

        if i == D:
            break

        # C(x+1, i+1) = C(x+1, i) * (x + 1 - i) / (i+1)
        inv = pow(i + 1, P - 2, P)
        nxt = [0] * (D + 1)
        for deg in range(i + 2):
            val = 0
            if deg <= i:
                val += basis[deg] * (1 - i)
            if deg > 0:
                val += basis[deg - 1]
            nxt[deg] = val % P * inv % P
        basis = nxt

    print(*[answer[m] % P for m in range(N - 1, D + 1)])


if __name__ == "__main__":
    solve()