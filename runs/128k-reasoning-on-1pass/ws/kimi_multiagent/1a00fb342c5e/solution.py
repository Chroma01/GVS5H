import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    it = iter(data)
    n = next(it)
    m = next(it)

    edges = []
    max_z = 0
    for _ in range(m):
        x = next(it) - 1
        y = next(it) - 1
        z = next(it)
        edges.append((x, y, z))
        if z > max_z:
            max_z = z

    ans = [0] * n
    B = max_z.bit_length()
    out_write = sys.stdout.write

    for b in range(B):
        bit = 1 << b
        parent = list(range(n))
        size = [1] * n
        diff = [0] * n  # diff[v] = bit(v) XOR bit(parent[v]); root: bit(v) XOR bit(root)

        ok = True
        for x, y, z in edges:
            w = (z >> b) & 1

            # find(x) with path compression, normalizing diff to root
            if parent[x] != x:
                path = []
                t = x
                while parent[t] != t:
                    path.append(t)
                    t = parent[t]
                rx = t
                acc = 0
                for node in reversed(path):
                    acc ^= diff[node]
                    diff[node] = acc
                    parent[node] = rx
            else:
                rx = x

            # find(y)
            if parent[y] != y:
                path = []
                t = y
                while parent[t] != t:
                    path.append(t)
                    t = parent[t]
                ry = t
                acc = 0
                for node in reversed(path):
                    acc ^= diff[node]
                    diff[node] = acc
                    parent[node] = ry
            else:
                ry = y

            if rx == ry:
                if (diff[x] ^ diff[y]) != w:
                    ok = False
                    break
            else:
                t = w ^ diff[x] ^ diff[y]  # required bit(rx) XOR bit(ry)
                if size[rx] < size[ry]:
                    parent[rx] = ry
                    diff[rx] = t
                    size[ry] += size[rx]
                else:
                    parent[ry] = rx
                    diff[ry] = t
                    size[rx] += size[ry]

        if not ok:
            out_write("-1")
            return

        # Compress all nodes so diff[v] is relative to root, count ones per root
        ones = [0] * n
        for v in range(n):
            if parent[v] != v:
                path = []
                t = v
                while parent[t] != t:
                    path.append(t)
                    t = parent[t]
                root = t
                acc = 0
                for node in reversed(path):
                    acc ^= diff[node]
                    diff[node] = acc
                    parent[node] = root
            if diff[v]:
                ones[parent[v]] += 1

        # Decide per-component flip to minimize number of ones
        flip = bytearray(n)
        for r in range(n):
            if parent[r] == r and ones[r] * 2 > size[r]:
                flip[r] = 1

        for v in range(n):
            if diff[v] ^ flip[parent[v]]:
                ans[v] |= bit

    out_write(" ".join(map(str, ans)))

if __name__ == "__main__":
    main()