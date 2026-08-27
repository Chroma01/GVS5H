import sys
from collections import deque


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m = data[0], data[1]
    graph = [[] for _ in range(n)]
    pos = 2

    for _ in range(m):
        x, y, z = data[pos] - 1, data[pos + 1] - 1, data[pos + 2]
        pos += 3
        graph[x].append((y, z))
        graph[y].append((x, z))

    relative = [-1] * n
    answer = [0] * n

    for start in range(n):
        if relative[start] != -1:
            continue

        relative[start] = 0
        queue = deque([start])
        vertices = []

        while queue:
            v = queue.popleft()
            vertices.append(v)

            for to, z in graph[v]:
                expected = relative[v] ^ z
                if relative[to] == -1:
                    relative[to] = expected
                    queue.append(to)
                elif relative[to] != expected:
                    print(-1)
                    return

        offset = 0
        size = len(vertices)

        for bit in range(30):
            ones = 0
            mask = 1 << bit
            for v in vertices:
                if relative[v] & mask:
                    ones += 1

            zeros = size - ones
            if zeros < ones:
                offset |= mask

        for v in vertices:
            answer[v] = relative[v] ^ offset

    print(*answer)


if __name__ == "__main__":
    solve()