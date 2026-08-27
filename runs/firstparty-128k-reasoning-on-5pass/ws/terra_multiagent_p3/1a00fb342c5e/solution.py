import sys
from collections import deque

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    it = iter(data)
    n = next(it)
    m = next(it)

    graph = [[] for _ in range(n)]
    for _ in range(m):
        x = next(it) - 1
        y = next(it) - 1
        z = next(it)
        graph[x].append((y, z))
        graph[y].append((x, z))

    label = [-1] * n
    answer = [0] * n

    for start in range(n):
        if label[start] != -1:
            continue

        label[start] = 0
        q = deque([start])
        vertices = []
        bit_count = [0] * 30

        while q:
            v = q.popleft()
            vertices.append(v)

            value = label[v]
            for b in range(30):
                if (value >> b) & 1:
                    bit_count[b] += 1

            for to, z in graph[v]:
                expected = value ^ z
                if label[to] == -1:
                    label[to] = expected
                    q.append(to)
                elif label[to] != expected:
                    print(-1)
                    return

        size = len(vertices)
        shift = 0
        for b in range(30):
            if bit_count[b] * 2 > size:
                shift |= 1 << b

        for v in vertices:
            answer[v] = label[v] ^ shift

    print(*answer)

if __name__ == "__main__":
    main()