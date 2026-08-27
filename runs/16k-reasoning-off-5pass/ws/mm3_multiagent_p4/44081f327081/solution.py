import sys
import threading

def main():
    import sys
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    MAXV = 10**6

    # frequency of each value
    freq = [0] * (MAXV + 1)
    for x in A:
        freq[x] += 1

    # precompute smallest prime factor up to MAXV
    spf = [0] * (MAXV + 1)
    for i in range(2, MAXV + 1):
        if spf[i] == 0:
            spf[i] = i
            if i * i <= MAXV:
                step = i
                start = i * i
                for j in range(start, MAXV + 1, step):
                    if spf[j] == 0:
                        spf[j] = i
    # fill spf for primes > sqrt(MAXV) and for 1 (set to 1)
    for i in range(2, MAXV + 1):
        if spf[i] == 0:
            spf[i] = i
    spf[1] = 1

    # function to get divisors of a number using spf
    def get_divisors(x):
        # factorize
        factors = []
        while x > 1:
            p = spf[x]
            e = 0
            while x % p == 0:
                x //= p
                e += 1
            factors.append((p, e))
        # generate divisors iteratively
        divs = [1]
        for p, e in factors:
            cur_len = len(divs)
            mul = 1
            for _ in range(e):
                mul *= p
                for i in range(cur_len):
                    divs.append(divs[i] * mul)
        return divs

    # Compute cnt[d] = number of elements divisible by d
    # We do an inverse sieve: for each value v that appears, add freq[v] to cnt[d] for all d dividing v
    cnt = [0] * (MAXV + 1)
    # iterate over all possible values
    for v in range(1, MAXV + 1):
        f = freq[v]
        if f == 0:
            continue
        # get all divisors of v
        divs = get_divisors(v)
        for d in divs:
            cnt[d] += f

    # Now answer each query
    out = []
    append = out.append
    for a in A:
        best = 1
        # enumerate divisors of a
        divs = get_divisors(a)
        for d in divs:
            if cnt[d] >= K and d > best:
                best = d
        append(str(best))
    sys.stdout.write('\n'.join(out))

threading.Thread(target=main).start()