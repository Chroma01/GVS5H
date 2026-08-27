import sys
import heapq
from array import array


def main():
    input = sys.stdin.buffer.readline
    n, m, s, t = map(int, input().split())
    s -= 1
    t -= 1

    # For each original vertex v:
    # vin(v) = 2*v, vout(v) = 2*v+1.
    # The vin -> vout edge enforces vertex capacity.
    vn = 2 * n
    source = 2 * s + 1
    sink = 2 * t

    head = array('i', [-1]) * vn
    to = array('i')
    nxt = array('i')
    cost = array('b')
    cap = bytearray()

    def add_edge(v, u, capacity, edge_cost):
        idx = len(to)

        to.append(u)
        nxt.append(head[v])
        head[v] = idx
        cap.append(capacity)
        cost.append(edge_cost)

        to.append(v)
        nxt.append(head[u])
        head[u] = idx + 1
        cap.append(0)
        cost.append(-edge_cost)

    for v in range(n):
        # S and T may be used by both paths; every other vertex by at most one.
        vertex_capacity = 2 if v == s or v == t else 1
        add_edge(2 * v, 2 * v + 1, vertex_capacity, 0)

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1

        # Each traversal of an original edge costs one move.
        add_edge(2 * u + 1, 2 * v, 1, 1)
        add_edge(2 * v + 1, 2 * u, 1, 1)

    inf = 10**18
    potential = [0] * vn
    total_cost = 0

    # Send two units of flow with successive shortest augmenting paths.
    for _ in range(2):
        dist = [inf] * vn
        prev = [-1] * vn
        dist[source] = 0
        pq = [(0, source)]

        # Do not stop when sink is popped: potentials must be updated for all
        # reachable residual vertices to preserve nonnegative reduced costs.
        while pq:
            d, v = heapq.heappop(pq)
            if d != dist[v]:
                continue

            e = head[v]
            while e != -1:
                if cap[e]:
                    u = to[e]
                    nd = d + cost[e] + potential[v] - potential[u]
                    if nd < dist[u]:
                        dist[u] = nd
                        prev[u] = e
                        heapq.heappush(pq, (nd, u))
                e = nxt[e]

        if dist[sink] == inf:
            print(-1)
            return

        # Update every reachable vertex potential, not merely the sink path.
        for v in range(vn):
            if dist[v] != inf:
                potential[v] += dist[v]

        v = sink
        while v != source:
            e = prev[v]
            total_cost += cost[e]
            cap[e] -= 1
            cap[e ^ 1] += 1
            v = to[e ^ 1]

    print(total_cost)


if __name__ == "__main__":
    main()