import sys
sys.setrecursionlimit(1 << 25)

def solve():
    input = sys.stdin.readline
    N = int(input())
    contests = []
    max_val = 0
    for _ in range(N):
        L, R = map(int, input().split())
        contests.append((L, R))
        max_val = max(max_val, R)
    Q = int(input())
    queries = []
    max_query = 0
    for _ in range(Q):
        x = int(input())
        queries.append(x)
        max_query = max(max_query, x)
    # The domain size: we need to cover all possible initial ratings that appear in queries,
    # and also to ensure that for contests, we can find a and b correctly. The maximum initial
    # rating we care about is max(max_query, max_val) but actually final ratings can go higher,
    # but we only need to update F(X) for X up to the maximum initial rating that might be affected.
    # However, to be safe, we can set the size to max(max_query, max_val) + N, but that might be too large.
    # Actually, we only need to consider X up to the maximum initial rating in queries, because for larger X,
    # we don't have queries. But during the process, F(X) for X larger than max_query might be needed to
    # compute a and b? For example, if we have a contest with L=1, R=1e6, and max_query=5, then F(5) might
    # become large, but a and b are determined by F(X) for X up to max_query. However, if we set the domain
    # to max_query, then for X > max_query, we don't have F(X) defined, but we might need to check if
    # F(X) <= R for some X > max_query. But since there are no queries for X > max_query, we don't care
    # about updating them. However, when we find b, we need the largest X such that F(X) <= R. This could
    # be larger than max_query if F(X) for X > max_query is still <= R. But we don't have F(X) for those X.
    # To be correct, we should set the domain to at least the maximum possible initial rating that could
    # affect the queries. But since we only care about the final rating for queried X, we can restrict
    # the domain to [1, max_query]. But then when we process a contest, we need to consider that F(X)
    # for X > max_query might be <= R, and that would affect the condition? Actually, no: the condition
    # for updating is: for all X such that F(X) in [L, R], we add 1. If we ignore X > max_query, we might
    # miss some updates that would affect the F values for X <= max_query? No, because the update for
    # X > max_query does not affect F(X) for X <= max_query. So we can safely restrict the domain to
    # [1, max_query] as long as we correctly compute a and b within that domain. However, the true a
    # and b might extend beyond max_query. For example, if max_query=5, and there is a contest with L=1, R=10,
    # and for X=6, F(6) might be <= R, but we don't have X=6 in our domain. But does that affect the
    # update for X<=5? The update rule is: for all X, if F(X) in [L,R], then F(X)++. So if we only
    # consider X up to 5, we might miss the fact that for X=6, F(6) is in [L,R], and that doesn't
    # affect X=5. So it's fine. However, we need to compute a and b correctly for the domain [1, max_query].
    # That is, we need the smallest X in [1, max_query] with F(X) >= L, and the largest X in [1, max_query]
    # with F(X) <= R. If the true a is less than 1, we take 1. If the true b is greater than max_query,
    # we take max_query. But is it possible that for some X > max_query, F(X) is in [L,R], and that would
    # affect the condition for X <= max_query? No, because the update is independent per X. So we can
    # safely limit the domain to [1, max_query]. However, we must be careful: if we set the domain too
    # small, we might incorrectly compute a and b. For example, if max_query=5, and for all X in [1,5],
    # F(X) > R, but for X=6, F(6) <= R, then the true b would be >=6, but we would set b=5 (since
    # F(5) > R). That would be incorrect because there are X>5 with F(X) in [L,R], but we don't care
    # about them. So it's fine. But what if for X=5, F(5) <= R, and for X=6, F(6) > R, then the true
    # b is 5, which is within our domain. So we need to ensure that for the X in our domain, we correctly
    # compute a and b. The only issue is if the true a is less than 1 (impossible) or true b is greater
    # than max_query. But if true b > max_query, that means there exists X > max_query with F(X) <= R.
    # But for X = max_query+1, we don't have F(X). However, does that affect the update for X <= max_query?
    # No. So we can set b = max_query if F(max_query) <= R. But we need to check: if F(max_query) <= R,
    # then b should be at least max_query. But if there is some X > max_query with F(X) > R, then the
    # true b is max_query. So we need to find the largest X in [1, max_query] with F(X) <= R. That's
    # exactly what our algorithm does. So it's correct. Therefore, we can set the domain size to
    # max_query. But wait, what if max_query is 0? Not possible. So we set M = max_query.
    # However, to be safe, we might set M = max(max_query, max_val) because some contests might have
    # L > max_query, and then a would be > max_query, and we would have no X to update. That's fine.
    # But if we set M too small, we might miss updates for X that are not in queries but could affect
    # the F values for queried X? No, because updates for different X are independent. So it's fine.
    # So we set M = max_query.
    # But what if there are no queries? Q>=1, so max_query >=1.
    # So M = max_query.
    M = max_query
    if M == 0:
        # No queries, but Q>=1, so this won't happen.
        return

    # Segment tree
    size = 1
    while size < M:
        size <<= 1
    # Initialize arrays
    INF = 10**18
    minv = [INF] * (2 * size)
    maxv = [0] * (2 * size)
    lazy = [0] * (2 * size)
    # Build leaves
    for i in range(M):
        minv[size + i] = i + 1
        maxv[size + i] = i + 1
    for i in range(M, size):
        minv[size + i] = INF
        maxv[size + i] = 0
    # Build internal nodes
    for i in range(size - 1, 0, -1):
        minv[i] = min(minv[2*i], minv[2*i+1])
        maxv[i] = max(maxv[2*i], maxv[2*i+1])

    def apply(node, val):
        if minv[node] == INF:
            return
        minv[node] += val
        maxv[node] += val
        if node < size:
            lazy[node] += val

    def push(node):
        if lazy[node] != 0:
            apply(2*node, lazy[node])
            apply(2*node+1, lazy[node])
            lazy[node] = 0

    # Range add on [l, r] (1-indexed, inclusive)
    def range_add(l, r, val):
        l += size - 1
        r += size - 1
        l0, r0 = l, r
        while l <= r:
            if l % 2 == 1:
                apply(l, val)
                l += 1
            if r % 2 == 0:
                apply(r, val)
                r -= 1
            l //= 2
            r //= 2
        # After updates, we need to pull up the changes
        for i in [l0, r0]:
            i //= 2
            while i >= 1:
                new_min = min(minv[2*i], minv[2*i+1])
                new_max = max(maxv[2*i], maxv[2*i+1])
                if minv[i] == new_min and maxv[i] == new_max:
                    # No change, we can break if we want, but we need to update ancestors
                    # Actually, we need to update all ancestors up to root
                    minv[i] = new_min
                    maxv[i] = new_max
                else:
                    minv[i] = new_min
                    maxv[i] = new_max
                i //= 2

    # Point query to get value at x (1-indexed)
    def point_query(x):
        x += size - 1
        # Push down from root to leaf
        stack = []
        node = 1
        while node < size:
            push(node)
            if x < node * 2:
                node = node * 2
            else:
                node = node * 2 + 1
        return minv[node]  # value at leaf

    # Find smallest x such that F(x) >= L
    def find_left(L_bound):
        # Returns smallest x in [1, M] with F(x) >= L_bound, or None if not exists
        if maxv[1] < L_bound:
            return None
        node = 1
        while node < size:
            push(node)
            left = node * 2
            if maxv[left] >= L_bound:
                node = left
            else:
                node = left + 1
        # node is a leaf
        idx = node - size + 1
        if idx > M:
            return None
        return idx

    # Find largest x such that F(x) <= R_bound
    def find_right(R_bound):
        # Returns largest x in [1, M] with F(x) <= R_bound, or None if not exists
        if minv[1] > R_bound:
            return None
        node = 1
        while node < size:
            push(node)
            right = node * 2 + 1
            if minv[right] <= R_bound:
                node = right
            else:
                node = right - 1
        idx = node - size + 1
        if idx > M:
            return None
        return idx

    # Process contests
    for L, R in contests:
        a = find_left(L)
        if a is None:
            continue
        b = find_right(R)
        if b is None:
            continue
        if a <= b:
            range_add(a, b, 1)

    # Answer queries
    out = []
    for x in queries:
        out.append(str(point_query(x)))
    print('\n'.join(out))

if __name__ == "__main__":
    solve()