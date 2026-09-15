import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    P = list(map(int, data[1:1 + n]))

    pos = [0] * (n + 1)
    for i in range(n):
        pos[P[i]] = i + 1

    # Fenwick tree over original positions
    tree = [0] * (n + 1)

    ans = 0
    for k in range(1, n + 1):
        p = pos[k]
        # count of values < k that lie before position p
        c = 0
        i = p - 1
        while i > 0:
            c += tree[i]
            i -= i & (-i)

        pk = c + 1                 # rank of k among values 1..k
        m = k - pk                 # smaller values to the right
        if m > 0:
            ans += (pk + (k - 1)) * m // 2   # sum of pk..k-1

        # insert position of k
        i = p
        while i <= n:
            tree[i] += 1
            i += i & (-i)

    print(ans)

main()