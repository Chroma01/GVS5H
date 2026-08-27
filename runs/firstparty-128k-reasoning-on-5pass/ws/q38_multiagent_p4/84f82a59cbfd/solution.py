import sys
from math import isqrt

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    q = int(data[0])
    MAX = 1_000_000

    # cnt[x] = number of distinct prime factors of x
    cnt = bytearray(MAX + 1)
    for p in range(2, MAX + 1):
        if cnt[p] == 0:  # p is prime
            for j in range(p, MAX + 1, p):
                cnt[j] += 1

    # best[i] = largest j <= i such that cnt[j] == 2
    best = [0] * (MAX + 1)
    last = 0
    for i in range(1, MAX + 1):
        if cnt[i] == 2:
            last = i
        best[i] = last

    out = []
    append = out.append
    b = best

    for token in data[1:1 + q]:
        a = int(token)
        m = isqrt(a)
        r = b[m]
        append(str(r * r))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()