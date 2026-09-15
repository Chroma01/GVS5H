import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    p = 0
    n = data[p]; p += 1
    Ls = [0] * n
    Rs = [0] * n
    maxR = 0
    for i in range(n):
        l = data[p]; r = data[p + 1]; p += 2
        Ls[i] = l
        Rs[i] = r
        if r > maxR:
            maxR = r
    q = data[p]; p += 1
    qs = data[p:p + q]
    maxX = max(qs)

    # M must be large enough: >= max query + N and >= maxR + 2
    M = max(maxR, maxX) + n + 5

    # Fenwick tree with all counts = 1 (value v has count 1, v in 1..M)
    tree = [0] * (M + 1)
    for i in range(1, M + 1):
        tree[i] = i & (-i)
    cnt = [1] * (M + 1)
    cnt[0] = 0

    top = 1 << (M.bit_length() - 1)
    tr = tree

    # Process contests backwards on the multiset
    for i in range(n - 1, -1, -1):
        # a = value at position L (kth smallest, L-th)
        k = Ls[i]
        idx = 0
        bit = top
        while bit:
            nxt = idx + bit
            if nxt <= M and tr[nxt] < k:
                idx = nxt
                k -= tr[nxt]
            bit >>= 1
        a = idx + 1

        # b = value at position R+1 in current multiset
        # (after deleting position L <= R, it becomes position R)
        k = Rs[i] + 1
        idx = 0
        bit = top
        while bit:
            nxt = idx + bit
            if nxt <= M and tr[nxt] < k:
                idx = nxt
                k -= tr[nxt]
            bit >>= 1
        b = idx + 1

        # remove one copy of a
        cnt[a] -= 1
        j = a
        while j <= M:
            tr[j] -= 1
            j += j & (-j)

        # add one copy of b
        cnt[b] += 1
        j = b
        while j <= M:
            tr[j] += 1
            j += j & (-j)

    # Reconstruct the final sorted sequence: position -> value
    vals = []
    ext = vals.extend
    for v in range(1, M + 1):
        c = cnt[v]
        if c:
            ext([v] * c)

    out = [str(vals[x - 1]) for x in qs]
    sys.stdout.write('\n'.join(out) + '\n')

main()