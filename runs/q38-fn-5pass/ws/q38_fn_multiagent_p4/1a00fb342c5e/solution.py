import sys


def solve():
    input = sys.stdin.buffer.readline
    first = input().split()
    if not first:
        return

    N = int(first[0])
    M = int(first[1])

    adj = [[] for _ in range(N)]
    max_z = 0

    for _ in range(M):
        x, y, z = map(int, input().split())
        x -= 1
        y -= 1
        if z > max_z:
            max_z = z

        adj[x].append((y, z))
        if x != y:
            adj[y].append((x, z))

    val = [-1] * N
    ans = [0] * N

    # Bits above max_z are always zero in all tentative values,
    # so the optimal shift has zero there.
    B = max(1, max_z.bit_length())
    bit_range = range(B)

    for s in range(N):
        if val[s] != -1:
            continue

        # Isolated vertex.
        if not adj[s]:
            val[s] = 0
            ans[s] = 0
            continue

        val[s] = 0
        stack = [s]
        comp = []

        while stack:
            u = stack.pop()
            comp.append(u)
            vu = val[u]

            for v, w in adj[u]:
                nv = vu ^ w
                if val[v] == -1:
                    val[v] = nv
                    stack.append(v)
                elif val[v] != nv:
                    sys.stdout.write("-1\n")
                    return

        size = len(comp)

        if size == 1:
            ans[comp[0]] = 0
            continue

        counts = [0] * B

        for u in comp:
            x = val[u]
            if x:
                for b in bit_range:
                    counts[b] += (x >> b) & 1

        shift = 0
        for b in bit_range:
            if counts[b] > size - counts[b]:
                shift |= 1 << b

        for u in comp:
            ans[u] = val[u] ^ shift

    sys.stdout.write(" ".join(map(str, ans)) + "\n")


if __name__ == "__main__":
    solve()