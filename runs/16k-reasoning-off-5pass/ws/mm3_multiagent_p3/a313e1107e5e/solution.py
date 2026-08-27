import sys
import threading
import bisect

def main():
    import sys
    sys.setrecursionlimit(1 << 25)
    input = sys.stdin.readline

    N, Q = map(int, input().split())
    A = list(map(int, input().split()))
    queries = []
    for i in range(Q):
        R, X = map(int, input().split())
        queries.append((R, X, i))

    # Step 1: Compute first occurrence for each distinct value in A
    first_pos = {}
    for i, a in enumerate(A, 1):
        if a not in first_pos:
            first_pos[a] = i

    # Step 2: Coordinate compress distinct values (sorted)
    values = sorted(first_pos.keys())
    M = len(values)

    # Step 3: Build sequence P where P[i] = first_pos of i-th smallest value (1-indexed)
    P = [0] * (M + 1)  # 1-indexed
    for idx, v in enumerate(values):
        P[idx + 1] = first_pos[v]

    # Step 4: For each query, compute K = number of distinct values <= X
    K_of_query = []
    for R, X, i in queries:
        k = bisect.bisect_right(values, X)
        K_of_query.append(k)

    # Step 5: Create points (y=P[i], x=i) and sort by y
    points = [(P[i], i) for i in range(1, M + 1)]
    points.sort()  # sort by y (first element of tuple)

    # Step 6: Sort queries by R (the y-bound) for offline processing
    indexed_queries = [(queries[i][0], K_of_query[i], i) for i in range(Q)]  # (R, K, original_index)
    indexed_queries.sort()  # sort by R

    # Step 7: Fenwick tree (BIT) for maximum prefix query
    class BIT:
        def __init__(self, n):
            self.n = n
            self.tree = [0] * (n + 1)
        def update(self, idx, val):
            while idx <= self.n:
                if val > self.tree[idx]:
                    self.tree[idx] = val
                idx += idx & -idx
        def query(self, idx):
            res = 0
            while idx > 0:
                if self.tree[idx] > res:
                    res = self.tree[idx]
                idx -= idx & -idx
            return res

    bit = BIT(M)
    ans = [0] * Q
    p_idx = 0  # pointer in points

    # Process queries in order of increasing R
    for R, K, orig_idx in indexed_queries:
        # Add all points with y <= R
        while p_idx < len(points) and points[p_idx][0] <= R:
            _, x = points[p_idx]
            # Get maximum LIS length among points with index < x
            L = bit.query(x - 1) + 1
            bit.update(x, L)
            p_idx += 1
        # Answer for this query: maximum LIS length in prefix [1, K]
        ans[orig_idx] = bit.query(K)

    # Output answers
    out = '\n'.join(map(str, ans))
    sys.stdout.write(out)

if __name__ == "__main__":
    threading.Thread(target=main).start()