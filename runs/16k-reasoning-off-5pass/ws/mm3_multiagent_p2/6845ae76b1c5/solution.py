import sys
import bisect

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    B = [int(next(it)) for _ in range(N)]
    K = int(next(it))
    queries = []
    for idx in range(K):
        X = int(next(it))
        Y = int(next(it))
        queries.append((Y, X, idx))

    A.sort()
    B.sort()

    # prefix sums: SA[i] = sum of first i elements of A (i from 0..N)
    SA = [0] * (N + 1)
    for i in range(N):
        SA[i+1] = SA[i] + A[i]
    SB = [0] * (N + 1)
    for i in range(N):
        SB[i+1] = SB[i] + B[i]

    # Segment tree with lazy propagation
    size = 4 * N
    sumC = [0] * size          # Σ c_i in segment
    sumW = [0] * size          # Σ A_i * c_i in segment
    sumS = [0] * size          # Σ s_i in segment
    lazyC = [0] * size         # pending count addition
    lazyS = [0] * size         # pending sum addition

    def apply(node, l, r, addC, addS):
        length = r - l + 1
        sumC[node] += addC * length
        # sum of A in this segment using global prefix sums
        seg_sumA = SA[r+1] - SA[l]
        sumW[node] += addC * seg_sumA
        sumS[node] += addS * length
        lazyC[node] += addC
        lazyS[node] += addS

    def push(node, l, r):
        if l == r or (lazyC[node] == 0 and lazyS[node] == 0):
            return
        mid = (l + r) // 2
        left = node * 2
        right = left + 1
        apply(left, l, mid, lazyC[node], lazyS[node])
        apply(right, mid+1, r, lazyC[node], lazyS[node])
        lazyC[node] = 0
        lazyS[node] = 0

    def pull(node):
        left = node * 2
        right = left + 1
        sumC[node] = sumC[left] + sumC[right]
        sumW[node] = sumW[left] + sumW[right]
        sumS[node] = sumS[left] + sumS[right]

    def update(node, l, r, ql, qr, addC, addS):
        if ql <= l and r <= qr:
            apply(node, l, r, addC, addS)
            return
        push(node, l, r)
        mid = (l + r) // 2
        if ql <= mid:
            update(node*2, l, mid, ql, qr, addC, addS)
        if qr > mid:
            update(node*2+1, mid+1, r, ql, qr, addC, addS)
        pull(node)

    def query(node, l, r, ql, qr):
        if ql <= l and r <= qr:
            return sumW[node], sumS[node]
        push(node, l, r)
        mid = (l + r) // 2
        resW = 0
        resS = 0
        if ql <= mid:
            w, s = query(node*2, l, mid, ql, qr)
            resW += w
            resS += s
        if qr > mid:
            w, s = query(node*2+1, mid+1, r, ql, qr)
            resW += w
            resS += s
        return resW, resS

    # Process queries sorted by Y
    queries.sort()
    answers = [0] * K
    processed = 0  # number of B values already activated
    for Y, X, idx in queries:
        # activate B values until we have Y of them
        while processed < Y:
            b_val = B[processed]
            pos = bisect.bisect_left(A, b_val)
            if pos < N:
                update(1, 0, N-1, pos, N-1, 1, b_val)
            processed += 1
        # answer query for prefix of A of length X
        sumW_q, sumS_q = query(1, 0, N-1, 0, X-1)
        SA_X = SA[X]
        SB_Y = SB[Y]
        ans = 2 * sumW_q - Y * SA_X + X * SB_Y - 2 * sumS_q
        answers[idx] = ans

    out = '\n'.join(str(answers[i]) for i in range(K))
    sys.stdout.write(out)

if __name__ == "__main__":
    solve()