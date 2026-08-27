import sys


def main():
    input = sys.stdin.buffer.readline
    n = int(input())
    graph = [[] for _ in range(n)]

    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    deg = [len(adj) for adj in graph]
    best = 0

    for center in range(n):
        capacities = [deg[v] - 1 for v in graph[center] if deg[v] >= 2]
        capacities.sort(reverse=True)

        count = 0
        i = 0
        while i < len(capacities):
            cap = capacities[i]
            j = i
            while j < len(capacities) and capacities[j] == cap:
                j += 1

            count = j
            retained = 1 + count * (cap + 1)
            if retained > best:
                best = retained

            i = j

    print(n - best)


if __name__ == "__main__":
    main()