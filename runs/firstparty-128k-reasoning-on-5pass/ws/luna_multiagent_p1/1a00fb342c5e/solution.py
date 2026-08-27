import sys


def solve():
    input = sys.stdin.buffer.readline
    n, m = map(int, input().split())

    graph = [[] for _ in range(n)]
    for _ in range(m):
        x, y, z = map(int, input().split())
        x -= 1
        y -= 1
        graph[x].append((y, z))
        graph[y].append((x, z))

    potential = [-1] * n
    answer = [0] * n

    for start in range(n):
        if potential[start] != -1:
            continue

        potential[start] = 0
        stack = [start]
        component = []

        while stack:
            v = stack.pop()
            component.append(v)

            for to, z in graph[v]:
                expected = potential[v] ^ z
                if potential[to] == -1:
                    potential[to] = expected
                    stack.append(to)
                elif potential[to] != expected:
                    print(-1)
                    return

        offset = 0
        size = len(component)

        for bit in range(30):
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