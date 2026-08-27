import sys
from sys import setrecursionlimit

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    adj = [[] for _ in range(N+1)]
    for _ in range(N-1):
        a = int(next(it)); b = int(next(it))
        adj[a].append(b); adj[b].append(a)
    
    # iterative post-order traversal
    parent = [0]*(N+1)
    order = []
    stack = [1]
    parent[1] = -1
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if v != parent[u]:
                parent[v] = u
                stack.append(v)
    # order is preorder; reverse to get post-order
    order.reverse()
    
    # dp1[u], dp3[u], dp4[u]
    NEG = -10**9
    dp1 = [NEG]*(N+1)
    dp3 = [NEG]*(N+1)
    dp4 = [NEG]*(N+1)
    
    for u in order:
        contribs = []
        for v in adj[u]:
            if parent[v] == u:  # v is child of u
                best = dp1[v] if dp1[v] > dp3[v] else dp3[v]
                contribs.append(best)
        contribs.sort(reverse=True)
        if len(contribs) >= 1:
            dp1[u] = 1 + contribs[0]
        if len(contribs) >= 3:
            dp3[u] = 1 + contribs[0] + contribs[1] + contribs[2]
        if len(contribs) >= 4:
            dp4[u] = 1 + contribs[0] + contribs[1] + contribs[2] + contribs[3]
    
    ans = -1
    for u in range(1, N+1):
        if dp4[u] > ans:
            ans = dp4[u]
    print(ans)

if __name__ == "__main__":
    setrecursionlimit(300000)
    main()