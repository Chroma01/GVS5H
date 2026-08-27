import sys
sys.setrecursionlimit(1 << 25)

def solve():
    input = sys.stdin.readline
    N = int(input())
    adj = [[] for _ in range(N + 1)]
    for _ in range(N - 1):
        a, b = map(int, input().split())
        adj[a].append(b)
        adj[b].append(a)
    
    parent = [0] * (N + 1)
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
    
    NEG = -10**18
    g = [0] * (N + 1)          # best size of partial alkane using parent edge (may or may not have internal vertex)
    use_int = [0] * (N + 1)    # best size of partial alkane using parent edge that has at least one internal vertex
    down0 = [0] * (N + 1)      # best alkane within subtree where u is leaf (p=0, x=1)
    down4 = [0] * (N + 1)      # best alkane within subtree where u is internal (p=0, x=4)
    best = [0] * (N + 1)       # best alkane entirely within subtree
    ans = 0
    
    for u in reversed(order):
        children = [v for v in adj[u] if v != parent[u]]
        child_g = []
        max_use_int_child = NEG
        for v in children:
            child_g.append(g[v])
            if use_int[v] > max_use_int_child:
                max_use_int_child = use_int[v]
        child_g.sort(reverse=True)
        
        # compute use_int[u]: u is internal (x=3) -> need top 3 g[child]
        if len(child_g) >= 3:
            use_int[u] = 1 + child_g[0] + child_g[1] + child_g[2]
        else:
            use_int[u] = NEG
        
        # g[u] is the best size when edge to parent is used (leaf or internal)
        g[u] = max(use_int[u], 1)
        
        # down0[u]: u is leaf, pick one child that provides an internal vertex
        if max_use_int_child > NEG:
            down0[u] = 1 + max_use_int_child
        else:
            down0[u] = NEG
        
        # down4[u]: u is internal, pick top 4 children by g[child]
        if len(child_g) >= 4:
            down4[u] = 1 + child_g[0] + child_g[1] + child_g[2] + child_g[3]
        else:
            down4[u] = NEG
        
        # best[u]: best alkane in subtree of u
        best_u = max(0, down0[u], down4[u])
        for v in children:
            if best[v] > best_u:
                best_u = best[v]
        best[u] = best_u
        if best_u > ans:
            ans = best_u
    
    if ans == 0:
        print(-1)
    else:
        print(ans)

if __name__ == "__main__":
    solve()