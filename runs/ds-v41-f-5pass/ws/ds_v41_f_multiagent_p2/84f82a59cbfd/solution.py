import sys
import math

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    Q = int(data[0])
    queries = data[1:1 + Q]
    MAX = 10 ** 6

    # omega[i] = number of distinct prime factors of i
    omega = [0] * (MAX + 1)
    for i in range(2, MAX + 1):
        if omega[i] == 0:          # i is prime
            for j in range(i, MAX + 1, i):
                omega[j] += 1

    # pref[i] = largest M <= i with omega[M] == 2
    pref = [0] * (MAX + 1)
    last = 0
    for i in range(1, MAX + 1):
        if omega[i] == 2:
            last = i
        pref[i] = last

    out = []
    append = out.append
    isqrt = math.isqrt
    for q in queries:
        m = isqrt(int(q))
        v = pref[m]
        append(str(v * v))

    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == '__main__':
    main()