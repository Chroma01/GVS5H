
## ideation
**Solution (Python 3)**

```python
import sys
from collections import deque

def solve() -> None:
    input = sys.stdin.readline
    N = int(input())
    # out[u][c] : destinations of edges u -> * with label c (c = 0..25)
    out_adj = [[ [] for _ in range(26) ] for _ in range(N)]
    # inc[u][c] : sources of edges * -> u with label c
    inc_adj = [[ [] for _ in range(26) ] for _ in range(N)]

    for i in range(N):
        row = input().strip()
        for j, ch in enumerate(row):
            if ch != '-':
                c = ord(ch) - 97
                out_adj[i][c].append(j)
                inc_adj[j][c].append(i)

    INF = 10 ** 9
    dist = [ [ INF ] * N for _ in range(N) ]

    # distance 0 : empty walk
    for i in range(N):
        dist[i][i] = 0

    # distance 1 : direct edges
    for i in range(N):
        for c in range(26):
            for j in out_adj[i][c]:
                if dist[i][j] > 1:
                    dist[i][j] = 1

    q = deque()
    for i in range(N):
        for j in range(N):
            if dist[i][j] != INF:
                q.append((i, j))

    while q:
        u, v = q.popleft()
        cur = dist[u][v]
        nd = cur + 2
        inc_u = inc_adj[u]
        out_v = out_adj[v]
        for c in range(26):
            pre = inc_u[c]          # vertices x with edge x -> u (label c)
            nxt = out_v[c]          # vertices y with edge v -> y (label c)
            if not pre or not nxt:
                continue
            for x in pre:
                # try all y that share the same label
                for y in nxt:
                    if dist[x][y] > nd:
                        dist[x][y] = nd
                        q.append((x, y))

    out_lines = []
    for i in range(N):
        row = []
        for j in range(N):
            val = dist[i][j]
            row.append(str(val) if val != INF else "-1")
        out_lines.append(" ".join(row))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
```

## worker: finalize
- The problem asks for the length of the shortest walk (possibly non‑simple) whose edge‑label string is a palindrome.
- The empty walk is a palindrome, therefore `dist[i][i] = 0`.  
  Any single edge `i → j` gives a palindrome of length 1, so `dist[i][j] = 1` for every existing edge.
- For any palindrome walk `i … j` of length ≥ 2 the first and last labels are equal. Removing them yields a shorter palindrome walk. Conversely, given a palindrome walk from `u` to `v` we can prepend an edge `x → u` and append an edge `v → y` **with the same label** to obtain a longer palindrome walk from `x` to `y` whose length is `+2`.
- Hence we build a state graph whose vertices are ordered pairs `(u, v)`.  
  From a state `(u, v)` with current distance `d` we can go to any `(x, y)` such that there are edges `x → u` and `v → y` both labelled by the same letter `c`. The transition weight is always `2`.
- All transitions have positive weight, so a normal BFS over the state graph visits states in non‑decreasing order of the answer. The first time we reach a pair `(i, j)` we have the minimal possible length. Initial states are all `(i,i)` (distance 0) and all `(i,j)` with a direct edge (distance 1).
- The BFS runs in `O(N⁴)` time in the worst case (each of the `N²` states may examine all pairs of incoming/outgoing edges for each of the 26 letters), which is fast enough for `N ≤ 100`. Memory consumption is `O(N²)`.
