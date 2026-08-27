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
        row = [int(data[idx + j]) for j in range(W)]
        idx += W
        S.append(row)

    p = P - 1
    q = Q - 1
    T = S[p][q]

    visited = [[False] * W for _ in range(H)]
    visited[p][q] = True

    heap = []
    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))

    def push_neighbors(r, c):
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W and not visited[nr][nc]:
                visited[nr][nc] = True
                heapq.heappush(heap, (S[nr][nc], nr, nc))

    push_neighbors(p, q)

    while heap:
        s, r, c = heapq.heappop(heap)
        if s * X < T:
            T += s
            push_neighbors(r, c)
        else:
            break

    sys.stdout.write(str(T) + "\n")

solve()