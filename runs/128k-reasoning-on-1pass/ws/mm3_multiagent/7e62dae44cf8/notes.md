
## ideation
```python
import sys
import heapq

def solve():
    input = sys.stdin.readline
    H, W, X = map(int, input().split())
    P, Q = map(int, input().split())
    P -= 1
    Q -= 1
    grid = [list(map(int, input().split())) for _ in range(H)]
    total = grid[P][Q]
    visited = [[False] * W for _ in range(H)]
    visited[P][Q] = True
    heap = []
    # initial frontier
    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ni, nj = P + di, Q + dj
        if 0 <= ni < H and 0 <= nj < W and not visited[ni][nj]:
            heapq.heappush(heap, (grid[ni][nj], ni, nj))
    while heap:
        s, i, j = heapq.heappop(heap)
        if visited[i][j]:
            continue
        # if s * X >= total, cannot absorb this or any larger frontier cell
        if s * X >= total:
            break
        # absorb
        total += s
        visited[i][j] = True
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < H and 0 <= nj < W and not visited[ni][nj]:
                heapq.heappush(heap, (grid[ni][nj], ni, nj))
    print(total)

if __name__ == "__main__":
    solve()
```

## worker: finalize
We treat the set of already absorbed cells as a connected region.  
A neighboring slime with strength \(s\) can be absorbed exactly when  

\[
s < \frac{\text{total}}{X} \quad\Longleftrightarrow\quad s\cdot X < \text{total}.
\]

Because the condition is monotone in \(s\) (a smaller strength is easier to satisfy), if any neighbor is absorbable then the neighbor with the smallest strength is also absorbable. Therefore we can always process the frontier in increasing order of strength.  
A min‑heap stores all frontier cells. We repeatedly extract the smallest strength cell; if it fails the condition we stop (no further absorption is possible). Otherwise we absorb it, add its strength to the current total, mark it visited, and push its four neighbours onto the heap. The algorithm ends when the heap is empty or its top does not satisfy the condition.  

**Correctness**: The monotone property guarantees that absorbing cells in non‑decreasing order never blocks a possible absorption. If a cell can be absorbed at any moment, the smallest frontier cell is also absorbable, so the greedy choice is safe. The process stops only when no frontier cell satisfies the inequality, which is exactly when no further absorption is possible. Hence the final total is the maximum achievable strength.
