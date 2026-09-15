import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    A = list(map(int, data[2:2 + n]))
    del data

    # K == 1: the only chosen element is A_i itself.
    if k == 1:
        sys.stdout.write('\n'.join(map(str, A)))
        sys.stdout.write('\n')
        return

    M = max(A)

    # K == n: the only K-subset is the whole array -> gcd of all.
    if k == n:
        from math import gcd
        g = 0
        for a in A:
            g = gcd(g, a)
        sys.stdout.write((str(g) + '\n') * n)
        return

    # frequency of each value
    f = [0] * (M + 1)
    for a in A:
        f[a] += 1

    ans = [0] * (M + 1)
    # Ascending d: processing larger divisors later makes the last write
    # for a value its largest feasible divisor.
    for d in range(1, M + 1):
        if sum(f[d::d]) >= k:                 # cnt[d] = number divisible by d
            ans[d::d] = [d] * ((M - d) // d + 1)

    sys.stdout.write('\n'.join(map(str, map(ans.__getitem__, A))))
    sys.stdout.write('\n')


main()