import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    s = int(data[idx]); idx += 1
    t = int(data[idx]); idx += 1

    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        adj[u].append(v)
        adj[v].append(u)

    # Baseline reference solution: BFS over ordered configuration states (a, b),
    # a != b, meaning piece A is at a and piece B is at b.
    #   start = (S, T), goal = (T, S)
    #   from (a, b): successors (a', b) for a' in adj[a], a' != b,
    #                and (a, b') for b' in adj[b], b' != a.
    # NOTE: this is O(N^2) states (up to N^2) with O(N) transitions each -> O(N^3)
    # worst case; it is the guaranteed-correct reference and will be optimized later.
    start = (s, t)
    goal = (t, s)

    dist = {start: 0}
    q = deque([start])
    while q:
        a, b = q.popleft()
        d = dist[(a, b)]
        if (a, b) == goal:
            print(d)
            return
        for na in adj[a]:
            if na != b:
                st = (na, b)
                if st not in dist:
                    dist[st] = d + 1
                    q.append(st)
        for nb in adj[b]:
            if nb != a:
                st = (a, nb)
                if st not in dist:
                    dist[st] = d + 1
                    q.append(st)

    print(-1)


main()