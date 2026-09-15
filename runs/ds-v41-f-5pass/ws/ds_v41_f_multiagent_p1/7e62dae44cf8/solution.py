import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    H = int(data[idx]); idx += 1
    W = int(data[idx]); idx += 1
    X = int(data[idx]); idx += 1
    P = int(data[idx]) - 1; idx += 1
    Q = int(data[idx]) - 1; idx += 1

    S = []
    for i in range(H):
        row = data[idx:idx + W]
        idx += W
        S.append([int(v) for v in row])

    visited = [[False] * W for _ in range(H)]
    current = S[P][Q]
    visited[P][Q] = True

    heap = []
    # push initial neighbors
    if P > 0:
        heapq.heappush(heap, (S[P - 1][Q], P - 1, Q))
    if P < H - 1:
        heapq.heappush(heap, (S[P + 1][Q], P + 1, Q))
    if Q > 0:
        heapq.heappush(heap, (S[P][Q - 1], P, Q - 1))
    if Q < W - 1:
        heapq.heappush(heap, (S[P][Q + 1], P, Q + 1))

    while heap:
        val, r, c = heap[0]
        if val * X < current:
            heapq.heappop(heap)
            if visited[r][c]:
                continue
            visited[r][c] = True
            current += val
            if r > 0 and not visited[r - 1][c]:
                heapq.heappush(heap, (S[r - 1][c], r - 1, c))
            if r < H - 1 and not visited[r + 1][c]:
                heapq.heappush(heap, (S[r + 1][c], r + 1, c))
            if c > 0 and not visited[r][c - 1]:
                heapq.heappush(heap, (S[r][c - 1], r, c - 1))
            if c < W - 1 and not visited[r][c + 1]:
                heapq.heappush(heap, (S[r][c + 1], r, c + 1))
        else:
            break

    print(current)

main()