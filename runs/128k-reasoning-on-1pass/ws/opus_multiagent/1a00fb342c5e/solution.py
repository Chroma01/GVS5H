import sys
import numpy as np


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])

    if M > 0:
        vals = np.array(list(map(int, data[2:2 + 3 * M])), dtype=np.int64)
        vals = vals.reshape(M, 3)
        X = vals[:, 0] - 1
        Y = vals[:, 1] - 1
        Z = vals[:, 2]
    else:
        X = np.zeros(0, dtype=np.int64)
        Y = np.zeros(0, dtype=np.int64)
        Z = np.zeros(0, dtype=np.int64)

    # Build CSR adjacency (both directions)
    if M > 0:
        src = np.concatenate([X, Y])
        dst = np.concatenate([Y, X])
        wt = np.concatenate([Z, Z])
        order = np.argsort(src, kind='stable')
        adj = dst[order]
        wadj = wt[order]
        deg = np.bincount(src, minlength=N)
    else:
        adj = np.zeros(0, dtype=np.int64)
        wadj = np.zeros(0, dtype=np.int64)
        deg = np.zeros(N, dtype=np.int64)

    start = np.zeros(N + 1, dtype=np.int64)
    np.cumsum(deg, out=start[1:])

    adj_l = adj.tolist()
    w_l = wadj.tolist()
    st_l = start.tolist()

    d = [0] * N
    comp = [-1] * N
    k = 0

    for s in range(N):
        if comp[s] < 0:
            comp[s] = k
            d[s] = 0
            stack = [s]
            while stack:
                u = stack.pop()
                du = d[u]
                for i in range(st_l[u], st_l[u + 1]):
                    v = adj_l[i]
                    if comp[v] < 0:
                        comp[v] = k
                        d[v] = du ^ w_l[i]
                        stack.append(v)
            k += 1

    dnp = np.array(d, dtype=np.int64)
    compnp = np.array(comp, dtype=np.int64)

    if M > 0:
        if np.any((dnp[X] ^ dnp[Y]) != Z):
            sys.stdout.write("-1\n")
            return

    sizes = np.bincount(compnp, minlength=k).astype(np.int64)
    r = np.zeros(k, dtype=np.int64)
    for b in range(30):
        ones = ((dnp >> b) & 1).astype(np.float64)
        c = np.bincount(compnp, weights=ones, minlength=k)
        flip = (2.0 * c > sizes.astype(np.float64))
        r += flip.astype(np.int64) << b

    A = dnp ^ r[compnp]
    sys.stdout.write(' '.join(map(str, A.tolist())))
    sys.stdout.write('\n')


main()