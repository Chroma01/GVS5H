import sys
import heapq

def solve():
    input = sys.stdin.readline
    n = int(input())
    graph = [input().strip() for _ in range(n)]

    incoming = [[set() for _ in range(26)] for _ in range(n)]
    outgoing = [[set() for _ in range(26)] for _ in range(n)]

    for u in range(n):
        row = graph[u]
        for v, ch in enumerate(row):
            if ch != '-':
                c = ord(ch) - 97
                outgoing[u][c].add(v)
                incoming[v][c].add(u)

    total = n * n
    dist = [-1] * total
    unknown_rows = [set(range(n)) for _ in range(n)]
    heap = []

    for i in range(n):
        idx = i * n + i
        dist[idx] = 0
        unknown_rows[i].remove(i)
        heap.append((0, i, i))

    for u in range(n):
        for v, ch in enumerate(graph[u]):
            if ch == '-':
                continue
            idx = u * n + v
            if dist[idx] == -1:
                dist[idx] = 1
                unknown_rows[u].remove(v)
                heap.append((1, u, v))

    heapq.heapify(heap)

    while heap:
        d, x, y = heapq.heappop(heap)
        if dist[x * n + y] != d:
            continue

        nd = d + 2
        for c in range(26):
            right = outgoing[y][c]
            if not right:
                continue

            for u in incoming[x][c]:
                row_unknown = unknown_rows[u]
                if not row_unknown:
                    continue

                candidates = row_unknown.intersection(right)
                if not candidates:
                    continue

                for v in candidates:
                    dist[u * n + v] = nd
                    heapq.heappush(heap, (nd, u, v))
                row_unknown.difference_update(candidates)

    out = []
    for i in range(n):
        out.append(" ".join(map(str, dist[i * n:(i + 1) * n])))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()