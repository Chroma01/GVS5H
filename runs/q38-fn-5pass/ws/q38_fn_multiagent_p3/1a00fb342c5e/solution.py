import sys


def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    N = int(next(it))
    M = int(next(it))

    adj = [[] for _ in range(N + 1)]
    max_z = 0

    for _ in range(M):
        x = int(next(it))
        y = int(next(it))
        z = int(next(it))

        adj[x].append((y, z))
        if x != y:
            adj[y].append((x, z))

        if z > max_z:
            max_z = z

    # All potentials are XORs of edge weights, so no bit above max_z can appear.
    BITS = max(1, max_z.bit_length())
    bit_range = range(BITS)

    # pot[v] is the value of vertex v relative to its component root.
    # -1 means unvisited.
    pot = [-1] * (N + 1)
    ans = [0] * (N + 1)

    for start in range(1, N + 1):
        if pot[start] != -1:
            continue

        pot[start] = 0
        stack = [start]
        comp = []

        while stack:
            v = stack.pop()
            comp.append(v)
            pv = pot[v]

            for to, w in adj[v]:
                if pot[to] == -1:
                    pot[to] = pv ^ w
                    stack.append(to)
                elif (pv ^ pot[to]) != w:
                    sys.stdout.write("-1\n")
                    return

        size = len(comp)

        # Isolated vertex, or a single vertex with only consistent self-loops.
        if size == 1:
            ans[comp[0]] = 0
            continue

        # Count how many base values have each bit set.
        counts = [0] * BITS
        for v in comp:
            val = pot[v]
            for k in bit_range:
                counts[k] += (val >> k) & 1

        # Choose the component offset bit independently.
        offset = 0
        for k in bit_range:
            if counts[k] * 2 > size:
                offset |= 1 << k

        if offset:
            for v in comp:
                ans[v] = pot[v] ^ offset
        else:
            for v in comp:
                ans[v] = pot[v]

    sys.stdout.write(" ".join(map(str, ans[1:])) + "\n")


if __name__ == "__main__":
    solve()