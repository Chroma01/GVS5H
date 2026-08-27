```python
import sys

def solve():
    import sys
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N - 1)]
    mod = 998244353

    if N - 1 == 0:
        print(1)
        return

    maxA = max(A) if A else 0
    # smallest prime factor sieve
    spf = list(range(maxA + 1))
    for i in range(2, int(maxA ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, maxA + 1, i):
                if spf[j] == j:
                    spf[j] = i

    # factorize each A_i
    factors = []  # list of list of (prime, exponent)
    primes_set = set()
    for a in A:
        fac = []
        x = a
        while x > 1:
            p = spf[x]
            cnt = 0
            while x % p == 0:
                x //= p
                cnt += 1
            fac.append((p, cnt))
            primes_set.add(p)
        factors.append(fac)

    if not primes_set:
        # only possible sequence is all 1s
        print(1)
        return

    ans = 1
    # process each prime independently
    for p in sorted(primes_set):
        # build exponent sequence e[i] = v_p(A_i)
        e = [0] * (N - 1)
        for i in range(N - 1):
            for pp, cnt in factors[i]:
                if pp == p:
                    e[i] = cnt
                    break

        total_sum = sum(e)
        if total_sum == 0:
            # only walk is all zeros, weight 1
            continue

        maxX = total_sum
        # precompute p^k mod mod
        pow_p = [1] * (maxX + 1)
        p_mod = p % mod
        for k in range(1, maxX + 1):
            pow_p[k] = (pow_p[k - 1] * p_mod) % mod

        # dp0[x] = weight of walks ending at x, not visited 0 yet
        # dp1[x] = weight of walks ending at x, visited 0 at least once
        dp0 = [0] * (maxX + 1)
        dp1 = [0] * (maxX + 1)
        dp1[0] = 1
        for x in range(1, maxX + 1):
            dp0[x] = pow_p[x]

        for step in range(N - 1):
            e_step = e[step]
            new_dp0 = [0] * (maxX + 1)
            new_dp1 = [0] * (maxX + 1)
            if e_step == 0:
                # x stays the same
                for x in range(maxX + 1):
                    val0 = dp0[x]
                    val1 = dp1[x]
                    if val0 == 0 and val1 == 0:
                        continue
                    w = pow_p[x]
                    if x == 0:
                        add = (val0 + val1) % mod
                        new_dp1[0] = (new_dp1[0] + add * w) % mod
                    else:
                        new_dp0[x] = (new_dp0[x] + val0 * w) % mod
                        new_dp1[x] = (new_dp1[x] + val1 * w) % mod
            else:
                e_val = e_step
                for x in range(maxX + 1):
                    val0 = dp0[x]
                    val1 = dp1[x]
                    if val0 == 0 and val1 == 0:
                        continue
                    # move up
                    x_up = x + e_val
                    if x_up <= maxX:
                        w = pow_p[x_up]
                        new_dp0[x_up] = (new_dp0[x_up] + val0 * w) % mod
                        new_dp1[x_up] = (new_dp1[x_up] + val1 * w) % mod
                    # move down
                    if x >= e_val:
                        x_down = x - e_val
                        w = pow_p[x_down]
                        if x_down == 0:
                            add = (val0 + val1) % mod
                            new_dp1[0] = (new_dp1[0] + add * w) % mod
                        else:
                            new_dp0[x_down] = (new_dp0[x_down] + val0 * w) % mod
                            new_dp1[x_down] = (new_dp1[x_down] + val1 * w) % mod
            dp0, dp1 = new_dp0, new_dp1

        sum_p = sum(dp1) % mod
        ans = (ans * sum_p) % mod

    print(ans)


if __name__ == "__main__":
    solve()
```