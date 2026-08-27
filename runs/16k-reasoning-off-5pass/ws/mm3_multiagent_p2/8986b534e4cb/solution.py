import sys
from sys import stdin
from math import inf, log2

def main():
    input = sys.stdin.readline
    N, M, Q = map(int, input().split())
    L = [0] * (M + 1)
    R = [0] * (M + 1)
    for i in range(1, M+1):
        s, t = map(int, input().split())
        if s < t:
            L[i] = s
            R[i] = t
        else:
            L[i] = t
            R[i] = s

    # Group by L
    groups = {}
    for i in range(1, M+1):
        l = L[i]
        if l not in groups:
            groups[l] = []
        groups[l].append(i)

    # Compute next_diff: for same L, smallest j>i with R_j != R_i
    next_diff = [inf] * (M + 1)
    for l, indices in groups.items():
        k = len(indices)
        nxt = [None] * k
        for idx in range(k-2, -1, -1):
            i_curr = indices[idx]
            i_next = indices[idx+1]
            if R[i_next] != R[i_curr]:
                nxt[idx] = idx+1
            else:
                nxt[idx] = nxt[idx+1] if nxt[idx+1] is not None else None
        for idx in range(k):
            i = indices[idx]
            if nxt[idx] is not None:
                next_diff[i] = indices[nxt[idx]]

    # Segment tree for different L case
    size = 1
    while size < N+2:
        size *= 2
    seg = [inf] * (2 * size)
    def seg_update(pos, val):
        i = pos + size
        seg[i] = min(seg[i], val)
        i //= 2
        while i:
            seg[i] = min(seg[2*i], seg[2*i+1])
            i //= 2
    def seg_query(l, r):
        if l > r:
            return inf
        l += size
        r += size
        res = inf
        while l <= r:
            if l % 2 == 1:
                res = min(res, seg[l])
                l += 1
            if r % 2 == 0:
                res = min(res, seg[r])
                r -= 1
            l //= 2
            r //= 2
        return res

    bad_next = [inf] * (M + 1)
    for i in range(M, 0, -1):
        if L[i] + 1 <= R[i] - 1:
            cand = seg_query(L[i]+1, R[i]-1)
        else:
            cand = inf
        bad_next[i] = min(next_diff[i], cand)
        seg_update(L[i], i)

    # Sparse table for range min on bad_next[1..M]
    log = [0] * (M + 1)
    for i in range(2, M+1):
        log[i] = log[i//2] + 1
    K = log[M] + 1
    st = [[inf] * M for _ in range(K)]
    for i in range(M):
        st[0][i] = bad_next[i+1]
    for k in range(1, K):
        for i in range(M - (1 << k) + 1):
            st[k][i] = min(st[k-1][i], st[k-1][i + (1 << (k-1))])
    def range_min(l, r):
        l -= 1
        r -= 1
        k = log[r - l + 1]
        return min(st[k][l], st[k][r - (1 << k) + 1])

    out = []
    for _ in range(Q):
        l, r = map(int, input().split())
        min_val = range_min(l, r)
        out.append("No" if min_val <= r else "Yes")
    print("\n".join(out))

if __name__ == "__main__":
    main()