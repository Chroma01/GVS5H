import sys
import heapq
from array import array


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m, s, t = data[0], data[1], data[2] - 1, data[3] - 1
    pos = 4

    vertices = 2 * n
    head = array('i', [-1]) * vertices
    to = array('i')
    nxt = array('i')
    cap = array('b')
    cost = array('b')

    def add_edge(u, v, capacity, c):
        e = len(to)
        to.append(v)
        cap.append(capacity)
        cost.append(c)
        nxt.append(head[u])
        head[u] = e

        to.append(u)
        cap.append(0)
        cost.append(-c)
        nxt.append(head[v])
        head[v] = e + 1

    def vin(v):
        return 2 * v

    def vout(v):
        return 2 * v + 1

    # Internal vertices have capacity one.
    for v in range(n):
        if v != s and v != t:
            add_edge(vin(v), vout(v), 1, 0)

    # Source and sink are represented by Sout and Tin.
    source = vout(s)
    sink = vin(t)

    # Movement edges. Do not enter S or leave T, so paths are simple
    # with respect to the terminals.
    for _ in range(m):
        u, v = data[pos] - 1, data[pos + 1] - 1
        pos += 2

        if u != t and v != s:
            add_edge(vout(u), vin(v), 1, 1)
        if v != t and u != s:
            add_edge(vout(v), vin(u), 1, 1)

    inf = 10 ** 18
    potential = [0] * vertices
    total_cost = 0

    for _ in range(2):
        dist = [inf] * vertices
        parent = [-1] * vertices
        dist[source] = 0
        heap = [(0, source)]

        while heap:
            d, u = heapq.heappop(heap)
            if d != dist[u]:
                continue

            e = head[u]
            while e != -1:
                if cap[e]:
                    v = to[e]
                    nd = d + cost[e] + potential[u] - potential[v]
                    if nd < dist[v]:
                        dist[v] = nd
                        parent[v] = e
                        heapq.heappush(heap, (nd, v))
                e = nxt[e]

        if dist[sink] == inf:
            print(-1)
            return

        for v in range(vertices):
            if dist[v] < inf:
                potential[v] += dist[v]

        v = sink
        path_cost = 0
        while v != source:
            e = parent[v]
            cap[e] = 0
            cap[e ^ 1] = 1
            path_cost += cost[e]
            v = to[e ^ 1]

        total_cost += path_cost

    print(total_cost)


if __name__ == "__main__":
    solve()