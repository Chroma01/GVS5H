import sys
import heapq


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    H = next(it)
    W = next(it)
    X = next(it)
    P = next(it) - 1
    Q = next(it) - 1

    n = H * W
    values = [next(it) for _ in range(n)]

    start = P * W + Q
    strength = values[start]

    seen = bytearray(n)
    seen[start] = 1
    heap = []

    def add_neighbors(index):
        r, c = divmod(index, W)
        if r > 0:
            ni = index - W
            if not seen[ni]:
                seen[ni] = 1
                heapq.heappush(heap, (values[ni], ni))
        if r + 1 < H:
            ni = index + W
            if not seen[ni]:
                seen[ni] = 1
                heapq.heappush(heap, (values[ni], ni))
        if c > 0:
            ni = index - 1
            if not seen[ni]:
                seen[ni] = 1
                heapq.heappush(heap, (values[ni], ni))
        if c + 1 < W:
            ni = index + 1
            if not seen[ni]:
                seen[ni] = 1
                heapq.heappush(heap, (values[ni], ni))

    add_neighbors(start)

    while heap:
        value, index = heap[0]
        if value * X >= strength:
            break
        heapq.heappop(heap)
        strength += value
        add_neighbors(index)

    print(strength)


if __name__ == "__main__":
    solve()