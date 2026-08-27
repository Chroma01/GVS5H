import sys

def solve():
    input = sys.stdin.buffer.readline
    n = int(input())
    graph = [[] for _ in range(n)]

    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    best = 0

    for center in range(n):
        capacities = [len(graph[neighbor]) - 1 for neighbor in graph[center]]
        capacities.sort(reverse=True)

        for i, capacity in enumerate(capacities, 1):
            if capacity <= 0:
                break
            retained = 1 + i * (capacity + 1)
            if retained > best:
                best = retained

    print(n - best)

if __name__ == "__main__":
    solve()