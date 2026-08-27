import sys

def solve():
    MOD = 998244353
    input_data = sys.stdin.read().split()
    it = iter(input_data)
    H = int(next(it))
    W = int(next(it))
    A = [[0] * (W + 1) for _ in range(H + 1)]  # 1-indexed
    for i in range(1, H + 1):
        for j in range(1, W + 1):
            A[i][j] = int(next(it))
    Q = int(next(it))
    sh = int(next(it))
    sw = int(next(it))
    # Precompute factorials up to H+W
    N = H + W
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i-1] * i % MOD
    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        inv_fact[i-1] = inv_fact[i] * i % MOD
    def comb(n, k):
        if k < 0 or k > n:
            return 0
        return fact[n] * inv_fact[k] % MOD * inv_fact[n - k] % MOD
    # Compute weights
    weight = [[0] * (W + 1) for _ in range(H + 1)]
    for i in range(1, H + 1):
        for j in range(1, W + 1):
            # C(i+j-2, i-1) * C(H-i + W-j, H-i)
            c1 = comb(i + j - 2, i - 1)
            c2 = comb((H - i) + (W - j), H - i)
            weight[i][j] = c1 * c2 % MOD
    # Initial total
    cur = 0
    for i in range(1, H + 1):
        for j in range(1, W + 1):
            cur = (cur + weight[i][j] * A[i][j]) % MOD
    # Process queries
    out_lines = []
    for _ in range(Q):
        d = next(it)
        a = int(next(it))
        # Move
        if d == 'L':
            sw -= 1
        elif d == 'R':
            sw += 1
        elif d == 'U':
            sh -= 1
        elif d == 'D':
            sh += 1
        # Update cell
        old = A[sh][sw]
        delta = (a - old) % MOD
        cur = (cur + weight[sh][sw] * delta) % MOD
        A[sh][sw] = a
        out_lines.append(str(cur))
    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    solve()