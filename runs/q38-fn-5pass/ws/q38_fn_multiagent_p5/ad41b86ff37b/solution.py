import sys


def solve():
    input = sys.stdin.buffer.readline
    line = input()
    if not line:
        return

    N = int(line)
    adj = [[] for _ in range(N)]
    deg = [0] * N

    for _ in range(N - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1

    best = 0
    deg_local = deg

    for nbrs in adj:
        # Neighbor degrees > 1 are possible branch vertices.
        # If a branch has degree d, it can contribute d kept vertices:
        # itself plus d-1 leaves.
        ds = [deg_local[v] for v in nbrs if deg_local[v] > 1]
        if not ds:
            continue

        m = len(ds)
        max_d = max(ds)

        # Upper bound for this center.
        if 1 + m * max_d <= best:
            continue

        if m > 1:
            ds.sort(reverse=True)

        for i, d in enumerate(ds, 1):
            # For this and all later i, d is an upper bound on the degree.
            if 1 + m * d <= best:
                break

            kept = 1 + i * d
            if kept > best:
                best = kept
                if best == N:
                    print(0)
                    return

    print(N - best)


if __name__ == "__main__":
    solve()