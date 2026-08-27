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
    max_deg = max(deg)

    buckets = [[] for _ in range(max_deg)]
    for v in range(n):
        if deg[v] >= 2:
            buckets[deg[v] - 1].append(v)

    eligible_count = [0] * n
    current_max_count = 0
    best_size = 0

    # At threshold y, vertices with degree(v)-1 >= y are active.
    for y in range(max_deg - 1, 0, -1):
        for middle in buckets[y]:
            for center in graph[middle]:
                eligible_count[center] += 1
                if eligible_count[center] > current_max_count:
                    current_max_count = eligible_count[center]

        if current_max_count > 0:
            best_size = max(best_size, 1 + (y + 1) * current_max_count)

    print(n - best_size)


if __name__ == "__main__":
    main()