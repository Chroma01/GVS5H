def biconnected_components(N, adj, U, V):
    dfn=[0]*N; low=[0]*N; parent=[-1]*N; pedge=[-1]*N; child=[0]*N
    is_art=[False]*N
    comps=[]
    time=0
    edge_stack=[]
    for start in range(N):
        if dfn[start]: continue
        time+=1; dfn[start]=low[start]=time
        stack=[(start,0)]
        while stack:
            u, idx = stack[-1]
            if idx < len(adj[u]):
                v,eid = adj[u][idx]
                stack[-1]=(u,idx+1)
                if eid == pedge[u]:
                    continue
                if dfn[v]==0:
                    parent[v]=u; pedge[v]=eid; child[u]+=1
                    edge_stack.append(eid)
                    time+=1; dfn[v]=low[v]=time
                    stack.append((v,0))
                elif dfn[v] < dfn[u]:
                    edge_stack.append(eid)
                    if dfn[v] < low[u]: low[u]=dfn[v]
            else:
                stack.pop()
                if parent[u] != -1:
                    p=parent[u]
                    if low[u] < low[p]: low[p]=low[u]
                    if low[u] >= dfn[p]:
                        if parent[p] != -1 or child[p] > 1:
                            is_art[p]=True
                        comp=[]
                        while True:
                            e=edge_stack.pop()
                            comp.append(e)
                            if e == pedge[u]: break
                        comps.append(comp)
                else:
                    if child[u] > 1:
                        is_art[u]=True
                    # edge_stack should be empty for this component? If graph connected and root, yes. But if multiple components, maybe leftover? For root, each child popped. If root has no children (N=1) no edges.
    return comps, is_art