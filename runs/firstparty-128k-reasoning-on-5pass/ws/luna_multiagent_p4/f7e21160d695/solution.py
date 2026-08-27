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

    count_a = [0] * n
    for _ in range(k):
        count_a[next(it) - 1] += 1

    count_b = [0] * n
    for _ in range(k):
        count_b[next(it) - 1] += 1

    edges.sort()

    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    answer = 0

    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue

        old_pairs = min(count_a[ru], count_b[ru]) + min(count_a[rv], count_b[rv])

        if size[ru] < size[rv]:
            ru, rv = rv, ru

        parent[rv] = ru
        size[ru] += size[rv]
        count_a[ru] += count_a[rv]
        count_b[ru] += count_b[rv]

        new_pairs = min(count_a[ru], count_b[ru])
        answer += (new_pairs - old_pairs) * w

    print(answer)

if __name__ == "__main__":
    solve()