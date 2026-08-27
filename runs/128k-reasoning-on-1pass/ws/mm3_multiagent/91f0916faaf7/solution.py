import sys

def solve():
    import sys
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N - 1)]
    MOD = 998244353

    # trivial case: N = 1 (though constraints say N >= 2)
    if N == 1:
        print(1)
        return

    maxA = max(A) if A else 0
    # smallest prime factor sieve up to maxA (or 1)
    spf = list(range(maxA + 1))
    for i in range(2, int(maxA ** 0.5) + 1):
        if spf[i] == i:
            step = i
            start = i * i
            for j in range(start, maxA + 1, step):
                if spf[j] == j:
                    spf[j] = i

    # factorize each A_i, store list of (prime, exponent)
    factors = []  # factors[i] = list of (p, cnt) for A_i
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

    ans = 1
    # process each prime independently
    for p in sorted(primes_set):
        # build exponent list e[i] = v_p(A_i)
        e = [0] * (N - 1)
        for i in range(N - 1):
            for pp, cnt in factors[i]:
                if pp == p:
                    e[i] = cnt
                    break

        total_sum = sum(e)
        # precompute p^k mod MOD for k = 0..total_sum
        pow_p = [1] * (total_sum + 1)
        p_mod = p % MOD
        for k in range(1, total_sum + 1):
            pow_p[k] = (pow_p[k - 1] * p_mod) % MOD

        # dp0[x] = weight of sequences of length i ending at exponent x, zero not visited yet
        # dp1[x] = weight of sequences of length i ending at exponent x, zero visited at least once
        dp0 = [0] * (total_sum + 1)
        dp1 = [0] * (total_sum + 1)
        dp1[0] = 1
        for x in range(1, total_sum + 1):
            dp0[x] = pow_p[x]

        # process each step i = 1 .. N-1
        for step in range(N - 1):
            a = e[step]
            new_dp0 = [0] * (total_sum + 1)
            new_dp1 = [0] * (total_sum + 1)
            if a == 0:
                # stay at the same exponent
                for x in range(total_sum + 1):
                    val0 = dp0[x]
                    val1 = dp1[x]
                    if val0 == 0 and val1 == 0:
                        continue
                    w = pow_p[x]  # multiply by p^x for the new element
                    if x == 0:
                        add = (val0 + val1) % MOD
                        new_dp1[0] = (new_dp1[0] + add * w) % MOD
                    else:
                        new_dp0[x] = (new_dp0[x] + val0 * w) % MOD
                        new_dp1[x] = (new_dp1[x] + val1 * w) % MOD
            else:
                a_val = a
                for x in range(total_sum + 1):
                    val0 = dp0[x]
                    val1 = dp1[x]
                    if val0 == 0 and val1 == 0:
                        continue
                    # move up
                    y_up = x + a_val
                    if y_up <= total_sum:
                        w = pow_p[y_up]
                        new_dp0[y_up] = (new_dp0[y_up] + val0 * w) % MOD
                        new_dp1[y_up] = (new_dp1[y_up] + val1 * w) % MOD
                    # move down
                    if x >= a_val:
                        y_down = x - a_val
                        w = pow_p[y_down]
                        if y_down == 0:
                            add = (val0 + val1) % MOD
                            new_dp1[0] = (new_dp1[0] + add * w) % MOD
                        else:
                            new_dp0[y_down] = (new_dp0[y_down] + val0 * w) % MOD
                            new_dp1[y_down] = (new_dp1[y_down] + val1 * w) % MOD
            dp0, dp1 = new_dp0, new_dp1

        sum_p = sum(dp1) % MOD
        ans = (ans * sum_p) % MOD

    print(ans)


if __name__ == "__main__":
    solve()