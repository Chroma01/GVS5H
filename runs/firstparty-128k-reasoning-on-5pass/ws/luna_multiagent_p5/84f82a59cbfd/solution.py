import sys
from array import array
from bisect import bisect_right

LIMIT = 1_000_000

# Smallest-prime-factor sieve.
spf = array('I', range(LIMIT + 1))
root = int(LIMIT ** 0.5)
for p in range(2, root + 1):
    if spf[p] == p:
        start = p * p
        for x in range(start, LIMIT + 1, p):
            if spf[x] == x:
                spf[x] = p

# Number of distinct prime factors for each value.
distinct = bytearray(LIMIT + 1)
valid_squares = []

for x in range(2, LIMIT + 1):
    p = spf[x]
    y = x // p
    distinct[x] = distinct[y] + (p != spf[y])
    if distinct[x] == 2:
        valid_squares.append(x * x)

data = list(map(int, sys.stdin.buffer.read().split()))
q = data[0]
queries = data[1:1 + q]

out = []
for a in queries:
    out.append(str(valid_squares[bisect_right(valid_squares, a) - 1]))

sys.stdout.write("\n".join(out))