import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0]); M = int(data[1]); K = int(data[2])
    edges = []
    ptr = 3
    for _ in range(M):
        u = int(data[ptr]); v = int(data[ptr + 1]); ptr += 2
        edges.append((u, v))

    INF = K + 1          # any cut using an INF arc already exceeds K
    limit = K + 1        # early stop for max-flow

    def min_tight(d):
        """min number of 'tight' edges over labelings p:V->{0..d}, p(1)=0, p(N)=d,
           p(v)-p(u) <= 1 for every edge.  Value capped at K+1."""
        if d == 0:
            return 0
        S = 0
        T = 1
        inter = N - 2
        nnodes = 2 + (inter if inter > 0 else 0) * d
        to = []
        cap = []
        head = [[] for _ in range(nnodes)]

        def add(a, b, c):
            head[a].append(len(to)); to.append(b); cap.append(c)
            head[b].append(len(to)); to.append(a); cap.append(0)

        def nid(i, k):
            # y_{i,k} = [p_i >= k]; y=1 <=> source side
            if i == 1:
                return T          # p_1 = 0  => all y_{1,k} = 0 (sink side)
            if i == N:
                return S          # p_N = d  => all y_{N,k} = 1 (source side)
            return 2 + (i - 2) * d + (k - 1)

        # monotonicity y_{i,k+1} <= y_{i,k}
        for i in range(2, N):
            for k in range(1, d):
                a = nid(i, k + 1); b = nid(i, k)
                if a != b:
                    add(a, b, INF)

        # g(x) = 1*max(0,x) + INF*max(0,x-1),  x = p_v - p_u
        for (u, v) in edges:
            for k in range(1, d + 1):
                a = nid(v, k); b = nid(u, k)
                if a != b:
                    add(a, b, 1)
            for k in range(2, d + 1):
                a = nid(v, k); b = nid(u, k - 1)
                if a != b:
                    add(a, b, INF)

        # ---- Dinic with flow limit ----
        flow = 0
        while flow < limit:
            level = [-1] * nnodes
            level[S] = 0
            q = deque([S])
            while q:
                x = q.popleft()
                for eid in head[x]:
                    if cap[eid] > 0:
                        y = to[eid]
                        if level[y] < 0:
                            level[y] = level[x] + 1
                            q.append(y)
            if level[T] < 0:
                break
            it = [0] * nnodes
            while flow < limit:
                stack = [S]
                path = []
                found = False
                while stack:
                    x = stack[-1]
                    if x == T:
                        found = True
                        break
                    hx = head[x]
                    lx = level[x] + 1
                    while it[x] < len(hx):
                        eid = hx[it[x]]
                        if cap[eid] > 0 and level[to[eid]] == lx:
                            break
                        it[x] += 1
                    if it[x] == len(hx):
                        level[x] = -1
                        stack.pop()
                        if path:
                            path.pop()
                            it[stack[-1]] += 1
                    else:
                        eid = hx[it[x]]
                        path.append(eid)
                        stack.append(to[eid])
                if not found:
                    break
                f = limit - flow
                for eid in path:
                    if cap[eid] < f:
                        f = cap[eid]
                for eid in path:
                    cap[eid] -= f
                    cap[eid ^ 1] += f
                flow += f
        return flow

    ans = 0
    hi = K if K < N - 1 else N - 1
    for d in range(hi, 0, -1):
        if min_tight(d) <= K:
            ans = d
            break
    print(ans)

main()