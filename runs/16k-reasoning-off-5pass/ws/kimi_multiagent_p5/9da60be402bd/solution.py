import sys
import heapq

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    rows = data[1:1 + n]

    # Per-vertex, per-letter predecessor and successor lists.
    # preds[u][c] = list of x with edge x -> u labeled c
    # succs[v][c] = list of y with edge v -> y labeled c
    preds = [[[] for _ in range(26)] for _ in range(n)]
    succs = [[[] for _ in range(26)] for _ in range(n)]
    for i in range(n):
        row = rows[i]
        for j, ch in enumerate(row):
            if ch != '-':
                c = ord(ch) - 97
                succs[i][c].append(j)
                preds[j][c].append(i)

    # State = unordered pair (a, b) with a <= b, encoded as a * n + b.
    INF = -1
    size = n * n
    dist = [INF] * size
    heap = []

    def relax(a, b, d):
        if a > b:
            a, b = b, a
        idx = a * n + b
        if dist[idx] == INF or d < dist[idx]:
            dist[idx] = d
            heapq.heappush(heap, (d, a, b))

    # Seeds: empty palindrome (length 0) and single-edge palindromes (length 1).
    for u in range(n):
        relax(u, u, 0)
    for u in range(n):
        for c in range(26):
            for v in succs[u][c]:
                relax(u, v, 1)

    # Multi-source Dijkstra: expanding both ends with the same letter costs +2.
    while heap:
        d, u, v = heapq.heappop(heap)
        if u > v:
            u, v = v, u
        if dist[u * n + v] != d:
            continue
        nd = d + 2
        pu = preds[u]
        sv = succs[v]
        for c in range(26):
            pl = pu[c]
            sl = sv[c]
            if not pl or not sl:
                continue
            for x in pl:
                for y in sl:
                    a, b = (x, y) if x <= y else (y, x)
                    idx = a * n + b
                    if dist[idx] == INF or nd < dist[idx]:
                        dist[idx] = nd
                        heapq.heappush(heap, (nd, a, b))

    out_lines = []
    for i in range(n):
        line = []
        base_i = i * n
        for j in range(n):
            idx = base_i + j if i <= j else j * n + i
            line.append(str(dist[idx]))
        out_lines.append(' '.join(line))
    sys.stdout.write('\n'.join(out_lines) + '\n')

main()