import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    pos = 0
    N = int(data[pos]); M = int(data[pos + 1]); K = int(data[pos + 2])
    pos += 3

    edges = []
    for _ in range(M):
        u = int(data[pos]); v = int(data[pos + 1]); w = int(data[pos + 2])
        pos += 3
        edges.append((w, u, v))

    # Signed surplus at each vertex: (# unmatched A) - (# unmatched B).
    # The guarantee A_i != B_j means no vertex needs both signs initially,
    # but the net-count method would also cancel same-vertex pairs at cost 0.
    diff = [0] * (N + 1)
    for _ in range(K):
        a = int(data[pos]); pos += 1
        diff[a] += 1
    for _ in range(K):
        b = int(data[pos]); pos += 1
        diff[b] -= 1

    edges.sort()  # Kruskal order: nondecreasing bottleneck threshold

    parent = list(range(N + 1))
    size = [1] * (N + 1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    ans = 0
    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue

        du = diff[ru]
        dv = diff[rv]

        # If the two components carry opposite unmatched types, every such
        # cross pair can now be matched at bottleneck cost exactly w. Match
        # as many as possible; deferring cannot make any of them cheaper.
        if (du > 0 and dv < 0) or (du < 0 and dv > 0):
            au = du if du >= 0 else -du
            av = dv if dv >= 0 else -dv
            m = au if au < av else av
            ans += m * w

        if size[ru] < size[rv]:
            ru, rv = rv, ru
        parent[rv] = ru
        size[ru] += size[rv]
        diff[ru] = du + dv

    sys.stdout.write(str(ans) + "\n")

main()