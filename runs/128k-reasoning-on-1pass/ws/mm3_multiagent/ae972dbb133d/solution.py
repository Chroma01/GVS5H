import sys
from collections import deque

MOD = 998244353

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    T = int(next(it))
    out_lines = []

    for _ in range(T):
        H = int(next(it))
        W = int(next(it))

        # count A's per row and per column
        row_cnt = [0] * H
        col_cnt = [0] * W

        # parity of A's in each column up to the previous row
        col_par = [0] * W

        # adjacency for the bipartite graph (rows 0..H-1, columns H..H+W-1)
        row_adj = [[] for _ in range(H)]   # row_adj[i] : list of packed (col<<1 | label)
        col_adj = [[] for _ in range(W)]   # col_adj[j] : list of packed (row<<1 | label)

        for i in range(H):
            s = next(it)          # bytes object, length W
            row_par = 0           # parity of A's in this row before current column
            for j in range(W):
                ch = s[j]        # ord('A') = 65, ord('B') = 66
                if ch == 65:     # 'A'
                    row_cnt[i] += 1
                    col_cnt[j] += 1
                    row_par ^= 1
                    col_par[j] ^= 1
                else:            # 'B'
                    # label = (row_par XOR col_par[j]) XOR 1
                    label = (row_par ^ col_par[j]) ^ 1
                    row_adj[i].append((j << 1) | label)
                    col_adj[j].append((i << 1) | label)
                    # no parity toggle for B

        # parity condition: every row and every column must contain an even number of A's
        ok = True
        for c in row_cnt:
            if c & 1:
                ok = False
                break
        if ok:
            for c in col_cnt:
                if c & 1:
                    ok = False
                    break

        if not ok:
            out_lines.append('0')
            continue

        # BFS / propagation on the bipartite graph
        N = H + W                     # total vertices
        visited = [False] * N
        val = [0] * N                 # 0/1 potentials
        components = 0
        dq = deque()

        for v in range(N):
            if visited[v]:
                continue
            components += 1
            visited[v] = True
            val[v] = 0
            dq.append(v)
            while dq and ok:
                x = dq.popleft()
                if x < H:            # row vertex
                    i = x
                    for packed in row_adj[i]:
                        col = packed >> 1
                        lab = packed & 1
                        y = H + col
                        need = val[x] ^ lab
                        if not visited[y]:
                            visited[y] = True
                            val[y] = need
                            dq.append(y)
                        elif val[y] != need:
                            ok = False
                            break
                else:                # column vertex
                    col = x - H
                    for packed in col_adj[col]:
                        row_i = packed >> 1
                        lab = packed & 1
                        y = row_i
                        need = val[x] ^ lab
                        if not visited[y]:
                            visited[y] = True
                            val[y] = need
                            dq.append(y)
                        elif val[y] != need:
                            ok = False
                            break

        if not ok:
            out_lines.append('0')
        else:
            out_lines.append(str(pow(2, components, MOD)))

    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    solve()