import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    a = list(map(int, data[2:2 + n]))

    # Base inversion count (k = 0) via Fenwick tree over values [0, m)
    bit = [0] * (m + 1)

    def bit_add(i, v):
        i += 1
        while i <= m:
            bit[i] += v
            i += i & -i

    def bit_sum(i):  # sum over [0, i]
        i += 1
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s

    base_inv = 0
    tot = [0] * m
    for idx, v in enumerate(a):
        # previous elements greater than v
        base_inv += idx - bit_sum(v)
        bit_add(v, 1)
        tot[v] += 1

    # Difference array over k in [0, m-1]; index m used as sentinel (A_i = 0 -> M - A_i = M)
    diff = [0] * (m + 1)
    seen = [0] * m
    for t, v in enumerate(a):  # t is 0-based; 1-based position = t + 1
        pre = seen[v]                 # occurrences of v before t
        post = tot[v] - pre - 1       # occurrences of v after t
        # pairs where this element is the right endpoint with different value: t - pre
        # pairs where this element is the left endpoint with different value: (n - t - 1) - post
        diff[m - v] += (t - pre) - ((n - t - 1) - post)
        seen[v] += 1

    out = []
    cur = 0
    for k in range(m):
        cur += diff[k]
        out.append(str(base_inv + cur))
    sys.stdout.write("\n".join(out) + "\n")

main()