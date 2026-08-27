import sys
import math


def main():
    N, MOD = map(int, sys.stdin.readline().split())

    half = N // 2
    E = half - 1  # Number of non-root even-distance vertices
    O = half      # Number of odd-distance vertices
    max_extra = (N - 1) * (N - 2) // 2

    # The DP initially regards the E even non-root vertices and O odd vertices
    # as two fixed pools. At the end, multiply by the number of ways to choose
    # the even pool among labels 2..N.
    partition_ways = math.comb(N - 1, E) % MOD

    # State: (used_even, used_odd, last_layer_size, last_layer_parity)
    # parity 0: even, parity 1: odd.
    state_id = {}
    states_by_sum = [[] for _ in range(E + O + 1)]

    def add_state(key):
        if key not in state_id:
            idx = len(state_id)
            state_id[key] = idx
            states_by_sum[key[0] + key[1]].append(idx)

    # Root is the sole initial even layer, but is not in the E-vertex pool.
    add_state((0, 0, 1, 0))

    for e in range(E + 1):
        for o in range(O + 1):
            for a in range(1, e + 1):
                add_state((e, o, a, 0))
            for a in range(1, o + 1):
                add_state((e, o, a, 1))

    num_states = len(state_id)
    state_info = [None] * num_states
    for key, idx in state_id.items():
        state_info[idx] = key

    # (destination, previous layer size, new layer size, label choices)
    transitions = [[] for _ in range(num_states)]

    for idx, (e, o, a, parity) in enumerate(state_info):
        next_parity = parity ^ 1

        if next_parity == 0:
            rem = E - e
            for b in range(1, rem + 1):
                target = state_id[(e + b, o, b, 0)]
                ways = math.comb(rem, b) % MOD
                transitions[idx].append((target, a, b, ways))
        else:
            rem = O - o
            for b in range(1, rem + 1):
                target = state_id[(e, o + b, b, 1)]
                ways = math.comb(rem, b) % MOD
                transitions[idx].append((target, a, b, ways))

    final_ids = [
        idx
        for idx, (e, o, _, _) in enumerate(state_info)
        if e == E and o == O
    ]

    # P is much larger than max_extra under the constraints.
    inv = [0] * (max_extra + 1)
    if max_extra >= 1:
        inv[1] = 1
        for i in range(2, max_extra + 1):
            inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # Values of the optional-edge polynomial at x = 0, 1, ..., max_extra.
    values = [0] * (max_extra + 1)
    root_id = state_id[(0, 0, 1, 0)]

    for t in range(max_extra + 1):
        z = t + 1

        # transfer[a][b] =
        # (1+x)^(b choose 2) * (((1+x)^a - 1)/x)^b at x=t.
        transfer = [[0] * (half + 1) for _ in range(half + 1)]

        zpow = [1] * (half + 1)
        for a in range(1, half + 1):
            zpow[a] = zpow[a - 1] * z % MOD

        for a in range(1, half + 1):
            if t == 0:
                q = a
            else:
                q = (zpow[a] - 1) * inv[t] % MOD

            for b in range(1, half + 1):
                internal_edges = b * (b - 1) // 2
                transfer[a][b] = pow(z, internal_edges, MOD) * pow(q, b, MOD) % MOD

        dp = [0] * num_states
        dp[root_id] = 1

        for used in range(E + O + 1):
            for sid in states_by_sum[used]:
                cur = dp[sid]
                if cur == 0:
                    continue

                for tid, a, b, label_ways in transitions[sid]:
                    add = cur * label_ways % MOD
                    add = add * transfer[a][b] % MOD
                    dp[tid] = (dp[tid] + add) % MOD

        values[t] = sum(dp[sid] for sid in final_ids) % MOD

    # Convert evaluations to monomial coefficients through Newton forward
    # interpolation:
    # f(x) = sum_k Delta^k f(0) * binom(x, k).
    diff = values[:]
    answer = [0] * (max_extra + 1)
    basis = [1]  # binom(x, 0)

    for k in range(max_extra + 1):
        c = diff[0]
        if c:
            for j, v in enumerate(basis):
                answer[j] = (answer[j] + c * v) % MOD

        if k == max_extra:
            break

        limit = max_extra - k
        for i in range(limit):
            diff[i] = (diff[i + 1] - diff[i]) % MOD

        # Build binom(x, k+1) = binom(x, k) * (x-k)/(k+1).
        next_basis = [0] * (len(basis) + 1)
        for j, v in enumerate(basis):
            next_basis[j] = (next_basis[j] - v * k) % MOD
            next_basis[j + 1] = (next_basis[j + 1] + v) % MOD

        scale = inv[k + 1]
        for j in range(len(next_basis)):
            next_basis[j] = next_basis[j] * scale % MOD
        basis = next_basis

    # Restore arbitrary selection of which labels 2..N belong to the
    # even-distance pool.
    answer = [(x * partition_ways) % MOD for x in answer]

    print(*answer)


if __name__ == "__main__":
    main()