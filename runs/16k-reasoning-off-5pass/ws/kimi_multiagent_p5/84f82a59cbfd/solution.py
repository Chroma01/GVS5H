import sys
import math

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    q = int(data[0])
    queries = data[1:1 + q]

    LIMIT = 10**6

    # Smallest prime factor sieve
    spf = list(range(LIMIT + 1))
    for i in range(2, int(LIMIT ** 0.5) + 1):
        if spf[i] == i:  # i is prime
            step = i
            start = i * i
            for j in range(start, LIMIT + 1, step):
                if spf[j] == j:
                    spf[j] = i

    # omega[m] = number of distinct prime factors of m
    omega = [0] * (LIMIT + 1)
    for m in range(2, LIMIT + 1):
        p = spf[m]
        r = m // p
        # add 1 only if p does not divide the remaining part
        omega[m] = omega[r] + (1 if spf[r] != p else 0)

    # prev[m] = largest index <= m with exactly two distinct prime factors
    prev = [0] * (LIMIT + 1)
    last = 0
    for m in range(1, LIMIT + 1):
        if omega[m] == 2:
            last = m
        prev[m] = last

    out = []
    for tok in queries:
        a = int(tok)
        m = math.isqrt(a)
        v = prev[m]
        out.append(str(v * v))
    sys.stdout.write("\n".join(out) + "\n")

main()