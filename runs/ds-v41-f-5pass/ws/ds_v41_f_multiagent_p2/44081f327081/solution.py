import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(x) for x in it]
    del data

    if K == 1:
        sys.stdout.write('\n'.join(map(str, A)))
        return

    M = max(A)
    cnt = [0] * (M + 1)
    for a in A:
        cnt[a] += 1

    # Sieve primes up to M
    is_prime = bytearray([1]) * (M + 1)
    is_prime[0] = 0
    if M >= 1:
        is_prime[1] = 0
    i = 2
    while i * i <= M:
        if is_prime[i]:
            start = i * i
            step = i
            count = (M - start) // step + 1
            is_prime[start::step] = bytearray(count)
        i += 1
    primes = [i for i in range(2, M + 1) if is_prime[i]]
    del is_prime

    # cnt[d] = number of elements divisible by d (multiple zeta transform)
    for p in primes:
        mp = M // p
        dp = mp * p
        for d in range(mp, 0, -1):
            cnt[d] += cnt[dp]
            dp -= p

    # f[d] = d if cnt[d] >= K else 0
    for d in range(1, M + 1):
        if cnt[d] >= K:
            cnt[d] = d
        else:
            cnt[d] = 0

    # max over divisors transform
    for p in primes:
        mp = M // p
        xp = p
        for x in range(1, mp + 1):
            v = cnt[x]
            if v and v > cnt[xp]:
                cnt[xp] = v
            xp += p

    out = '\n'.join([str(cnt[a]) for a in A])
    sys.stdout.write(out)

if __name__ == '__main__':
    main()