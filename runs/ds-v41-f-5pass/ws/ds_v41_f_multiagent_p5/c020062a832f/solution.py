import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    a = list(map(int, data[2:2 + n]))

    count = [0] * m
    sum_pos = [0] * m
    for i, x in enumerate(a):
        count[x] += 1
        sum_pos[x] += i

    # Fenwick tree over values (1-indexed, value v -> index v+1)
    tree = [0] * (m + 1)

    def add(idx, val):
        while idx <= m:
            tree[idx] += val
            idx += idx & (-idx)

    def query(idx):
        s = 0
        while idx > 0:
            s += tree[idx]
            idx -= idx & (-idx)
        return s

    inv = 0
    for i, x in enumerate(a):
        # inserted elements <= x -> query(x+1); those > x are inversions
        leq = query(x + 1)
        inv += i - leq
        add(x + 1, 1)

    out = [0] * m
    out[0] = inv
    cur = inv
    for k in range(m - 1):
        v = m - 1 - k
        cur += 2 * sum_pos[v] - count[v] * (n - 1)
        out[k + 1] = cur

    sys.stdout.write('\n'.join(map(str, out)) + '\n')

main()