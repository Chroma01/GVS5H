import sys
import heapq


def main() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    h = next(it)
    w = next(it)
    x = next(it)
    p = next(it) - 1
    q = next(it) - 1

    strength = [next(it) for _ in range(h * w)]

    start = p * w + q
    current = strength[start]

    visited = bytearray(h * w)
    visited[start] = 1
    heap = []

    def add_neighbor(idx: int) -> None:
        if not visited[idx]:
            visited[idx] = 1
            heapq.heappush(heap, (strength[idx], idx))

    if p > 0:
        add_neighbor(start - w)
    if p + 1 < h:
        add_neighbor(start + w)
    if q > 0:
        add_neighbor(start - 1)
    if q + 1 < w:
        add_neighbor(start + 1)

    while heap and heap[0][0] * x < current:
        value, pos = heapq.heappop(heap)
        current += value

        row = pos // w
        col = pos - row * w

        if row > 0:
            add_neighbor(pos - w)
        if row + 1 < h:
            add_neighbor(pos + w)
        if col > 0:
            add_neighbor(pos - 1)
        if col + 1 < w:
            add_neighbor(pos + 1)

    print(current)


if __name__ == "__main__":
    main()