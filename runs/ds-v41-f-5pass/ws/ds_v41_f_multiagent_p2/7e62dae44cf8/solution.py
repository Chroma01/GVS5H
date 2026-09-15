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
    P -= 1
    Q -= 1
    S = []
    for i in range(H):
        row = data[idx:idx + W]
        idx += W
        S.append([int(x) for x in row])

    visited = [[False] * W for _ in range(H)]
    visited[P][Q] = True
    cur = S[P][Q]

    heap = []

    def push_neighbors(i, j):
        if i > 0 and not visited[i - 1][j]:
            visited[i - 1][j] = True
            heapq.heappush(heap, (S[i - 1][j], i - 1, j))
        if i + 1 < H and not visited[i + 1][j]:
            visited[i + 1][j] = True
            heapq.heappush(heap, (S[i + 1][j], i + 1, j))
        if j > 0 and not visited[i][j - 1]:
            visited[i][j - 1] = True
            heapq.heappush(heap, (S[i][j - 1], i, j - 1))
        if j + 1 < W and not visited[i][j + 1]:
            visited[i][j + 1] = True
            heapq.heappush(heap, (S[i][j + 1], i, j + 1))

    push_neighbors(P, Q)

    while heap:
        v, i, j = heapq.heappop(heap)
        if X * v < cur:
            cur += v
            push_neighbors(i, j)
        else:
            break

    sys.stdout.write(str(cur) + "\n")

main()