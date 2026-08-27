import sys
import sys
sys.setrecursionlimit(1 << 25)

def solve():
    import sys
    input = sys.stdin.readline
    N = int(input())
    adj = [[] for _ in range(N)]
    for _ in range(N-1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        adj[u].append(v)
        adj[v].append(u)
    
    # Determine leaves: degree == 1 (except when N==1, but N>=3)
    is_leaf = [False]*N
    for i in range(N):
        if len(adj[i]) == 1:
            is_leaf[i] = True
    
    # First DFS: compute down[v] = number of leaves in subtree of v (including v if leaf)
    # Use iterative stack to avoid recursion limit
    parent = [-1]*N
    order = []
    stack = [0]
    parent[0] = -1
    while stack:
        v = stack.pop()
        order.append(v)
        for b in adj[v]:
            if b != parent[v]:
                parent[b] = v
                stack.append(b)
    
    down = [0]*N
    for v in reversed(order):
        cnt = 0
        if is_leaf[v]:
            cnt = 1
        for b in adj[v]:
            if b != parent[v]:
                cnt += down[b]
        down[v] = cnt
    
    L = 0
    for i in range(N):
        if is_leaf[i]:
            L += 1
    
    # For each node v, compute best (1 + max_y freq[y]*(y+1))
    ans = N - 1  # worst case: keep nothing? Actually we can always keep at least the root? Wait, we can keep 1 vertex (a leaf) as a snowflake? No, snowflake needs center with at least 1 hub with at least 1 leaf. But we can delete all but a single vertex? The problem says we can delete zero or more vertices. We can delete N-1 vertices and keep one vertex. Is a single vertex a Snowflake Tree? Definition: choose positive integers x,y. So x>=1, y>=1. So a single vertex is NOT a Snowflake Tree. So we need to keep at least 1 + x + x*y >= 1+1+1=3 vertices. But the answer is N - max_size. If max_size is at least 3, we can delete N-3. If we cannot find any Snowflake Tree, the problem says it's always possible, so max_size >= 3. However, if N=3, sample 2 shows max_size=3. So we initialize ans as a large number.
    ans = N  # placeholder
    
    # For each node v, gather leaf counts of its neighbors
    # We need to process all nodes. We can precompute for each node a list of its neighbors' component leaf counts.
    # But we can compute on the fly.
    # For each v, we need to consider each neighbor b:
    #   if b is child of v (parent[b]==v): leaf_count = down[b]
    #   else (b is parent of v): leaf_count = L - down[v]  (i.e., up[v])
    # So for each v, we can iterate over neighbors, compute leaf_count, and update frequency in a dict.
    # But doing a dict per node is O(N deg) average, but in worst case could be O(N^2) if we use Python dicts. However, N is 3e5, and we need O(N) total. We need a way to compute max freq[y]*(y+1) efficiently.
    # Since the sum of degrees is 2(N-1), iterating over all edges and for each node computing frequencies is O(N) if we can compute max per node in O(deg) time without hashmap overhead? Actually we can use a dictionary per node because total operations across all nodes is O(N) (since sum of deg = 2N-2, and each neighbor is processed once per node? No, each node v processes its own neighbors. So total neighbor processing across all nodes is 2 * sum(deg(v)) = 4(N-1) = O(N). So O(N) total operations. Using Python dicts with O(1) average per op is fine.
    
    for v in range(N):
        freq = {}
        for b in adj[v]:
            if parent[b] == v:  # b is child
                lc = down[b]
            else:  # b is parent of v
                lc = L - down[v]
            freq[lc] = freq.get(lc, 0) + 1
        # Find best y
        best = 0
        for y, cnt in freq.items():
            # We can only choose y if y >= 1? The definition says y is positive integer. So y>=1.
            if y >= 1:
                val = cnt * (y + 1)
                if val > best:
                    best = val
        size = 1 + best
        deletions = N - size
        if deletions < ans:
            ans = deletions
    
    print(ans)

if __name__ == "__main__":
    solve()