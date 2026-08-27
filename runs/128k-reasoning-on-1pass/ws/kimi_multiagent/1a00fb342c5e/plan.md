```python
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

    for b in range(B):
        bit = 1 << b
        parent = list(range(n))
        size = [1] * n
        diff = [0] * n  # xor from node to its parent

        def find(x):
            if parent[x] == x:
                return x
            path = []
            y = x
            while parent[y] != y:
                path.append(y)
                y = parent[y]
            root = y
            acc = 0
            for node in reversed(path):
                acc ^= diff[node]
                diff[node] = acc
                parent[node] = root
            return root

        ok = True
        for x, y, z in edges:
            w = (z >> b) & 1
            rx = find(x)
            ry = find(y)
            if rx == ry:
                if (diff[x] ^ diff[y]) != w:
                    ok = False
                    break
            else:
                t = w ^ diff[x] ^ diff[y]
                if size[rx] < size[ry]:
                    parent[rx] = ry
                    diff[rx] = t
                    size[ry] += size[rx]
                else:
                    parent[ry] = rx
                    diff[ry] = t
                    size[rx] += size[ry]

        if not ok:
            sys.stdout.write("-1")
            return

        ones = [0] * n
        for v in range(n):
            r = find(v)
            if diff[v]:
                ones[r] += 1

        flip = bytearray(n)
        for r in range(n):
            if parent[r] == r and ones[r] * 2 > size[r]:
                flip[r] = 1

        for v in range(n):
            if diff[v] ^ flip[parent[v]]:
                ans[v] |= bit

    sys.stdout.write(" ".join(map(str, ans)))

if __name__ == "__main__":
    main()
```