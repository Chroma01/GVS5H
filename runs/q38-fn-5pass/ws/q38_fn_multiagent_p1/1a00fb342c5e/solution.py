import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    m = int(data[1])

    adj = [[] for _ in range(n)]
    max_z = 0
    idx = 2

    for _ in range(m):
        x = int(data[idx]) - 1
        y = int(data[idx + 1]) - 1
        z = int(data[idx + 2])
        idx += 3

        if x == y:
            if z != 0:
                print(-1)
                return
            continue

        if z > max_z:
            max_z = z

        adj[x].append((y, z))
        adj[y].append((x, z))

    bits = max(1, max_z.bit_length())
    bit_range = range(bits)

    val = [-1] * n

    for start in range(n):
        if val[start] != -1:
            continue

        if not adj[start]:
            val[start] = 0
            continue

        val[start] = 0
        stack = [start]
        comp = [start]
        counts = [0] * bits

        while stack:
            v = stack.pop()
            vv = val[v]

            if vv:
                for b in bit_range:
                    counts[b] += (vv >> b) & 1

            for to, w in adj[v]:
                nv = vv ^ w
                if val[to] == -1:
                    val[to] = nv
                    stack.append(to)
                    comp.append(to)
                elif val[to] != nv:
                    print(-1)
                    return

        size = len(comp)
        offset = 0

        for b in bit_range:
            if counts[b] * 2 > size:
                offset |= 1 << b

        if offset:
            for v in comp:
                val[v] ^= offset

    sys.stdout.write(" ".join(map(str, val)) + "\n")

if __name__ == "__main__":
    solve()