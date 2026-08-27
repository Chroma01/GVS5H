import sys
from itertools import accumulate

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    if n == 0:
        return
    P = [0]
    P.extend(accumulate(A))

    L = [0] * n
    R = [0] * n

    # L[i] = (last j < i with A[j] >= A[i]) + 1
    st = []
    ap = st.append
    pp = st.pop
    for i in range(n):
        ai = A[i]
        while st and A[st[-1]] < ai:
            pp()
        L[i] = st[-1] + 1 if st else 0
        ap(i)
    del st[:]
    # R[i] = (first j > i with A[j] > A[i]) - 1
    for i in range(n - 1, -1, -1):
        ai = A[i]
        while st and A[st[-1]] <= ai:
            pp()
        R[i] = st[-1] - 1 if st else n - 1
        ap(i)
    del st

    try:
        import numpy as np
    except Exception:
        np = None

    if np is not None:
        Aarr = np.array(A, dtype=np.int64)
        Larr = np.array(L, dtype=np.int64)
        Rarr = np.array(R, dtype=np.int64)
        Parr = np.array(P, dtype=np.int64)

        a = Larr - 1
        b = Rarr + 1
        ac = np.maximum(a, 0)
        bc = np.minimum(b, n - 1)
        INF = np.int64(1) << 62
        Av = np.where(a >= 0, Aarr[ac], INF)
        Bv = np.where(b < n, Aarr[bc], INF)
        p = np.where(Av < Bv, ac, bc)          # tie -> right boundary
        S = Parr[Rarr + 1] - Parr[Larr]
        cond = S > np.minimum(Av, Bv)          # root: min == INF -> False

        order = np.argsort(-Aarr, kind='stable')  # A desc, ties index asc

        pl = p.tolist()
        condl = cond.tolist()
        esc = S.tolist()
        for i in order.tolist():
            if condl[i]:
                esc[i] = esc[pl[i]]

        idx = np.arange(n, dtype=np.int64)
        stuck = (Larr == idx)
        eq = np.zeros(n, dtype=bool)
        if n > 1:
            eq[:n - 1] = (Aarr[1:] == Aarr[:n - 1])
        stuck &= eq
        res = np.where(stuck, Aarr, np.array(esc, dtype=np.int64))
        sys.stdout.write(' '.join(map(str, res.tolist())))
        sys.stdout.write('\n')
    else:
        order = sorted(range(n), key=A.__getitem__, reverse=True)
        esc = [0] * n
        for i in order:
            li = L[i]
            ri = R[i]
            aa = li - 1
            bb = ri + 1
            S = P[ri + 1] - P[li]
            if aa < 0:
                if bb >= n:
                    esc[i] = S
                    continue
                pi = bb
            elif bb >= n:
                pi = aa
            else:
                pi = aa if A[aa] < A[bb] else bb
            esc[i] = esc[pi] if S > A[pi] else S
        out = esc
        for k in range(n - 1):
            if L[k] == k and A[k + 1] == A[k]:
                out[k] = A[k]
        sys.stdout.write(' '.join(map(str, out)))
        sys.stdout.write('\n')

main()