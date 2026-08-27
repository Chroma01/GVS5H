import sys
import numpy as np

try:
    from scipy.sparse import csr_matrix
    from scipy.sparse.csgraph import connected_components
    HAVE_SCIPY = True
except Exception:
    HAVE_SCIPY = False

MOD = 998244353


def excl(x):
    """exclusive cumulative sum, int64"""
    x = np.asarray(x, dtype=np.int64)
    n = x.shape[0]
    r = np.zeros(n, dtype=np.int64)
    if n > 1:
        np.cumsum(x[:-1], out=r[1:])
    return r


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    T = int(data[0])
    pos = 1
    Hl = [0] * T
    Wl = [0] * T
    toks = []
    ext = toks.extend
    for t in range(T):
        h = int(data[pos]); w = int(data[pos + 1]); pos += 2
        Hl[t] = h; Wl[t] = w
        ext(data[pos:pos + h])
        pos += h
    blob = b''.join(toks)
    del toks, data

    chars = np.frombuffer(blob, dtype=np.uint8)
    a = (chars == 65).astype(np.int8)   # 1 if 'A'
    del chars
    blob = None

    H = np.array(Hl, dtype=np.int64)
    W = np.array(Wl, dtype=np.int64)
    del Hl, Wl

    N = a.shape[0]
    cells = H * W
    cellstart = excl(cells)
    nodes = H + W
    nodebase = excl(nodes)
    M = int(nodes.sum())
    SH = int(H.sum())
    rowoffset = excl(H)
    Wrep = np.repeat(W, H)          # length SH : width of each global row
    rowstart = excl(Wrep)           # global cell index of start of each row

    # ---- row prefix xor (inclusive) and row parity check ----
    cse = np.zeros(N + 1, dtype=np.int32)
    np.cumsum(a, dtype=np.int32, out=cse[1:])
    base = cse[rowstart]
    P = ((cse[1:] - np.repeat(base, Wrep)) & 1).astype(np.int8)
    rowpar = (cse[rowstart + Wrep] - base) & 1
    bad = np.add.reduceat(rowpar, rowoffset) > 0
    del rowpar, base, cse

    # ---- column prefix xor (inclusive) grouped by equal W ----
    order = np.argsort(W, kind='stable')
    lens = cells[order]
    offs = excl(lens)
    idx = np.arange(N, dtype=np.int64) + np.repeat(cellstart[order] - offs, lens)
    a_sorted = a[idx]
    Q_sorted = np.empty(N, dtype=np.int8)
    Wsorted = W[order]
    if T > 1:
        bounds = np.concatenate((
            np.array([0], dtype=np.int64),
            np.flatnonzero(Wsorted[1:] != Wsorted[:-1]).astype(np.int64) + 1,
            np.array([T], dtype=np.int64)))
    else:
        bounds = np.array([0, T], dtype=np.int64)

    for gi in range(bounds.shape[0] - 1):
        gs = int(bounds[gi]); ge = int(bounds[gi + 1])
        w = int(Wsorted[gs])
        tests = order[gs:ge]
        hs = H[tests]
        s = int(offs[gs])
        e = s + int(lens[gs:ge].sum())
        block = a_sorted[s:e].reshape(-1, w)
        R = block.shape[0]
        off_b = excl(hs)
        CSe = np.zeros((R + 1, w), dtype=np.int32)
        np.cumsum(block, axis=0, dtype=np.int32, out=CSe[1:])
        Qb = (CSe[1:] - CSe[np.repeat(off_b, hs)]) & 1
        badcol = ((CSe[off_b + hs] - CSe[off_b]) & 1).any(axis=1)
        bad[tests] |= badcol
        Q_sorted[s:e] = Qb.reshape(-1)
        del CSe, Qb, block

    Q = np.empty(N, dtype=np.int8)
    Q[idx] = Q_sorted
    del a_sorted, Q_sorted, idx

    # ---- build B-cell edges ----
    maskB = (a == 0)
    u_row = np.repeat(nodebase, H) + (np.arange(SH, dtype=np.int64) - np.repeat(rowoffset, H))
    v_row = np.repeat(nodebase + H, H)
    u = np.repeat(u_row, Wrep)[maskB].astype(np.int32)
    jj = np.arange(N, dtype=np.int64) - np.repeat(rowstart, Wrep)
    v = (np.repeat(v_row, Wrep) + jj)[maskB].astype(np.int32)
    wgt = ((P ^ Q ^ 1) & 1)[maskB].astype(np.int8)
    del maskB, u_row, v_row, jj, P, Q, a, Wrep, rowstart, rowoffset

    m = u.shape[0]
    conflict_test = np.zeros(T, dtype=bool)

    if m == 0:
        counts = nodes.copy()
    elif HAVE_SCIPY:
        n2 = 2 * M
        u2 = u.astype(np.int64) << 1
        v2 = v.astype(np.int64) << 1
        wl = wgt.astype(np.int64)
        U = np.concatenate((u2, u2 + 1)).astype(np.int32)
        V = np.concatenate((v2 + wl, v2 + 1 - wl)).astype(np.int32)
        del u2, v2, wl
        g = csr_matrix((np.ones(U.shape[0], dtype=np.int8), (U, V)), shape=(n2, n2))
        del U, V
        ncomp, labels = connected_components(g, directed=False)
        del g
        conf = labels[0::2] == labels[1::2]
        conflict_test = np.add.reduceat(conf, nodebase) > 0
        tn = np.repeat(np.arange(T, dtype=np.int64), 2 * nodes)
        tl = np.zeros(ncomp, dtype=np.int64)
        tl[labels] = tn
        counts = np.bincount(tl, minlength=T)[:T] // 2
        del tn, tl, labels, conf
    else:
        par = list(range(M))
        rel = bytearray(M)
        sz = [1] * M
        conf_nodes = []
        for x, y, c in zip(u.tolist(), v.tolist(), wgt.tolist()):
            r = x; p = 0
            while par[r] != r:
                p ^= rel[r]; r = par[r]
            if par[x] != r:
                cur = x; cp = p
                while par[cur] != r:
                    nxt = par[cur]; nr = rel[cur]
                    par[cur] = r; rel[cur] = cp
                    cp ^= nr
                    cur = nxt
            rx = r; px = p
            r = y; p = 0
            while par[r] != r:
                p ^= rel[r]; r = par[r]
            if par[y] != r:
                cur = y; cp = p
                while par[cur] != r:
                    nxt = par[cur]; nr = rel[cur]
                    par[cur] = r; rel[cur] = cp
                    cp ^= nr
                    cur = nxt
            ry = r; py = p
            if rx == ry:
                if (px ^ py) != c:
                    conf_nodes.append(rx)
            else:
                w2 = px ^ py ^ c
                if sz[rx] < sz[ry]:
                    rx, ry = ry, rx
                par[ry] = rx
                rel[ry] = w2
                sz[rx] += sz[ry]
        parr = np.array(par, dtype=np.int32)
        isroot = (parr == np.arange(M, dtype=np.int32)).astype(np.int32)
        counts = np.add.reduceat(isroot, nodebase)
        if conf_nodes:
            ct = np.searchsorted(nodebase, np.array(conf_nodes, dtype=np.int64), side='right') - 1
            conflict_test[ct] = True
        del par, rel, sz, parr, isroot

    bad = bad | conflict_test
    counts = counts.astype(np.int64)
    mx = int(counts.max()) if T > 0 else 0

    # 2^c mod p via two small tables (c = 1024*hi + lo)
    K = 1024
    low = [1] * K
    cur = 1
    for i in range(1, K):
        cur = cur * 2 % MOD
        low[i] = cur
    nb = mx // K + 2
    step = pow(2, K, MOD)
    high = [1] * nb
    cur = 1
    for j in range(1, nb):
        cur = cur * step % MOD
        high[j] = cur
    lowa = np.array(low, dtype=np.int64)
    higha = np.array(high, dtype=np.int64)
    ans = lowa[counts & (K - 1)] * higha[counts >> 10] % MOD
    ans[bad] = 0
    out = '\n'.join(map(str, ans.tolist()))
    sys.stdout.write(out)
    sys.stdout.write('\n')


main()