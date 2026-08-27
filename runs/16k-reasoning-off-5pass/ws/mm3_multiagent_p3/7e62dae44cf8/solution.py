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
    
    S = []
    for _ in range(H):
        row = [int(next(it)) for _ in range(W)]
        S.append(row)
    
    visited = [[False] * W for _ in range(H)]
    visited[P][Q] = True
    cur = S[P][Q]
    
    pq = []
    # Push initial neighbors
    for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
        ni, nj = P + di, Q + dj
        if 0 <= ni < H and 0 <= nj < W:
            if not visited[ni][nj]:
                heapq.heappush(pq, (S[ni][nj], ni, nj))
    
    while pq:
        s, i, j = heapq.heappop(pq)
        if visited[i][j]:
            continue
        # Check condition: s * X < cur
        if s * X < cur:
            visited[i][j] = True
            cur += s
            for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < H and 0 <= nj < W and not visited[ni][nj]:
                    heapq.heappush(pq, (S[ni][nj], ni, nj))
        else:
            # Since heap is min-heap, this s is the smallest.
            # If it can't be absorbed, none can. Put it back? Actually we can just break.
            # But to be safe and not lose it (though we break anyway), we could push back.
            # However, once we break, we stop processing. Since larger ones also fail, it's fine.
            break
    
    print(cur)

if __name__ == "__main__":
    solve()