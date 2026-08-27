import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m = data[0], data[1]
    graph = [[] for _ in range(n)]
    max_bits = 0

    pos = 2
    for _ in range(m):
        x = data[pos] - 1
        y = data[pos + 1] - 1
        z = data[pos + 2]
        pos += 3

        graph[x].append((y, z))
        graph[y].append((x, z))
        if z:
            max_bits = max(max_bits, z.bit_length())

    potential = [0] * n
    visited = [False] * n
    answer = [0] * n

    for start in range(n):
        if visited[start]:
            continue

        visited[start] = True
        potential[start] = 0
        stack = [start]
        component = []

        while stack:
            v = stack.pop()
            component.append(v)

            for to, z in graph[v]:
                expected = potential[v] ^ z
                if not visited[to]:
                    visited[to] = True
                    potential[to] = expected
                    stack.append(to)
                elif potential[to] != expected:
                    print(-1)
                    return

        offset = 0
        size = len(component)

        for bit in range(max_bits):
            ones = 0
            mask = 1 << bit
            for v in component:
                if potential[v] & mask:
                    ones += 1

            if ones > size - ones:
                offset |= mask

        for v in component:
            answer[v] = potential[v] ^ offset

    print(*answer)


if __name__ == "__main__":
    solve()