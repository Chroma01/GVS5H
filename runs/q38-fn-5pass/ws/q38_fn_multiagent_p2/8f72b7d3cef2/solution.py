import sys
from bisect import bisect_right


def solve():
    A = list(map(int, sys.stdin.buffer.read().split()))
    if not A:
        return
    N = A[0]
    A[0] = 0

    INF = 10**18
    NEG = -INF
    n = N + 1  # positions p = j-1, p=0..N, p=N is right sentinel

    size = 1
    while size < n:
        size <<= 1

    tree = [NEG] * (2 * size)
    P = [0] * n

    s = 0
    base = size
    tr = tree
    for i in range(1, N + 1):
        a = A[i]
        # C_i = A_i - P_{i-1}, stored at position i-1
        tr[base + i - 1] = a - s
        s += a
        P[i] = s

    # sentinel C_{N+1} = +infinity, stored at position N
    tr[base + N] = INF

    for idx in range(size - 1, 0, -1):
        left = tr[idx << 1]
        right = tr[(idx << 1) | 1]
        tr[idx] = left if left >= right else right

    # First position >= l whose value is >= th.
    def find_first(l, th, tr=tr, sz=size, nn=n):
        if l >= nn:
            return nn
        l += sz
        while True:
            while (l & 1) == 0:
                l >>= 1
            if tr[l] >= th:
                while l < sz:
                    l <<= 1
                    if tr[l] < th:
                        l += 1
                return l - sz
            l += 1
            if (l & (l - 1)) == 0:
                return nn

    # Last position < r whose value is >= th, or -1.
    def find_last(r, th, tr=tr, sz=size, nn=n):
        if r <= 0:
            return -1
        r += sz
        while True:
            r -= 1
            while r > 1 and (r & 1):
                r >>= 1
            if tr[r] >= th:
                while r < sz:
                    r = (r << 1) | 1
                    if tr[r] < th:
                        r -= 1
                return r - sz
            if (r & (r - 1)) == 0:
                return -1

    # serviceR[i] = largest interval end p such that left boundary i is feasible.
    # i can serve K in [i+1, serviceR[i]].
    serviceR = [0] * N
    serviceR[0] = N  # left sentinel can always serve all K via whole interval

    br = bisect_right
    fl = find_last
    P_loc = P
    A_loc = A
    tr_loc = tr
    base_loc = base
    sr = serviceR

    for i in range(1, N):
        pi = P_loc[i]
        # largest r with P[r] - P[i] <= A[i]
        R = br(P_loc, pi + A_loc[i]) - 1
        if R > i:
            th = -pi
            if R == N:
                # right sentinel is always valid and is the rightmost possible end
                sr[i] = N
            elif tr_loc[base_loc + R] >= th:
                # position R itself already satisfies the right condition
                sr[i] = R
            elif R > i + 1:
                # find_last(R, th) already returns the largest position < R
                p = fl(R, th)
                if p > i:
                    sr[i] = p

    del A, A_loc

    # Assign each K the maximum feasible left boundary i.
    # Process i decreasing; DSU "next unassigned" gives O(N alpha(N)).
    parent = list(range(N + 2))
    ans = [0] * (N + 1)

    ff = find_first
    par = parent
    ans_loc = ans
    P_loc = P
    tr_loc = tr
    base_loc = base

    for i in range(N - 1, -1, -1):
        R = sr[i]
        L = i + 1
        if R < L:
            continue

        k = L
        while par[k] != k:
            par[k] = par[par[k]]
            k = par[k]
        if k > R:
            continue

        th = -P_loc[i]
        baseP = P_loc[i]
        cur = -1

        while k <= R:
            if k > cur:
                # If position k itself is a valid right boundary, use it directly.
                if tr_loc[base_loc + k] >= th:
                    cur = k
                else:
                    cur = ff(k + 1, th)
                    # Sentinel guarantees existence; this is only a safety guard.
                    if cur > N:
                        cur = N

            ans_loc[k] = P_loc[cur] - baseP

            nk = k + 1
            while par[nk] != nk:
                par[nk] = par[par[nk]]
                nk = par[nk]
            par[k] = nk
            k = nk

    sys.stdout.write(" ".join(map(str, ans_loc[1:])))
    sys.stdout.write("\n")


if __name__ == "__main__":
    solve()