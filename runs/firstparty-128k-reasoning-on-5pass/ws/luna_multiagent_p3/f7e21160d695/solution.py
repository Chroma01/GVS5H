import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = 0

    n = data[it]
    m = data[it + 1]
    k = data[it + 2]
    it += 3

    edges = []
    for _ in range(m):
        u = data[it] - 1
        v = data[it + 1] - 1
        w = data[it + 2]
        it += 3
        edges.append((w, u, v))

    a = data[it:it + k]
    it += k
    b = data[it:it + k]

    edges.sort()

    size = 2 * n + 5
    dsu = list(range(size))
    left = [-1] * size
    right = [-1] * size
    weight = [0] * size

    def find(x):
        root = x
        while dsu[root] != root:
            root = dsu[root]
        while dsu[x] != x:
            parent = dsu[x]
            dsu[x] = root
            x = parent
        return root

    residual = [0] * size
    for v in a:
        residual[v - 1] += 1
    for v in b:
        residual[v - 1] -= 1

    next_node = n
    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue

        z = next_node
        next_node += 1

        left[z] = ru
        right[z] = rv
        weight[z] = w

        dsu[z] = z
        dsu[ru] = z
        dsu[rv] = z

    root = find(0)
    answer = 0

    for z in range(n, next_node):
        l = left[z]
        r = right[z]
        rl = residual[l]
        rr = residual[r]

        if rl > 0 and rr < 0:
            answer += weight[z] * min(rl, -rr)
        elif rl < 0 and rr > 0:
            answer += weight[z] * min(-rl, rr)

        residual[z] = rl + rr

    print(answer)


if __name__ == "__main__":
    solve()