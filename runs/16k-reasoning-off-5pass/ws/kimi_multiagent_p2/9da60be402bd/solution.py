import sys
from heapq import heappush, heappop

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    rows = data[1:1 + n]

    INF = 10 ** 9

    # inL[v][c]  : list of i such that edge i -> v has label c
    # outL[u][c] : list of j such that edge u -> j has label c
    inL = [[[] for _ in range(26)] for _ in range(n)]
    outL = [[[] for _ in range(26)] for _ in range(n)]
    edges = []
    for i in range(n):
        r = rows[i]
        oi = outL[i]
        for j in range(n):
            ch = r[j]
            if ch != 45:  # '-'
                c = ch - 97
                oi[c].append(j)
                inL[j][c].append(i)
                edges.append((i, j))

    # dist[u][v] = shortest palindrome-labeled walk from u to v
    dist = [[INF] * n for _ in range(n)]
    heap = []
    infcount = n * n
    maxt = 0  # max tentative distance ever assigned (tentatives only decrease)

    # length 0 palindrome: empty string at (x, x)
    for x in range(n):
        dist[x][x] = 0
        infcount -= 1
        heappush(heap, (0, x, x))
    # length 1 palindrome: any single edge
    for i, j in edges:
        if dist[i][j] > 1:
            if dist[i][j] == INF:
                infcount -= 1
            dist[i][j] = 1
            heappush(heap, (1, i, j))
    if edges:
        maxt = 1

    # labels with non-empty in-list, per vertex
    in_labels = [[c for c in range(26) if inL[v][c]] for v in range(n)]

    # Dijkstra over the N^2 pair-states.
    # From (u, v) with distance d we can extend outward:
    #   i --c--> u  ...  v --c--> j   gives palindrome of length d+2 from i to j.
    while heap:
        d, u, v = heappop(heap)
        if d != dist[u][v]:
            continue
        nd = d + 2
        # All future candidates are >= nd; if nothing can be improved, stop.
        if nd > maxt and infcount == 0:
            break
        outv = outL[v]
        inu = inL[u]
        for c in in_labels[u]:
            J = outv[c]
            if not J:
                continue
            for i in inu[c]:
                row = dist[i]
                for j in J:
                    if nd < row[j]:
                        if row[j] == INF:
                            infcount -= 1
                        row[j] = nd
                        heappush(heap, (nd, i, j))
                        if nd > maxt:
                            maxt = nd

    out_lines = []
    for i in range(n):
        row = dist[i]
        out_lines.append(' '.join('-1' if row[j] == INF else str(row[j])
                                  for j in range(n)))
    sys.stdout.write('\n'.join(out_lines) + '\n')

main()