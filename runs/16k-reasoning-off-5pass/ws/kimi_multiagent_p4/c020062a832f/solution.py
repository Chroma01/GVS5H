import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    A = list(map(int, data[2:2 + n]))

    # Fenwick tree for initial inversion count (k = 0)
    bit = [0] * (m + 1)

    def bit_add(i, v):
        i += 1
        while i <= m:
            bit[i] += v
            i += i & (-i)

    def bit_sum(i):  # sum over [0, i]
        i += 1
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & (-i)
        return s

    inv = 0
    for idx, a in enumerate(A):
        # number of previous elements greater than a
        inv += idx - bit_sum(a)
        bit_add(a, 1)

    cnt = [0] * m
    pos_sum = [0] * m
    for p, a in enumerate(A, start=1):  # 1-indexed positions
        cnt[a] += 1
        pos_sum[a] += p

    out = []
    cur = inv
    out.append(str(cur))
    for k in range(m - 1):
        v = m - 1 - k  # elements with this value wrap from M-1 to 0
        cur += 2 * pos_sum[v] - cnt[v] * (n + 1)
        out.append(str(cur))

    sys.stdout.write("\n".join(out) + "\n")

main()