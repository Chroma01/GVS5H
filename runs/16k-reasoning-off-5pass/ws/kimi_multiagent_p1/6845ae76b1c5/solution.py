import sys
from collections import defaultdict


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    A = [int(x) for x in data[pos:pos + N]]; pos += N
    B = [int(x) for x in data[pos:pos + N]]; pos += N
    K = int(data[pos]); pos += 1
    X = [0] * K
    Y = [0] * K
    for k in range(K):
        X[k] = int(data[pos]); Y[k] = int(data[pos + 1]); pos += 2

    # ---------- coordinate compression of B values ----------
    vals = sorted(set(B))
    comp = {v: i for i, v in enumerate(vals)}
    V = len(vals)
    Bc = [comp[b] + 1 for b in B]  # 1-indexed Fenwick positions

    # ---------- sqrt decomposition on A index ----------
    BA = 1000
    nb = (N + BA - 1) // BA

    # ---------- collect remainder requests ----------
    # For query k with p = X_k // BA:
    #   ans = PH[p, Y_k] + sum_{i in [p*BA, X_k)} g(A[i], Y_k)
    # where g(a, y) = sum_{j<=y} |a - B_j|.
    req_a = []
    req_y = []
    req_k = []
    for k in range(K):
        x = X[k]
        y = Y[k]
        p = x // BA
        start = p * BA
        if start < x:
            seg = A[start:x]
            r = x - start
            req_a.extend(seg)
            req_y.extend([y] * r)
            req_k.extend([k] * r)
    rem_cnt = len(req_a)

    # ---------- group requests by y ----------
    by_y = defaultdict(list)
    for t in range(rem_cnt):
        by_y[req_y[t]].append(t)

    # ---------- offline sweep over Y with Fenwick over B values ----------
    # Fenwick stores count and sum of B_1..B_y (by compressed value).
    # g(a, y) = a*cnt_le(a) - sum_le(a) + (tot_sum - sum_le(a)) - a*(y - cnt_le(a))
    bitc = [0] * (V + 1)
    bits = [0] * (V + 1)
    agg = [0] * K

    ycur = 0
    ts = 0  # running total sum of inserted B values
    for y in sorted(by_y.keys()):
        while ycur < y:
            c = Bc[ycur]
            v = B[ycur]
            ts += v
            while c <= V:
                bitc[c] += 1
                bits[c] += v
                c += c & -c
            ycur += 1
        for t in by_y[y]:
            a = req_a[t]
            # binary search: largest compressed index with vals[idx] <= a
            lo, hi = 0, V - 1
            idx = -1
            while lo <= hi:
                mid = (lo + hi) // 2
                if vals[mid] <= a:
                    idx = mid
                    lo = mid + 1
                else:
                    hi = mid - 1
            c_le = 0
            s_le = 0
            if idx >= 0:
                c = idx + 1
                while c > 0:
                    c_le += bitc[c]
                    s_le += bits[c]
                    c -= c & -c
            agg[req_k[t]] += a * c_le - s_le + (ts - s_le) - a * (y - c_le)

    # ---------- numpy table for block-boundary prefixes ----------
    try:
        import numpy as np
        A_arr = np.array(A, dtype=np.int64)
        B_arr = np.array(B, dtype=np.int64)
        H = np.zeros((nb + 1, N), dtype=np.int64)
        for p in range(nb):
            seg = np.sort(A_arr[p * BA:(p + 1) * BA])
            ps = np.concatenate(([0], np.cumsum(seg)))
            m = len(seg)
            c = np.searchsorted(seg, B_arr)
            ps_c = ps[c]
            H[p + 1] = H[p] + (B_arr * c - ps_c + (ps[m] - ps_c) - B_arr * (m - c))
        PH = np.concatenate(
            (np.zeros((nb + 1, 1), dtype=np.int64), np.cumsum(H, axis=1)), axis=1)
        use_numpy = True
    except ImportError:
        use_numpy = False

    out = []
    for k in range(K):
        x = X[k]
        y = Y[k]
        p = x // BA
        if use_numpy:
            ans = int(PH[p, y])
        else:
            ans = 0
            for i in range(p * BA):
                ai = A[i]
                for j in range(y):
                    ans += abs(ai - B[j])
        ans += agg[k]
        out.append(ans)

    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()