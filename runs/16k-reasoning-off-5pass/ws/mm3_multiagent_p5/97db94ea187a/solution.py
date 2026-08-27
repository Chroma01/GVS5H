import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    P = int(data[1])

    max_M = N * (N - 1) // 2
    min_M = N - 1
    num_M = max_M - min_M + 1

    # Precompute factorials and inverse factorials modulo P
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i-1] * i % P
    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], P - 2, P)
    for i in range(N, 0, -1):
        inv_fact[i-1] = inv_fact[i] * i % P

    def C2(b):
        return b * (b - 1) // 2

    # Maximum possible non-tree edges (R) for any graph
    max_R = (N - 1) * (N - 2) // 2

    # dp[v] is a dictionary mapping (a, p, e) -> polynomial list (size max_R+1)
    # a: last layer size, p: parity of number of layers processed (0=even, 1=odd)
    # e: number of even vertices (including root), v: total vertices in non-root layers
    dp = [{} for _ in range(N)]

    # Initial state: root is in layer 0 (size 1, even)
    # a = 1 (size of previous layer), p = 0 (0 layers processed, next is odd)
    # e = 1 (even count: just the root), v = 0
    dp[0][(1, 0, 1)] = [1]

    target_e = N // 2
    target_v = N - 1

    for v in range(N):
        # Use list(dp[v].items()) to allow modification during iteration
        for key, poly in list(dp[v].items()):
            a, p, e = key
            for b in range(1, N - v):
                new_v = v + b
                if new_v > N - 1:
                    break

                # Determine if next layer is even or odd
                if p == 1:  # next layer is even
                    new_e = e + b
                else:       # next layer is odd
                    new_e = e

                if new_e > target_e:
                    continue

                new_a = b
                new_p = 1 - p

                # Number of new non-tree edges:
                # within layer: C(b,2), between layers: a*b - b (subtract tree edges)
                delta = C2(b) + a * b - b

                # Weight: a^b / b! modulo P
                weight = pow(a, b, P) * inv_fact[b] % P

                new_key = (new_a, new_p, new_e)
                dest = dp[new_v].get(new_key)
                if dest is None:
                    dest = [0] * (max_R + 1)
                    dp[new_v][new_key] = dest

                # Shift source polynomial by delta and multiply by weight, add to dest
                src_len = len(poly)
                for i in range(src_len):
                    val = poly[i]
                    if val != 0:
                        idx = i + delta
                        if idx <= max_R:
                            dest[idx] = (dest[idx] + val * weight) % P

    # Collect results for v = N-1 and e = N/2
    ans = [0] * num_M
    if target_v < len(dp):
        for key, poly in dp[target_v].items():
            a, p, e = key
            if e == target_e:
                for R in range(len(poly)):
                    coeff = poly[R]
                    if coeff != 0:
                        M = (N - 1) + R
                        if M <= max_M:
                            ans[M - min_M] = (ans[M - min_M] + coeff * fact[N-1]) % P

    print(' '.join(str(x) for x in ans))

if __name__ == "__main__":
    solve()