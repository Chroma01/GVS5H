import sys
import heapq

def solve():
    data = sys.stdin.read().split()
    it = iter(data)
    H = int(next(it))
    W = int(next(it))
    X = int(next(it))
    P = int(next(it)) - 1
    Q = int(next(it)) - 1
    grid = []
    for _ in range(H):
        row = [int(next(it)) for _ in range(W)]
        grid.append(row)
    
    visited = [[False] * W for _ in range(H)]
    # max-heap: store negative strengths to simulate max-heap
    heap = []
    current = grid[P][Q]
    visited[P][Q] = True
    # push initial neighbors
    for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
        ni, nj = P+di, Q+dj
        if 0 <= ni < H and 0 <= nj < W and not visited[ni][nj]:
            heapq.heappush(heap, -grid[ni][nj])
            visited[ni][nj] = True  # mark as queued to avoid duplicates? careful
    # Actually we need to handle duplicates differently: we should not mark visited for cells in heap until we absorb them,
    # because we need to be able to re-evaluate if they become absorbable later? No, condition depends only on current strength.
    # If a cell is in heap, it means it has been discovered as adjacent. We can mark it as "seen" to avoid pushing again.
    # When we pop, if it is absorbable we absorb and then mark visited; otherwise we ignore.
    # But if we mark visited when pushing to heap, we need to ensure that if we don't absorb it (because condition fails),
    # we might still need to consider it later if we become stronger? Actually once condition fails for a cell with strength s,
    # it will fail forever because current only grows. So we can safely discard it.
    # So marking visited when pushing is fine.
    
    # Reset visited marking: we should not mark visited when pushing, because we might push a cell multiple times from different parents.
    # Let's do standard BFS: use a separate "in_heap" or simply push and check visited when popping.
    # Better: when popping, check if already visited; if not, and absorbable, absorb and mark visited, then push its neighbors.
    # We need to ensure we don't push the same cell multiple times. We'll use a 'discovered' set.
    
    # Restart with correct approach
    visited = [[False] * W for _ in range(H)]
    visited[P][Q] = True
    heap = []
    for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
        ni, nj = P+di, Q+dj
        if 0 <= ni < H and 0 <= nj < W and not visited[ni][nj]:
            visited[ni][nj] = True
            heapq.heappush(heap, -grid[ni][nj])
    
    while heap:
        s = -heapq.heappop(heap)
        if s * X < current:
            current += s
            # find the cell with this strength? We don't know coordinates.
            # We need to store coordinates as well to know which cell to expand.
            # So heap entries should be (strength, i, j) with negative strength.
            # But we already popped s without coordinates. This is a bug.
            # We need to store (i,j) as well.
            # Let's restart properly.
            pass
        else:
            break
    # Since we realized the flaw, let's write the correct version.
    print(current)

# Let's write a correct version directly
def solve():
    data = sys.stdin.read().split()
    it = iter(data)
    H = int(next(it))
    W = int(next(it))
    X = int(next(it))
    P = int(next(it)) - 1
    Q = int(next(it)) - 1
    grid = []
    for _ in range(H):
        row = [int(next(it)) for _ in range(W)]
        grid.append(row)
    
    visited = [[False] * W for _ in range(H)]
    visited[P][Q] = True
    # heap entries: (-strength, i, j)
    heap = []
    for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
        ni, nj = P+di, Q+dj
        if 0 <= ni < H and 0 <= nj < W and not visited[ni][nj]:
            visited[ni][nj] = True
            heapq.heappush(heap, (-grid[ni][nj], ni, nj))
    
    current = grid[P][Q]
    
    while heap:
        neg_s, i, j = heapq.heappop(heap)
        s = -neg_s
        if s * X < current:
            current += s
            # mark as absorbed (already marked visited when pushed, but we can re-mark)
            # expand territory
            for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                ni, nj = i+di, j+dj
                if 0 <= ni < H and 0 <= nj < W and not visited[ni][nj]:
                    visited[ni][nj] = True
                    heapq.heappush(heap, (-grid[ni][nj], ni, nj))
        else:
            # not absorbable, and since we always pick the max, no further absorptions possible
            break
    
    print(current)

if __name__ == "__main__":
    solve()