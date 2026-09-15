import sys
import numpy as np


def main():
    data = sys.stdin.buffer.read().split()
    vals = list(map(int, data))
    idx = 0
    N = vals[idx]; idx += 1
    A = np.array(vals[idx:idx + N], dtype=np.int64); idx += N
    B = np.array(vals[idx:idx + N], dtype=np.int64); idx += N
    K = vals[idx]; idx += 1
    flat = vals[idx:idx + 2 * K]
    Xs = np.array(flat[0::2], dtype=np.int64)
    Ys = np.array(flat[1::2], dtype=np.int64)

    ans = np.zeros(K, dtype=np.int64)

    distinctY = np.unique(Ys)
    yidx_map = {int(y): i for i, y in enumerate(distinctY)}
    yidx = np.array([yidx_map[int(y)] for y in Ys], dtype=np.int64)
    dys_idx = (distinctY - 1).astype(np.int64)

    # block size (balanced between full-block numpy work and partial Fenwick work)
    S = int(N * (0.28 / max(1, K)) ** 0.5)
    S = max(1, min(N, S))

    P = Xs // S
    maxP = int(P.max()) if K > 0 else 0

    order = np.argsort(P, kind='stable')
    Psorted = P[order]
    ptr = 0
    C = np.zeros(len(distinctY), dtype=np.int64)

    for b in range(maxP + 1):
        start = ptr
        while ptr < K and Psorted[ptr] == b:
            ptr += 1
        if ptr > start:
            qids = order[start:ptr]
            ans[qids] = C[yidx[qids]]
        if b < maxP:
            l = b * S
            block = np.sort(A[l:l + S])
            ps = np.empty(S + 1, dtype=np.int64)
            ps[0] = 0
            np.cumsum(block, out=ps[1:])
            total = int(ps[S])
            k = np.searchsorted(block, B, side='right')
            w = B * k - ps[k] + (total - ps[k]) - B * (S - k)
            cum = np.cumsum(w)
            C += cum[dys_idx]

    # ---- partial suffix handling ----
    uniqueB = np.unique(B)
    m = len(uniqueB)
    rankA = np.searchsorted(uniqueB, A, side='right').astype(np.int64)
    prefB = np.empty(N + 1, dtype=np.int64)
    prefB[0] = 0
    np.cumsum(B, out=prefB[1:])

    posB = (np.searchsorted(uniqueB, B, side='left') + 1).astype(np.int64)
    upd_nodes_list = []
    upd_vals_list = []
    upd_start = np.zeros(N + 1, dtype=np.int64)
    for j in range(N):
        p = int(posB[j])
        v = int(B[j])
        while p <= m:
            upd_nodes_list.append(p)
            upd_vals_list.append(v)
            p += p & (-p)
        upd_start[j + 1] = len(upd_nodes_list)
    upd_nodes = np.array(upd_nodes_list, dtype=np.int64)
    upd_vals = np.array(upd_vals_list, dtype=np.int64)

    start_q = (Xs // S) * S
    lens = Xs - start_q

    bitc = np.zeros(m + 1, dtype=np.int64)
    bits = np.zeros(m + 1, dtype=np.int64)
    bitlen = m.bit_length() + 1

    qorder = np.argsort(Ys, kind='stable')
    cur = 0
    i = 0
    CHUNK = 1 << 20
    while i < K:
        q = int(qorder[i])
        Y = int(Ys[q])
        if cur < Y:
            a0 = upd_start[cur]
            a1 = upd_start[Y]
            np.add.at(bitc, upd_nodes[a0:a1], 1)
            np.add.at(bits, upd_nodes[a0:a1], upd_vals[a0:a1])
            cur = Y
        j = i
        while j < K and int(Ys[int(qorder[j])]) == Y:
            j += 1
        gq = [int(x) for x in qorder[i:j]]
        i = j
        SY = int(prefB[Y])
        pos = 0
        while pos < len(gq):
            idx_list = []
            seg_q = []
            seg_len = []
            cnt = 0
            while pos < len(gq) and cnt < CHUNK:
                qq = gq[pos]
                l = int(lens[qq])
                if l > 0:
                    s0 = int(start_q[qq])
                    idx_list.append(np.arange(s0, s0 + l, dtype=np.int64))
                    seg_q.append(qq)
                    seg_len.append(l)
                    cnt += l
                pos += 1
            if not idx_list:
                continue
            idxs = np.concatenate(idx_list)
            aa = A[idxs]
            rr = rankA[idxs].copy()
            c = np.zeros(rr.shape, dtype=np.int64)
            s = np.zeros(rr.shape, dtype=np.int64)
            for _ in range(bitlen):
                c += bitc[rr]
                s += bits[rr]
                rr -= rr & (-rr)
            h = 2 * aa * c - 2 * s + SY - aa * Y
            offsets = np.cumsum([0] + seg_len[:-1]).astype(np.int64)
            sums = np.add.reduceat(h, offsets)
            ans[seg_q] += sums

    sys.stdout.write('\n'.join(map(str, ans.tolist())))
    sys.stdout.write('\n')


main()