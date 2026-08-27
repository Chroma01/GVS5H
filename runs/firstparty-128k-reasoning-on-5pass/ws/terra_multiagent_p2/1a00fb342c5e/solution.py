import sys


def solve():
    input = sys.stdin.buffer.readline
    N, M = map(int, input().split())

    graph = [[] for _ in range(N)]
    for _ in range(M):
        x, y, z = map(int, input().split())
        x -= 1
        y -= 1
        graph[x].append((y, z))
        graph[y].append((x, z))

    dist = [-1] * N
    answer = [0] * N

    for start in range(N):
        if dist[start] != -1:
            continue

        dist[start] = 0
        stack = [start]
        component = []

        while stack:
            v = stack.pop()
            component.append(v)

            for to, z in graph[v]:
                expected = dist[v] ^ z
                if dist[to] == -1:
                    dist[to] = expected
                    stack.append(to)
                elif dist[to] != expected:
                    print(-1)
                    return

        size = len(component)
        offset = 0

        for bit in range(30):
            ones = 0
            mask = 1 << bit
            for v in component:
                if dist[v] & mask:
                    ones += 1

            if ones * 2 > size:
                offset |= mask

        for v in component:
            answer[v] = dist[v] ^ offset

    print(*answer)


if __name__ == "__main__":
    solve()