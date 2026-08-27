import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    m = next(it)
    k = next(it)

    edges = []
    for _ in range(m):
        u = next(it) - 1
        v = next(it) - 1
        w = next(it)
        edges.append((w, u, v))

    a = [next(it) - 1 for _ in range(k)]
    b = [next(it) - 1 for _ in range(k)]

    count_a = [0] * n
    count_b = [0] * n

    for v in a:
        count_a[v] += 1
    for v in b:
        count_b[v] += 1

    parent = [-1] * n

    def find(x):
        while parent[x] >= 0:
            if parent[parent[x]] >= 0:
                parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    edges.sort()

    matched = sum(min(count_a[i], count_b[i]) for i in range(n))
    answer = 0

    for w, u, v in edges:
        ru = find(u)
        rv = find(v)

        if ru == rv:
            continue

        old_pairs = min(count_a[ru], count_b[ru]) + min(count_a[rv], count_b[rv])

        if parent[ru] > parent[rv]:
            ru, rv = rv, ru

        parent[ru] += parent[rv]
        parent[rv] = ru

        count_a[ru] += count_a[rv]
        count_b[ru] += count_b[rv]

        new_pairs = min(count_a[ru], count_b[ru])
        increase = new_pairs - old_pairs

        matched += increase
        answer += increase * w

    print(answer)


if __name__ == "__main__":
    solve()