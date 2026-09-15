import sys
import heapq

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    H, W, X = data[0], data[1], data[2]
    P, Q = data[3] - 1, data[4] - 1
    idx = 5
    S = []
    for i in range(H):
        S.append(data[idx:idx+W])
        idx += W

    visited = [[False] * W for _ in range(H)]
    visited[P][Q] = True
    current = S[P][Q]
    heap = []
    dirs = ((-1, 0), (1, 0), (0, -1), (0, 1))

    for dr, dc in dirs:
        nr, nc = P + dr, Q + dc
        if 0 <= nr < H and 0 <= nc < W and not visited[nr][nc]:
            visited[nr][nc] = True
            heapq.heappush(heap, (S[nr][nc], nr, nc))

    while heap:
        s, r, c = heapq.heappop(heap)
        if s * X < current:
            current += s
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W and not visited[nr][nc]:
                    visited[nr][nc] = True
                    heapq.heappush(heap, (S[nr][nc], nr, nc))
        else:
            break

    print(current)

if __name__ == "__main__":
    main()