import sys
import numpy as np


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    A = np.array(list(map(int, data[pos:pos + N])), dtype=np.int64); pos += N
    B = np.array(list(map(int, data[pos:pos + N])), dtype=np.int64); pos += N
    K = int(data[pos]); pos += 1
    qs = data[pos:pos + 2 * K]

    # number of blocks target ~ sqrt(K), capped so that two (nb+1)x(N+1)
    # int64 arrays fit comfortably in memory
    nblk_target = max(1, min(64, int(K ** 0.5) + 1))
    S = max(1, (N + nblk_target - 1) // nblk_target)
    nblk = (N + S - 1) // S
    bounds = [min(b * S, N) for b in range(nblk + 1)]

    # Uc[bj, t] = sum_{i<t} sum_{j<bounds[bj]} |A_i - B_j|   (row 0 == 0)
    Uc = np.zeros((nblk + 1, N + 1), dtype=np.int64)
    for bj in range(1, nblk + 1):
        lo = bounds[bj - 1]; hi = bounds[bj]
        sb = np.sort(B[lo:hi])
        L = sb.shape[0]
        pb = np.empty(L + 1, dtype=np.int64)
        pb[0] = 0
        np.cumsum(sb, out=pb[1:])
        idx = np.searchsorted(sb, A, side='right')          # count of b <= A_i
        contrib = A * (2 * idx - L) + (pb[L] - 2 * pb[idx])
        np.add(Uc[bj - 1, 1:], np.cumsum(contrib), out=Uc[bj, 1:])

    # Vc[bi, t] = sum_{j<t} sum_{i<bounds[bi]} |A_i - B_j|
    Vc = np.zeros((nblk + 1, N + 1), dtype=np.int64)
    for bi in range(1, nblk + 1):
        lo = bounds[bi - 1]; hi = bounds[bi]
        sb = np.sort(A[lo:hi])
        L = sb.shape[0]
        pb = np.empty(L + 1, dtype=np.int64)
        pb[0] = 0
        np.cumsum(sb, out=pb[1:])
        idx = np.searchsorted(sb, B, side='right')
        contrib = B * (2 * idx - L) + (pb[L] - 2 * pb[idx])
        np.add(Vc[bi - 1, 1:], np.cumsum(contrib), out=Vc[bi, 1:])

    # P[bi][bj] = full-block answer = sum_{i<bi*S, j<bj*S} |A_i - B_j|
    P = [[0] * (nblk + 1) for _ in range(nblk + 1)]
    for bj in range(nblk + 1):
        col = Uc[bj]
        for bi in range(nblk + 1):
            P[bi][bj] = int(col[bounds[bi]])

    out = []
    ap = out.append
    for t in range(K):
        X = int(qs[2 * t]); Y = int(qs[2 * t + 1])
        bi = X // S; bj = Y // S
        a0 = bi * S; b0 = bj * S
        ans = P[bi][bj] + (int(Uc[bj, X]) - int(Uc[bj, a0])) \
                         + (int(Vc[bi, Y]) - int(Vc[bi, b0]))
        if a0 < X and b0 < Y:
            remA = A[a0:X]
            sb = np.sort(B[b0:Y])
            L = sb.shape[0]
            pb = np.empty(L + 1, dtype=np.int64)
            pb[0] = 0
            np.cumsum(sb, out=pb[1:])
            idx = np.searchsorted(sb, remA, side='right')
            ans += int((remA * (2 * idx - L) + (pb[L] - 2 * pb[idx])).sum())
        ap(str(ans))
    sys.stdout.write("\n".join(out) + "\n")


main()