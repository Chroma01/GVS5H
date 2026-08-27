import sys
from collections import deque

def solve():
    import sys
    input = sys.stdin.readline
    N, M, A, B = map(int, input().split())
    bad = []
    for _ in range(M):
        l, r = map(int, input().split())
        bad.append((l, r))

    # Build good intervals
    goods = []
    if M == 0:
        goods.append((1, N))
    else:
        if bad[0][0] > 1:
            goods.append((1, bad[0][0] - 1))
        for i in range(M - 1):
            r_cur = bad[i][1]
            l_next = bad[i + 1][0]
            if l_next - 1 >= r_cur + 1:
                goods.append((r_cur + 1, l_next - 1))
        if bad[-1][1] < N:
            goods.append((bad[-1][1] + 1, N))

    n = len(goods)
    if n == 0:
        print("No")
        return

    # DSU to merge good intervals that can be crossed in one jump
    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        x = find(x)
        y = find(y)
        if x == y:
            return
        if size[x] < size[y]:
            x, y = y, x
        parent[y] = x
        size[x] += size[y]

    for i in range(n - 1):
        l_cur, r_cur = goods[i]
        l_next, r_next = goods[i + 1]
        gap = l_next - r_cur
        if A <= gap <= B:
            union(i, i + 1)

    # Compute the overall interval for each connected component
    comps = {}
    for i in range(n):
        root = find(i)
        l, r = goods[i]
        if root not in comps:
            comps[root] = [l, r]
        else:
            if l < comps[root][0]:
                comps[root][0] = l
            if r > comps[root][1]:
                comps[root][1] = r

    comp_list = list(comps.values())
    comp_list.sort(key=lambda x: x[0])
    K = len(comp_list)

    # Find the component containing square 1
    start_idx = -1
    end_idx = -1
    for idx, (l, r) in enumerate(comp_list):
        if l <= 1 <= r:
            start_idx = idx
        if l <= N <= r:
            end_idx = idx

    if start_idx == -1:
        print("No")
        return
    if end_idx != -1:
        print("Yes")
        return

    # Build adjacency list between components
    adj = [[] for _ in range(K)]
    for i in range(K):
        l_i, r_i = comp_list[i]
        j = i + 1
        while j < K and comp_list[j][0] - r_i <= B:
            d = comp_list[j][0] - r_i
            if A <= d <= B:
                adj[i].append(j)
            j += 1

    # BFS from start component
    visited = [False] * K
    q = deque([start_idx])
    visited[start_idx] = True
    while q:
        u = q.popleft()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                l_v, r_v = comp_list[v]
                if l_v <= N <= r_v:
                    print("Yes")
                    return
                q.append(v)
    print("No")

if __name__ == "__main__":
    solve()