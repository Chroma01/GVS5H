import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    A = list(map(int, data[2:2 + n]))

    cnt = [0] * m
    spos = [0] * m
    for i, v in enumerate(A):
        cnt[v] += 1
        spos[v] += i

    # Fenwick tree over values 0..m-1, compute f(0): traverse right to left,
    # count later elements strictly smaller than A[i].
    bit = [0] * (m + 1)
    inv = 0
    for i in range(n - 1, -1, -1):
        v = A[i]
        # query sum over [0, v-1]
        j = v  # BIT index representing prefix up to v-1 is index v (1-indexed)
        s = 0
        while j > 0:
            s += bit[j]
            j -= j & (-j)
        inv += s
        # update at v -> BIT index v+1
        j = v + 1
        while j <= m:
            bit[j] += 1
            j += j & (-j)

    out = [str(inv)]
    nm1 = n - 1
    for k in range(m - 1):
        x = m - 1 - k
        inv += 2 * spos[x] - cnt[x] * nm1
        out.append(str(inv))

    sys.stdout.write('\n'.join(out) + '\n')

main()