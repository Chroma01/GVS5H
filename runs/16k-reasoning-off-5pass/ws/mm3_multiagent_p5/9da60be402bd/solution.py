import sys
from collections import deque

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    grid = data[1:]
    # grid[i] is the i-th row string (length N)
    # Build outgoing and incoming adjacency lists grouped by label (0..25)
    out = [[[] for _ in range(26)] for _ in range(N)]
    inc = [[[] for _ in range(26)] for _ in range(N)]
    # Also a boolean matrix for odd targets (edge u->v exists)
    has_edge = [[False]*N for _ in range(N)]
    for i in range(N):
        row = grid[i]
        for j in range(N):
            ch = row[j]
            if ch != '-':
                lbl = ord(ch) - ord('a')
                out[i][lbl].append(j)
                inc[j][lbl].append(i)
                has_edge[i][j] = True
    # BFS on reverse product graph
    # State: (u, v) encoded as u*N + v
    # Distance arrays: -1 means unvisited
    def bfs_reverse(targets):
        dist = [-1] * (N * N)
        dq = deque()
        for (u, v) in targets:
            idx = u * N + v
            if dist[idx] == -1:
                dist[idx] = 0
                dq.append(idx)
        while dq:
            state = dq.popleft()
            d = dist[state]
            u = state // N
            v = state % N
            # For each label L, match incoming edges to u and incoming edges to v
            # Note: reverse step uses inc[u][L] and inc[v][L]
            inc_u = inc[u]
            inc_v = inc[v]
            for L in range(26):
                list_u = inc_u[L]
                if not list_u:
                    continue
                list_v = inc_v[L]
                if not list_v:
                    continue
                for u_prev in list_u:
                    base = u_prev * N
                    for v_prev in list_v:
                        nxt = base + v_prev
                        if dist[nxt] == -1:
                            dist[nxt] = d + 1
                            dq.append(nxt)
        return dist
    # Even targets: all (u, u)
    even_targets = [(u, u) for u in range(N)]
    # Odd targets: all (u, v) where has_edge[u][v] is True
    odd_targets = []
    for u in range(N):
        for v in range(N):
            if has_edge[u][v]:
                odd_targets.append((u, v))
    dist_even = bfs_reverse(even_targets)
    dist_odd = bfs_reverse(odd_targets)
    # Compute answers
    out_lines = []
    INF = 10**9
    for i in range(N):
        row_ans = []
        base_i = i * N
        for j in range(N):
            if i == j:
                row_ans.append('0')
                continue
            d_e = dist_even[base_i + j]
            d_o = dist_odd[base_i + j]
            best = INF
            if d_e != -1:
                val = 2 * d_e
                if val < best:
                    best = val
            if d_o != -1:
                val = 2 * d_o + 1
                if val < best:
                    best = val
            if best == INF:
                row_ans.append('-1')
            else:
                row_ans.append(str(best))
        out_lines.append(' '.join(row_ans))
    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    solve()