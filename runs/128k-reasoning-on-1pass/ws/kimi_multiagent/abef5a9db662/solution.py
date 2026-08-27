import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    p = 0
    N = data[p]; p += 1
    L = [0] * N
    R = [0] * N
    for i in range(N):
        L[i] = data[p]
        R[i] = data[p + 1]
        p += 2
    Q = data[p]; p += 1
    queries = data[p:p + Q]

    # Only initial ratings that are actually queried matter.
    n = max(queries)
    size = n + 2
    tree = [0] * (size + 1)   # BIT over the difference array of add[]
    diff = [0] * (size + 1)   # plain difference array for final materialization
    hb = 1 << (n.bit_length() - 1)

    def lower_bound(tgt):
        # Smallest x in [1, n+1] with g(x) = x + add[x] >= tgt.
        # Binary lifting on the BIT: acc always equals add[pos] (prefix sum
        # of the diff array up to pos), so g(nx) = nx + acc + tree[nx].
        pos = 0
        acc = 0
        k = hb
        t = tree
        while k:
            nx = pos + k
            if nx <= n:
                tv = t[nx]
                if nx + acc + tv < tgt:
                    pos = nx
                    acc += tv
            k >>= 1
        return pos + 1

    tr = tree
    for i in range(N):
        l = lower_bound(L[i])              # first x with g(x) >= L_i
        r = lower_bound(R[i] + 1) - 1      # last  x with g(x) <= R_i
        if l <= r:
            diff[l] += 1
            diff[r + 1] -= 1
            j = l
            while j <= size:
                tr[j] += 1
                j += j & -j
            j = r + 1
            while j <= size:
                tr[j] -= 1
                j += j & -j

    # Materialize add[x] for all x in O(n).
    add = [0] * (n + 1)
    s = 0
    for x in range(1, n + 1):
        s += diff[x]
        add[x] = s

    out = [str(x + add[x]) for x in queries]
    sys.stdout.write('\n'.join(out) + '\n')


main()