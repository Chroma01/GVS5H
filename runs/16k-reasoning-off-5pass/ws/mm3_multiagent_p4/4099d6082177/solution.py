import sys
sys.setrecursionlimit(1 << 25)

def solve():
    import sys
    input = sys.stdin.readline
    N, K = map(int, input().split())
    total = N * K
    if K == 1:
        print("Yes")
        return
    if total == 1:
        print("Yes")
        return

    adj = [[] for _ in range(total + 1)]
    for _ in range(total - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)

    completed = [0]

    def dfs(u, p):
        dangles = []
        for v in adj[u]:
            if v == p:
                continue
            d = dfs(v, u)
            if d == -1:
                return -1
            if d == 0:
                continue
            if d == K:
                completed[0] += 1
                continue
            dangles.append(d)

        # Leaf node: no child dangles
        if not dangles:
            # True leaf (degree 1, not root) returns a dangle of length 1
            if len(adj[u]) == 1 and u != 1:
                return 1
            # Root with no children (single node tree) — handled by K=1 or total==1
            return 0

        # Close any dangle of length K-1: u becomes the other endpoint
        remaining = []
        for d in dangles:
            if d == K - 1:
                completed[0] += 1
            else:
                remaining.append(d)

        # Greedily pair dangles via min-heap
        import heapq
        heap = remaining[:]
        heapq.heapify(heap)
        while len(heap) >= 2:
            a = heapq.heappop(heap)
            b = heapq.heappop(heap)
            s = a + b + 1
            if s == K:
                completed[0] += 1
            elif s < K:
                heapq.heappush(heap, s)
            else:
                return -1

        if heap:
            val = heap[0]
            # Extend the single remaining dangle through u
            if val + 1 == K:
                completed[0] += 1
                return 0
            elif val + 1 < K:
                return val + 1
            else:
                return -1
        return 0

    root_res = dfs(1, 0)
    if root_res == -1:
        print("No")
        return
    if root_res == K:
        completed[0] += 1
    elif root_res > 0:
        print("No")
        return

    if completed[0] == N:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()