import sys


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

    potential = [-1] * n
    answer = [0] * n
    bit_count = 30

    for start in range(n):
        if potential[start] != -1:
            continue

        potential[start] = 0
        stack = [start]
        component = []

        while stack:
            u = stack.pop()
            component.append(u)

            for v, z in graph[u]:
                expected = potential[u] ^ z
                if potential[v] == -1:
                    potential[v] = expected
                    stack.append(v)
                elif potential[v] != expected:
                    print(-1)
                    return

        ones = [0] * bit_count
        for v in component:
            value = potential[v]
            for bit in range(bit_count):
                ones[bit] += (value >> bit) & 1

        offset = 0
        size = len(component)
        for bit in range(bit_count):
            if ones[bit] > size - ones[bit]:
                offset |= 1 << bit

        for v in component:
            answer[v] = potential[v] ^ offset

    print(*answer)


if __name__ == "__main__":
    solve()