def bfs(N, adj, src):
    dist = [-1]*N
    parent = [-1]*N
    dist[src]=0
    q=[src]
    order=[]
    head=0
    while head < len(q):
        v=q[head]; head+=1; order.append(v)
        nd=dist[v]+1
        for u in adj[v]:
            if dist[u]==-1:
                dist[u]=nd; parent[u]=v; q.append(u)
    return dist, order, parent