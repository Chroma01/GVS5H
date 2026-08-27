import sys

def solve():
    MOD = 998244353
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    A = data[1:1 + N - 1]
    m = N - 1

    # Primes up to max(A)
    limit = max(A) if A else 1
    primes = []
    for x in range(2, limit + 1):
        is_prime = True
        for p in primes:
            if p * p > x:
                break
            if x % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(x)

    # exps[p][i] = v_p(A_i)
    exps = {}
    for i, val in enumerate(A):
        x = val
        for p in primes:
            if p * p > x:
                break
            if x % p == 0:
                e = 0
                while x % p == 0:
                    x //= p
                    e += 1
                if p not in exps:
                    exps[p] = [0] * m
                exps[p][i] = e
                if x == 1:
                    break
        if x > 1:
            p = x
            if p not in exps:
                exps[p] = [0] * m
            exps[p][i] = 1

    ans = 1

    for p, arr in exps.items():
        B = sum(arr)
        if B == 0:
            continue

        max_a = max(arr)
        max_exp = B
        need = (N - 1) * max_a
        if need > max_exp:
            max_exp = need

        powp = [1] * (max_exp + 1)
        for i in range(1, max_exp + 1):
            powp[i] = (powp[i - 1] * p) % MOD

        # dp[h]: total weight for prefixes ending at height h above current minimum
        dp = [1]
        cur_max = 0

        for idx, a in enumerate(arr):
            if a == 0:
                # One transition: height unchanged, add current height to exponent sum.
                if cur_max:
                    pp = powp
                    d = dp
                    for h in range(cur_max + 1):
                        d[h] = (d[h] * pp[h]) % MOD
                continue

            i = idx + 1  # number of already placed positions
            new_max = cur_max + a
            if new_max > B:
                new_max = B

            new = [0] * (new_max + 1)
            d = dp
            pp = powp

            # New height 0:
            # - down from h = a without changing minimum
            # - down from h < a, creating a new minimum and shifting previous i heights
            val = 0
            if a <= cur_max:
                val = d[a]

            lim = a - 1
            if lim > cur_max:
                lim = cur_max

            exp = i * a
            for h in range(lim + 1):
                dh = d[h]
                if dh:
                    val += dh * pp[exp]
                exp -= i

            new[0] = val % MOD

            # New height y > 0:
            # - up from y - a
            # - down from y + a
            down_limit = cur_max - a
            for y in range(1, new_max + 1):
                s = 0
                if y >= a:
                    s = d[y - a]
                if y <= down_limit:
                    s += d[y + a]

                if s:
                    if s >= MOD:
                        s -= MOD
                    new[y] = (s * pp[y]) % MOD

            dp = new
            cur_max = new_max

        ans = (ans * (sum(dp) % MOD)) % MOD
        if ans == 0:
            break

    print(ans)

if __name__ == "__main__":
    solve()