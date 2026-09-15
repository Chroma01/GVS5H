import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    a = list(map(int, data[2:2 + n]))

    # Fenwick tree over values 0..m-1 to compute inv0 (inversions of A)
    size = m
    tree = [0] * (size + 1)

    def upd(i):
        i += 1
        while i <= size:
            tree[i] += 1
            i += i & (-i)

    def qry(i):  # count of inserted values <= i
        i += 1
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & (-i)
        return s

    inv0 = 0
    for j in range(n):
        v = a[j]
        inv0 += j - qry(v)   # previously inserted values strictly greater than v
        upd(v)

    # Group positions by value
    by_val = [[] for _ in range(m)]
    for p, v in enumerate(a):
        by_val[v].append(p)

    ans = [0] * m
    active = 0
    neg = 0
    for L in range(m):
        for p in by_val[L]:
            neg += p - active
            active += 1
        k = m - 1 - L
        ans[k] = inv0 + active * (n - active) - 2 * neg

    sys.stdout.write('\n'.join(map(str, ans)) + '\n')

main()