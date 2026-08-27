def endpoint_extra(N, adj, X, forbidden, INF):
    if forbidden < 0: return INF
    dist = [-1]*N; dist[X]=0; q=[X]
    while: for v in adj[u]: if v==forbidden continue; if dist[v]==-1: dist[v]=nd; q.append(v)
    best=INF
    for w in range(N):
        dw=dist[w]
        if dw == -1 or dw >= best: continue
        c=0
        for v in adj[w]:
            if v==forbidden: continue
            dv=dist[v]
            if dv != -1 and dv >= dw:
                c += 1
                if c >= 2: break
        if c >= 2:
            best = dw
            if best == 0: break
    if best == INF: return INF
    return 4*(best+1)