import sys
import heapq


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    it = iter(data)
    H = next(it)
    W = next(it)
    X = next(it)
    P = next(it) - 1
    Q = next(it) - 1

    S = [[0] * W for _ in range(H)]
    for i in range(H):
        row = S[i]
        for j in range(W):
            row[j] = next(it)

    current = S[P][Q]
    absorbed = [[False] * W for _ in range(H)]
    absorbed[P][Q] = True

    heap = []
    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))

    for dx, dy in dirs:
        nx, ny = P + dx, Q + dy
        if 0 <= nx < H and 0 <= ny < W:
            heapq.heappush(heap, (S[nx][ny], nx, ny))

    while heap:
        s, i, j = heapq.heappop(heap)
        if absorbed[i][j]:
            continue

        if s * X < current:
            current += s
            absorbed[i][j] = True

            for dx, dy in dirs:
                nx, ny = i + dx, j + dy
                if 0 <= nx < H and 0 <= ny < W and not absorbed[nx][ny]:
                    heapq.heappush(heap, (S[nx][ny], nx, ny))
        else:
            break

    print(current)


if __name__ == "__main__":
    main()