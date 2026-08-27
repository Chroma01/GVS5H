import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    p = 0
    N = int(data[p]); p += 1
    M = int(data[p]); p += 1
    K = int(data[p]); p += 1

    edges = []
    append = edges.append
    for _ in range(M):
        u = int(data[p]) - 1
        v = int(data[p + 1]) - 1
        w = int(data[p + 2])
        p += 3
        append((w, u, v))

    diff = [0] * N
    for _ in range(K):
        diff[int(data[p]) - 1] += 1
        p += 1
    for _ in range(K):
        diff[int(data[p]) - 1] -= 1
        p += 1

    del data

    edges.sort()

    parent = list(range(N))
    size = [1] * N
    sum_abs = sum(map(abs, diff))

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

        old_half = sum_abs // 2

        if size[ru] < size[rv]:
            ru, rv = rv, ru

        a = diff[ru]
        b = diff[rv]

        sum_abs -= abs(a) + abs(b) - abs(a + b)

        parent[rv] = ru
        size[ru] += size[rv]
        diff[ru] = a + b

        new_half = sum_abs // 2
        ans += w * (old_half - new_half)

    print(ans)

if __name__ == "__main__":
    main()