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
        row = [int(x) for x in data[idx:idx + W]]
        idx += W
        S.append(row)

    cur = S[P][Q]
    visited = [[False] * W for _ in range(H)]
    visited[P][Q] = True

    heap = []
    for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        ni, nj = P + di, Q + dj
        if 0 <= ni < H and 0 <= nj < W and not visited[ni][nj]:
            visited[ni][nj] = True
            heapq.heappush(heap, (S[ni][nj], ni, nj))

    while heap:
        s, i, j = heapq.heappop(heap)
        if s * X < cur:
            cur += s
            for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                ni, nj = i + di, j + dj
                if 0 <= ni < H and 0 <= nj < W and not visited[ni][nj]:
                    visited[ni][nj] = True
                    heapq.heappush(heap, (S[ni][nj], ni, nj))
        else:
            # smallest frontier slime is not absorbable -> none are
            break

    print(cur)

main()