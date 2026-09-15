import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]

    # Any tree with 3 vertices is a path of length 2, i.e. a snowflake
    # with x = 1, y = 1.
    if n == 3:
        print(0)
        return

    adj = [[] for _ in range(n)]
    deg = [0] * n

    idx = 1
    for _ in range(n - 1):
        u = data[idx] - 1
        v = data[idx + 1] - 1
        idx += 2

        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1

    del data

    # cap[v] = number of vertices that can be used as leaves if v is
    # chosen as a middle vertex attached to some center.
    cap = [d - 1 for d in deg]
    del deg

    best = 3
    cap_local = cap
    n_local = n

    for neigh in adj:
        d = len(neigh)

        # Center with one neighbor: only x = 1 is possible.
        if d == 1:
            y = cap_local[neigh[0]]
            if y > 0:
                val = y + 2  # 1 + 1 * (y + 1)
                if val > best:
                    best = val
                    if best == n_local:
                        break
            continue

        # Center with two neighbors: handle x = 1 and x = 2 directly.
        if d == 2:
            a = neigh[0]
            b = neigh[1]
            ca = cap_local[a]
            cb = cap_local[b]

            if ca > 0:
                val = ca + 2
                if val > best:
                    best = val
                    if best == n_local:
                        break

            if cb > 0:
                val = cb + 2
                if val > best:
                    best = val
                    if best == n_local:
                        break

            if ca > 0 and cb > 0:
                y = ca if ca < cb else cb
                val = 2 * y + 3  # 1 + 2 * (y + 1)
                if val > best:
                    best = val
                    if best == n_local:
                        break

            continue

        # General center: collect positive capacities of possible middle vertices.
        caps = [cap_local[m] for m in neigh if cap_local[m] > 0]
        lc = len(caps)

        if lc == 0:
            continue

        if lc == 1:
            val = caps[0] + 2
            if val > best:
                best = val
                if best == n_local:
                    break
            continue

        if lc == 2:
            a = caps[0]
            b = caps[1]
            if a < b:
                a, b = b, a

            val = a + 2
            if val > best:
                best = val
                if best == n_local:
                    break

            val = 2 * b + 3
            if val > best:
                best = val
                if best == n_local:
                    break

            continue

        caps.sort(reverse=True)

        # If x middle vertices are chosen, the maximum common y is the
        # x-th largest positive capacity.
        for x, y in enumerate(caps, 1):
            val = 1 + x * (y + 1)
            if val > best:
                best = val
                if best == n_local:
                    break

        if best == n_local:
            break

    print(n_local - best)


if __name__ == "__main__":
    main()