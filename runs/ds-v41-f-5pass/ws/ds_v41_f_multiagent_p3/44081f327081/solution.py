import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    A = list(map(int, data[2:2 + n]))
    del data

    M = max(A)

    # K == 1: we may choose just A_i, so gcd is A_i itself.
    if k == 1:
        sys.stdout.write('\n'.join(map(str, A)))
        sys.stdout.write('\n')
        return

    # freq[v] = number of array elements equal to v
    freq = [0] * (M + 1)
    for v in A:
        freq[v] += 1

    # primes up to M via sieve of Eratosthenes
    if M >= 2:
        sieve = bytearray([1]) * (M + 1)
        sieve[0] = 0
        sieve[1] = 0
        i = 2
        while i * i <= M:
            if sieve[i]:
                start = i * i
                sieve[start::i] = b'\x00' * (((M - start) // i) + 1)
            i += 1
        primes = [j for j in range(2, M + 1) if sieve[j]]
        del sieve
    else:
        primes = []

    # cnt[d] = number of elements divisible by d, via multiple/superset sum.
    # For each prime p, descending i: cnt[i] += cnt[i*p] builds chains p, p^2, ...
    cnt = freq
    for p in primes:
        lim = M // p
        for i in range(lim, 0, -1):
            cnt[i] += cnt[i * p]

    # eligible divisor d -> value d, else 0
    for d in range(1, M + 1):
        cnt[d] = d if cnt[d] >= k else 0

    # max-over-divisors transform: for each prime p, ascending i:
    # cnt[i*p] = max(cnt[i*p], cnt[i])  => cnt[x] = largest eligible divisor of x
    for p in primes:
        lim = M // p
        for i in range(1, lim + 1):
            j = i * p
            a = cnt[i]
            if a > cnt[j]:
                cnt[j] = a

    sys.stdout.write('\n'.join(str(cnt[v]) for v in A))
    sys.stdout.write('\n')


main()