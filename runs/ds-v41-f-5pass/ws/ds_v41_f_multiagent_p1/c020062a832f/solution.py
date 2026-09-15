import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    A = [int(x) for x in data[2:2 + n]]

    cnt = [0] * m
    sumIdx = [0] * m       # sum of 0-based indices of occurrences of each value
    sumAfter = [0] * m     # sum of (n-1-i) over occurrences of each value
    nm1 = n - 1
    for i in range(n):
        a = A[i]
        cnt[a] += 1
        sumIdx[a] += i
        sumAfter[a] += nm1 - i

    # pairs with equal values (never inversions)
    E = 0
    for v in range(m):
        c = cnt[v]
        if c > 1:
            E += c * (c - 1) // 2

    # invStrict = #{(i<j): pos_i > pos_j}, pos_x = (M - x) % M
    # via a Fenwick tree over values 0..m-1
    tree = [0] * (m + 1)
    invStrict = 0
    inserted = 0
    for i in range(n):
        a = A[i]
        p = (m - a) % m
        # count already-inserted pos <= p
        idx = p + 1
        s = 0
        while idx > 0:
            s += tree[idx]
            idx -= idx & (-idx)
        invStrict += inserted - s
        # insert p
        idx = p + 1
        while idx <= m:
            tree[idx] += 1
            idx += idx & (-idx)
        inserted += 1

    # circular pairs count
    W = n * (n - 1) // 2 - E - invStrict

    # difference array over k
    D = [0] * m
    for v in range(m):
        if cnt[v]:
            p = (m - v) % m
            D[p] += sumIdx[v] - sumAfter[v]
    D[0] += W

    out = []
    cur = 0
    for k in range(m):
        cur += D[k]
        out.append(cur)

    sys.stdout.write('\n'.join(map(str, out)) + '\n')

main()