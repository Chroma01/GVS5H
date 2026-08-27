import sys
from collections import deque

INF = 10**18


def compute_answer(N, adj, S, T):
    # BFS from S: shortest distance d and one shortest S-T path P.
    dist = [-1] * N
    parent = [-1] * N
    dq = deque([S])
    dist[S] = 0
    while dq:
        u = dq.popleft()
        nd = dist[u] + 1
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = nd
                parent[v] = u
                dq.append(v)

    d = dist[T]

    inP = [False] * N
    cur = T
    while True:
        inP[cur] = True
        if cur == S:
            break
        cur = parent[cur]

    # E1: minimum excess of an S-T walk that uses an off-P vertex
    # and does not visit the opposite endpoint early.
    def bfs_banned(start, banned):
        dist = [-1] * N
        dist[start] = 0
        dq = deque([start])
        while dq:
            u = dq.popleft()
            nd = dist[u] + 1
            for v in adj[u]:
                if v == banned or dist[v] != -1:
                    continue
                dist[v] = nd
                dq.append(v)
        return dist

    dist1 = bfs_banned(S, T)
    dist2 = bfs_banned(T, S)

    best = INF
    for v in range(N):
        if not inP[v]:
            a = dist1[v]
            b = dist2[v]
            if a != -1 and b != -1:
                s = a + b
                if s < best:
                    best = s

    e1 = best - d if best != INF else INF
    if e1 < 0:
        e1 = 0

    # If there is another shortest S-T path, the lower bound is attainable.
    if e1 == 0:
        return 2 * d

    # E2: endpoint buffer/branch rule.
    # For endpoint e, BFS in the graph where all P-vertices except e are banned.
    # If a reached vertex x has at least two BFS children, it can serve as a
    # passing gadget at distance r = dist[x], with excess 4*r + 4.
    e2 = INF
    for e in (S, T):
        distE = [-1] * N
        distE[e] = 0
        dq = deque([e])
        while dq:
            u = dq.popleft()
            nd = distE[u] + 1
            for v in adj[u]:
                if inP[v] and v != e:
                    continue
                if distE[v] == -1:
                    distE[v] = nd
                    dq.append(v)

        for u in range(N):
            du = distE[u]
            if du == -1:
                continue
            cnt = 0
            for v in adj[u]:
                if inP[v] and v != e:
                    continue
                if distE[v] == du + 1:
                    cnt += 1
                    if cnt >= 2:
                        break
            if cnt >= 2:
                val = 4 * du + 4
                if val < e2:
                    e2 = val
                    if e2 == 4:
                        break

        if e2 == 4:
            break

    excess = e1 if e1 < e2 else e2
    if excess >= INF:
        return -1
    return 2 * d + excess


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M, S, T = data[0], data[1], data[2] - 1, data[3] - 1
    adj = [[] for _ in range(N)]
    idx = 4
    for _ in range(M):
        u = data[idx] - 1
        v = data[idx + 1] - 1
        idx += 2
        adj[u].append(v)
        adj[v].append(u)

    print(compute_answer(N, adj, S, T))


# Optional stress test:
#   python program.py stress
def is_connected(N, adj):
    seen = [False] * N
    seen[0] = True
    dq = deque([0])
    while dq:
        u = dq.popleft()
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                dq.append(v)
    return all(seen)


def build_trans(N, adj):
    trans = [[] for _ in range(N * N)]
    for a in range(N):
        for b in range(N):
            if a == b:
                continue
            st = a * N + b
            for na in adj[a]:
                if na != b:
                    trans[st].append(na * N + b)
            for nb in adj[b]:
                if nb != a:
                    trans[st].append(a * N + nb)
    return trans


def exact_bfs(trans, start, goal):
    n = len(trans)
    dist = [-1] * n
    dq = deque([start])
    dist[start] = 0
    while dq:
        st = dq.popleft()
        if st == goal:
            return dist[st]
        nd = dist[st] + 1
        for ns in trans[st]:
            if dist[ns] == -1:
                dist[ns] = nd
                dq.append(ns)
    return -1


def stress():
    # All connected simple graphs up to N=6, all S,T pairs.
    for N in range(2, 7):
        edge_list = [(i, j) for i in range(N) for j in range(i + 1, N)]
        E = len(edge_list)
        pairs = [(i, j) for i in range(N) for j in range(i + 1, N)]

        for mask in range(1 << E):
            adj = [[] for _ in range(N)]
            for idx, (u, v) in enumerate(edge_list):
                if (mask >> idx) & 1:
                    adj[u].append(v)
                    adj[v].append(u)

            if not is_connected(N, adj):
                continue

            trans = build_trans(N, adj)
            for S, T in pairs:
                exact = exact_bfs(trans, S * N + T, T * N + S)
                ans = compute_answer(N, adj, S, T)
                ans_rev = compute_answer(N, adj, T, S)
                if ans != exact or ans_rev != exact:
                    print(
                        f"MISMATCH N={N} mask={mask} S={S + 1} T={T + 1} "
                        f"ans={ans} ans_rev={ans_rev} exact={exact}"
                    )
                    return

    # Random connected graphs with N=8.
    import random
    random.seed(12345)

    for _ in range(200):
        N = 8
        adj = [[] for _ in range(N)]

        order = list(range(N))
        random.shuffle(order)
        for i in range(1, N):
            u = order[i]
            v = order[random.randrange(i)]
            adj[u].append(v)
            adj[v].append(u)

        for u in range(N):
            for v in range(u + 1, N):
                if random.random() < 0.25:
                    if v not in adj[u]:
                        adj[u].append(v)
                        adj[v].append(u)

        trans = build_trans(N, adj)
        for S in range(N):
            for T in range(S + 1, N):
                exact = exact_bfs(trans, S * N + T, T * N + S)
                ans = compute_answer(N, adj, S, T)
                ans_rev = compute_answer(N, adj, T, S)
                if ans != exact or ans_rev != exact:
                    print(
                        f"MISMATCH random N={N} S={S + 1} T={T + 1} "
                        f"ans={ans} ans_rev={ans_rev} exact={exact}"
                    )
                    return

    print("STRESS OK")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stress":
        stress()
    else:
        main()