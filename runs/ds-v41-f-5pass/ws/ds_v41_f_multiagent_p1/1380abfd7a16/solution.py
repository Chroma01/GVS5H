import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    P = data[1:1 + n]

    # Fenwick tree over N slots, all initially empty (value 1).
    # tree[i] = i & -i is the O(N) build of an all-ones array.
    tree = [0] * (n + 1)
    for i in range(1, n + 1):
        tree[i] = i & (-i)

    # highest power of two <= n
    LOG = 1
    while (LOG << 1) <= n:
        LOG <<= 1

    ans = [0] * (n + 1)

    # Process values from N down to 1. Value i goes into the P_i-th
    # still-empty slot, since values i+1..N are already fixed and the
    # empty slots are exactly the positions of values 1..i.
    for i in range(n, 0, -1):
        k = int(P[i - 1])
        pos = 0
        rem = k
        bit = LOG
        while bit:
            nxt = pos + bit
            if nxt <= n and tree[nxt] < rem:
                pos = nxt
                rem -= tree[nxt]
            bit >>= 1
        p = pos + 1          # smallest index with prefix sum >= k
        ans[p] = i
        # mark slot p as occupied
        j = p
        while j <= n:
            tree[j] -= 1
            j += j & (-j)

    sys.stdout.write(' '.join(map(str, ans[1:])))
    sys.stdout.write('\n')

main()