import sys
import math

def main():
    LIM = 10**6

    try:
        import numpy as np
        # prime sieve
        is_comp = np.zeros(LIM + 1, dtype=bool)
        is_comp[0:2] = True
        for i in range(2, int(LIM**0.5) + 1):
            if not is_comp[i]:
                is_comp[i*i::i] = True
        primes = np.nonzero(~is_comp)[0]

        omega = np.zeros(LIM + 1, dtype=np.uint8)
        for p in primes.tolist():
            omega[p::p] += 1

        idx = np.where(omega == 2, np.arange(LIM + 1, dtype=np.int64), 0)
        best = np.maximum.accumulate(idx).tolist()
    except ImportError:
        omega = bytearray(LIM + 1)
        for p in range(2, LIM + 1):
            if omega[p] == 0:
                for j in range(p, LIM + 1, p):
                    omega[j] += 1
        best = [0] * (LIM + 1)
        cur = 0
        for m in range(LIM + 1):
            if omega[m] == 2:
                cur = m
            best[m] = cur

    data = sys.stdin.buffer.read().split()
    q = int(data[0])
    isqrt = math.isqrt
    out = []
    for i in range(1, q + 1):
        a = int(data[i])
        x = isqrt(a)
        v = best[x]
        out.append(v * v)
    sys.stdout.write('\n'.join(map(str, out)) + '\n')

main()