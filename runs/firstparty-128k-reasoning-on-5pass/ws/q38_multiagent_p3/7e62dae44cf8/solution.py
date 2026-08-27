import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)

    H = int(next(it))
    W = int(next(it))
    X = int(next(it))
    P = int(next(it)) - 1
    Q = int(next(it)) - 1

    S = [[0] * W for _ in range(H)]
    for i in range(H):
        row = S[i]
        for j in range(W):
            row[j] = int(next(it))

    total = S[P][Q]

    seen = [bytearray(W) for _ in range(H)]
    seen[P][Q] = 1

    heap = []
    push = heapq.heappush
    pop = heapq.heappop

    if P > 0:
        seen[P - 1][Q] = 1
        push(heap, (S[P - 1][Q], P - 1, Q))
    if P + 1 < H:
        seen[P + 1][Q] = 1
        push(heap, (S[P + 1][Q], P + 1, Q))
    if Q > 0:
        seen[P][Q - 1] = 1
        push(heap, (S[P][Q - 1], P, Q - 1))
    if Q + 1 < W:
        seen[P][Q + 1] = 1
        push(heap, (S[P][Q + 1], P, Q + 1))

    while heap:
        s, r, c = pop(heap)

        if s * X >= total:
            break

        total += s

        nr = r - 1
        if nr >= 0 and not seen[nr][c]:
            seen[nr][c] = 1
            push(heap, (S[nr][c], nr, c))

        nr = r + 1
        if nr < H and not seen[nr][c]:
            seen[nr][c] = 1
            push(heap, (S[nr][c], nr, c))

        nc = c - 1
        if nc >= 0 and not seen[r][nc]:
            seen[r][nc] = 1
            push(heap, (S[r][nc], r, nc))

        nc = c + 1
        if nc < W and not seen[r][nc]:
            seen[r][nc] = 1
            push(heap, (S[r][nc], r, nc))

    print(total)

if __name__ == "__main__":
    main()