import sys
import math

def main():
    data = sys.stdin.buffer.read().split()
    q = int(data[0])
    queries = data[1:1 + q]

    LIMIT = 10 ** 6

    # omega[n] = number of distinct prime factors of n
    omega = [0] * (LIMIT + 1)
    for i in range(2, LIMIT + 1):
        if omega[i] == 0:  # i is prime
            for j in range(i, LIMIT + 1, i):
                omega[j] += 1

    # prev_valid[i] = largest s <= i with exactly 2 distinct prime factors
    prev_valid = [0] * (LIMIT + 1)
    last = 0
    for i in range(1, LIMIT + 1):
        if omega[i] == 2:
            last = i
        prev_valid[i] = last

    out = []
    for tok in queries:
        a = int(tok)
        s = math.isqrt(a)
        s = prev_valid[s]
        out.append(str(s * s))

    sys.stdout.write("\n".join(out) + "\n")

main()