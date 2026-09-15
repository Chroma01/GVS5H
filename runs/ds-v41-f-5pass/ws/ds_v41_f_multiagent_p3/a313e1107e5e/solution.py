import sys
from bisect import bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    Q = int(data[idx]); idx += 1
    A = [0] * N
    for i in range(N):
        A[i] = int(data[idx]); idx += 1

    R = [0] * Q
    X = [0] * Q
    # group queries by R via linked lists (head[r] = first query index)
    head = [-1] * (N + 1)
    nxt = [-1] * Q
    for q in range(Q):
        r = int(data[idx]); x = int(data[idx + 1]); idx += 2
        R[q] = r
        X[q] = x
        nxt[q] = head[r]
        head[r] = q

    sorted_A = sorted(set(A))
    M = len(sorted_A)
    tree = [0] * (M + 1)   # Fenwick tree for prefix max
    ans = [0] * Q

    for i in range(1, N + 1):
        ai = A[i - 1]
        p = bisect_right(sorted_A, ai)  # 1-indexed rank of ai

        # strict: longest increasing ending here uses values < ai => prefix p-1
        res = 0
        j = p - 1
        while j > 0:
            v = tree[j]
            if v > res:
                res = v
            j -= j & (-j)
        dp = res + 1

        # point-update (max) at rank p
        j = p
        while j <= M:
            if tree[j] < dp:
                tree[j] = dp
            j += j & (-j)

        # answer all queries with R == i using current prefix
        q = head[i]
        while q != -1:
            pos = bisect_right(sorted_A, X[q])  # count of values <= X
            res = 0
            j = pos
            while j > 0:
                v = tree[j]
                if v > res:
                    res = v
                j -= j & (-j)
            ans[q] = res
            q = nxt[q]

    sys.stdout.write('\n'.join(map(str, ans)) + '\n')

main()