import sys
import heapq


def solve():
    input = sys.stdin.buffer.readline

    H, W, X = map(int, input().split())
    P, Q = map(int, input().split())
    P -= 1
    Q -= 1

    strengths = []
    for _ in range(H):
        strengths.extend(map(int, input().split()))

    start = P * W + Q
    current = strengths[start]

    visited = bytearray(H * W)
    visited[start] = 1

    heap = []

    def add_neighbor(r, c):
        if 0 <= r < H and 0 <= c < W:
            idx = r * W + c
            if not visited[idx]:
                visited[idx] = 1
                heapq.heappush(heap, (strengths[idx], idx))

    add_neighbor(P - 1, Q)
    add_neighbor(P + 1, Q)
    add_neighbor(P, Q - 1)
    add_neighbor(P, Q + 1)

    while heap and heap[0][0] * X < current:
        value, idx = heapq.heappop(heap)
        current += value

        r, c = divmod(idx, W)
        add_neighbor(r - 1, c)
        add_neighbor(r + 1, c)
        add_neighbor(r, c - 1)
        add_neighbor(r, c + 1)

    print(current)


if __name__ == "__main__":
    solve()