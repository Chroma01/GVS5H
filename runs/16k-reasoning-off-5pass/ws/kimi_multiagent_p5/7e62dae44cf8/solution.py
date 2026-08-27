import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    H = int(data[idx]); idx += 1
    W = int(data[idx]); idx += 1
    X = int(data[idx]); idx += 1
    P = int(data[idx]); idx += 1
    Q = int(data[idx]); idx += 1
    # Read grid
    S = []
    for _ in range(H):
        row = [int(data[idx + j]) for j in range(W)]
        idx += W
        S.append(row)

    # Convert to 0-indexed
    sr, sc = P - 1, Q - 1
    cur = S[sr][sc]

    visited = [[False] * W for _ in range(H)]
    visited[sr][sc] = True

    # Min-heap of frontier slimes keyed by strength
    heap = []
    def push_neighbors(r, c):
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W and not visited[nr][nc]:
                visited[nr][nc] = True
                heapq.heappush(heap, (S[nr][nc], nr, nc))

    push_neighbors(sr, sc)

    # Greedy: always absorb the weakest frontier slime if possible.
    # Since cur only increases, absorbing whenever possible never hurts.
    while heap:
        s, r, c = heapq.heappop(heap)
        # Condition: s < cur / X  <=>  cur > X * s
        if cur > X * s:
            cur += s
            push_neighbors(r, c)
        else:
            # Weakest frontier slime is not absorbable; none are.
            break

    print(cur)

main()