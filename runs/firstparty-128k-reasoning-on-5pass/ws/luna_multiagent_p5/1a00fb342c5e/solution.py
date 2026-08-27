import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    n = int(next(it))
    m = int(next(it))

    graph = [[] for _ in range(n)]
    max_z = 0

    for _ in range(m):
        x = int(next(it)) - 1
        y = int(next(it)) - 1
        z = int(next(it))
        graph[x].append((y, z))
        graph[y].append((x, z))
        if z > max_z:
            max_z = z

    potential = [-1] * n
    answer = [0] * n
    bits = max_z.bit_length()

    for start in range(n):
        if potential[start] != -1:
            continue

        potential[start] = 0
        stack = [start]
        vertices = []

        while stack:
            v = stack.pop()
            vertices.append(v)

            for to, z in graph[v]:
                expected = potential[v] ^ z
                if potential[to] == -1:
                    potential[to] = expected
                    stack.append(to)
                elif potential[to] != expected:
                    print(-1)
                    return

        counts = [0] * bits
        for v in vertices:
            value = potential[v]
            for b in range(bits):
                counts[b] += (value >> b) & 1

        offset = 0
        size = len(vertices)
        for b in range(bits):
            if counts[b] * 2 > size:
                offset |= 1 << b

        for v in vertices:
            answer[v] = potential[v] ^ offset

    print(*answer)


if __name__ == "__main__":
    solve()