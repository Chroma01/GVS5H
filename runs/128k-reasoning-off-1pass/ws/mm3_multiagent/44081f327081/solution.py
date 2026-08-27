import sys

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    if N == 0:
        return
    maxA = max(A)

    # frequency array
    freq = [0] * (maxA + 1)
    for x in A:
        freq[x] += 1

    # count of numbers divisible by each v
    cnt = [0] * (maxA + 1)
    for v in range(1, maxA + 1):
        s = 0
        step = v
        for m in range(v, maxA + 1, step):
            s += freq[m]
        cnt[v] = s

    # smallest prime factor sieve
    spf = [0] * (maxA + 1)
    for i in range(2, maxA + 1):
        if spf[i] == 0:
            spf[i] = i
            if i * i <= maxA:
                step = i
                start = i * i
                for j in range(start, maxA + 1, step):
                    if spf[j] == 0:
                        spf[j] = i
    spf[1] = 1

    out = []
    append = out.append
    for x in A:
        # factorize x using spf
        factors = []
        while x > 1:
            p = spf[x]
            e = 0
            while x % p == 0:
                x //= p
                e += 1
            factors.append((p, e))
        # generate all divisors
        divisors = [1]
        for p, e in factors:
            cur = []
            pow_p = 1
            for _ in range(e):
                pow_p *= p
                for d in divisors:
                    cur.append(d * pow_p)
            divisors.extend(cur)
        # find max divisor with cnt >= K
        best = 1
        for d in divisors:
            if cnt[d] >= K and d > best:
                best = d
        append(str(best))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()