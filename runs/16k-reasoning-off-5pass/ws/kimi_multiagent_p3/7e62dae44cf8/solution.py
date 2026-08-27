import sys
import heapq

def solve():
    data = sys.stdin.buffer.read().split()
    idx = 0
    H = int(data[idx]); idx += 1
    W = int(data[idx]); idx += 1
    X = int(data[idx]); idx += 1
    P = int(data[idx]); idx += 1
    Q = int(data[idx]); idx += 1

    S = []
    for i in range(H):
        row = [int(x) for x in data[idx:idx + W]]
        idx += W
        S.append(row)

    cur = S[P - 1][Q - 1]
    visited = [[False] * W for _ in range(H)]
    visited[P - 1][Q - 1] = True

    heap = []
    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))

    def push_neighbors(i, j):
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < H and 0 <= nj < W and not visited[ni][nj]:
                visited[ni][nj] = True
                heapq.heappush(heap, (S[ni][nj], ni, nj))

    push_neighbors(P - 1, Q - 1)

    while heap:
        s, i, j = heapq.heappop(heap)
        if s * X < cur:
            cur += s
            push_neighbors(i, j)
        else:
            break

    print(cur)

solve()