import sys

def solve() -> None:
    import sys
    sys.setrecursionlimit(1 << 25)
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    A = [0] + [int(next(it)) for _ in range(N)]   # 1‑indexed

    # ---------- prefix sums ----------
    P = [0] * (N + 1)
    for i in range(1, N + 1):
        P[i] = P[i-1] + A[i]
    total_sum = P[N]

    # ---------- segment tree (range maximum) ----------
    size = 1
    while size < N:
        size <<= 1
    seg = [0] * (2 * size)
    # leaves
    for i in range(N):
        seg[size + i] = A[i + 1]
    # internal nodes
    for i in range(size - 1, 0, -1):
        seg[i] = seg[2 * i] if seg[2 * i] >= seg[2 * i + 1] else seg[2 * i + 1]

    # ----- recursive search for rightmost index with value >= S -----
    def find_rightmost(node, nl, nr, ql, qr, S):
        """return rightmost index in [ql,qr] (1‑based) whose A[index] >= S,
           or None if no such index exists"""
        if nr < ql or nl > qr or seg[node] < S:
            return None
        if nl == nr:                 # leaf
            idx = nl
            if idx <= N and A[idx] >= S:
                return idx
            return None
        mid = (nl + nr) // 2
        # search right child first to obtain the rightmost index
        res = find_rightmost(node * 2 + 1, mid + 1, nr, ql, qr, S)
        if res is not None:
            return res
        return find_rightmost(node * 2, nl, mid, ql, qr, S)

    # ----- recursive search for leftmost index with value >= S -----
    def find_leftmost(node, nl, nr, ql, qr, S):
        """return leftmost index in [ql,qr] (1‑based) whose A[index] >= S,
           or None if no such index exists"""
        if nr < ql or nl > qr or seg[node] < S:
            return None
        if nl == nr:                 # leaf
            idx = nl
            if idx <= N and A[idx] >= S:
                return idx
            return None
        mid = (nl + nr) // 2
        # search left child first to obtain the leftmost index
        res = find_leftmost(node * 2, nl, mid, ql, qr, S)
        if res is not None:
            return res
        return find_leftmost(node * 2 + 1, mid + 1, nr, ql, qr, S)

    # wrappers
    def rightmost_ge(l, r, S):
        if l > r:
            return None
        return find_rightmost(1, 1, size, l, r, S)

    def leftmost_ge(l, r, S):
        if l > r:
            return None
        return find_leftmost(1, 1, size, l, r, S)

    # ---------- compute answer for every K ----------
    ans = [0] * (N + 1)
    for K in range(1, N + 1):
        S = A[K]
        L = K
        R = K
        # repeatedly expand the interval
        while True:
            changed = False

            # ----- expand to the left -----
            if L > 1:
                i = rightmost_ge(1, L - 1, S)          # barrier on the left
                if i is None:                           # no barrier
                    S += P[L - 1] - P[0]
                    L = 1
                    changed = True
                else:
                    # absorb the block (i+1 .. L-1)
                    if i + 1 <= L - 1:
                        S += P[L - 1] - P[i]
                        L = i + 1
                        changed = True
                    # possibly absorb the barrier itself
                    if S > A[i]:
                        S += A[i]
                        L = i
                        changed = True

            # ----- expand to the right -----
            if R < N:
                j = leftmost_ge(R + 1, N, S)            # barrier on the right
                if j is None:                           # no barrier
                    S += P[N] - P[R]
                    R = N
                    changed = True
                else:
                    # absorb the block (R+1 .. j-1)
                    if R + 1 <= j - 1:
                        S += P[j - 1] - P[R]
                        R = j - 1
                        changed = True
                    # possibly absorb the barrier itself
                    if S > A[j]:
                        S += A[j]
                        R = j
                        changed = True

            if not changed:
                break
            # early stop if the whole array has been absorbed
            if L == 1 and R == N:
                S = total_sum
                break

        ans[K] = S

    # ---------- output ----------
    sys.stdout.write(' '.join(map(str, ans[1:])))

if __name__ == "__main__":
    solve()