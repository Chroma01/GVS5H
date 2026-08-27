import sys
import heapq

def solve() -> None:
    it = iter(sys.stdin.read().split())
    H = int(next(it))
    W = int(next(it))
    X = int(next(it))
    P = int(next(it)) - 1
    Q = int(next(it)) - 1
    grid = [[0] * W for _ in range(H)]
    for i in range(H):
        for j in range(W):
            grid[i][j] = int(next(it))
    # visited marks cells whose slime has been absorbed (or starting cell)
    visited = [[False] * W for _ in range(H)]
    # max-heap via negative strengths
    heap = []
    cur = grid[P][Q]
    visited[P][Q] = True
    # push initial neighbors
    for di, dj in ((-1,0),(1,0),(0,-1),(0,1)):
        ni, nj = P+di, Q+dj
        if 0 <= ni < H and 0 <= nj < W and not visited[ni][nj]:
            heapq.heappush(heap, (-grid[ni][nj], ni, nj))
    # process
    while heap:
        neg_s, i, j = heapq.heappop(heap)
        if visited[i][j]:
            continue
        s = -neg_s
        # condition: s * X < cur  (strictly less than cur / X)
        if s * X >= cur:
            # cannot absorb now; push back? We could just skip, but we might need it later.
            # Since cur only increases, we can keep it in heap; but to avoid infinite loop we just skip and not push back.
            # However, if we skip, we may lose the ability to check it again when cur grows.
            # Better: keep it in heap, but we must allow it to be reconsidered.
            # We'll push it back to maintain presence.
            heapq.heappush(heap, (neg_s, i, j))
            break  # all remaining items have strength <= current max not absorbable, but we might have smaller ones that are absorbable? No, because heap is max-heap; if top is not absorbable, no other is.
        # absorb
        cur += s
        visited[i][j] = True
        # push its neighbors
        for di, dj in ((-1,0),(1,0),(0,-1),(0,1)):
            ni, nj = i+di, j+dj
            if 0 <= ni < H and 0 <= nj < W and not visited[ni][nj]:
                heapq.heappush(heap, (-grid[ni][nj], ni, nj))
    print(cur)

if __name__ == "__main__":
    solve()