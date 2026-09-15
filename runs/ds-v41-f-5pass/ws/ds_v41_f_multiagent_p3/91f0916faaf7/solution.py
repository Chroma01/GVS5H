import sys

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N = data[0]
    A = data[1:N]  # length N-1
    L = N - 1

    MAXA = 1000
    spf = list(range(MAXA + 1))
    for i in range(2, int(MAXA ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, MAXA + 1, i):
                if spf[j] == j:
                    spf[j] = i

    # prime -> list d_i = v_p(A_i)
    prime_d = {}
    for idx, a in enumerate(A):
        n = a
        while n > 1:
            p = spf[n]
            c = 0
            while n % p == 0:
                n //= p
                c += 1
            lst = prime_d.get(p)
            if lst is None:
                lst = [0] * L
                prime_d[p] = lst
            lst[idx] += c

    ans = 1

    for p, dlist in prime_d.items():
        S = sum(dlist)

        powp = [1] * (S + 1)
        for h in range(1, S + 1):
            powp[h] = powp[h - 1] * p % MOD

        # dp0[h]: no zero seen yet
        # dp1[h]: zero already seen
        dp0 = powp[:]
        dp0[0] = 0
        dp1 = [0] * (S + 1)
        dp1[0] = 1

        for d in dlist:
            if d == 0:
                dp0 = [(x * y) % MOD for x, y in zip(dp0, powp)]
                dp1 = [(x * y) % MOD for x, y in zip(dp1, powp)]
            else:
                ndp0 = [0] * (S + 1)
                ndp1 = [0] * (S + 1)

                # h -> h + d
                for h in range(S - d + 1):
                    nh = h + d
                    pw = powp[nh]
                    ndp0[nh] += dp0[h] * pw
                    ndp1[nh] += dp1[h] * pw

                # h -> h - d; h = d gives new height 0
                ndp1[0] += dp0[d] + dp1[d]
                for h in range(d + 1, S + 1):
                    nh = h - d
                    pw = powp[nh]
                    ndp0[nh] += dp0[h] * pw
                    ndp1[nh] += dp1[h] * pw

                dp0 = [x % MOD for x in ndp0]
                dp1 = [x % MOD for x in ndp1]

        ans = ans * (sum(dp1) % MOD) % MOD

    print(ans)

if __name__ == "__main__":
    main()