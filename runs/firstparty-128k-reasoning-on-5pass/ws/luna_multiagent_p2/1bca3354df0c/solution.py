import sys


def solve() -> None:
    input = sys.stdin.buffer.readline

    n, m = map(int, input().split())
    graph = [[] for _ in range(n)]

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    color = [-1] * n
    special_count = 0

    for start in range(n):
        if color[start] != -1:
            continue

        color[start] = 0
        stack = [start]
        count = [1, 0]

        while stack:
            v = stack.pop()
            for to in graph[v]:
                if color[to] == -1:
                    color[to] = color[v] ^ 1
                    count[color[to]] += 1
                    stack.append(to)

        if (count[0] + count[1]) % 2 == 0 and count[0] % 2 == 1:
            special_count += 1

    if n % 2 == 1:
        aoki_wins = (m % 2 == 1)
    else:
        aoki_wins = ((m % 2) ^ (special_count % 2)) == 1

    print("Aoki" if aoki_wins else "Takahashi")


if __name__ == "__main__":
    solve()