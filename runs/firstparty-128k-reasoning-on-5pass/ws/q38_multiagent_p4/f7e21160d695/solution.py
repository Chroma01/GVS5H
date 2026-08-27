import sys

def main():
    input = sys.stdin.buffer.readline
    line = input()
    if not line:
        return
    n, m, k = map(int, line.split())

    edges = []
    for _ in range(m):
        u, v, w = map(int, input().split())
        edges.append((w, u, v))

    a = [0] * (n + 1)
    cnt = 0
    while cnt < k:
        line = input()
        if not line:
            break
        for x in map(int, line.split()):
            a[x] += 1
            cnt += 1

    b = [0] * (n + 1)
    cnt = 0
    while cnt < k:
        line = input()
        if not line:
            break
        for x in map(int, line.split()):
            b[x] += 1
            cnt += 1

    edges.sort()

    parent = list(range(n + 1))
    size = [1] * (n + 1)

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

        au = a[ru]
        bu = b[ru]
        av = a[rv]
        bv = b[rv]

        total_a = au + av
        total_b = bu + bv
        delta = (total_a if total_a < total_b else total_b)
        delta -= (au if au < bu else bu)
        delta -= (av if av < bv else bv)

        if delta:
            ans += w * delta

        if size[ru] < size[rv]:
            ru, rv = rv, ru
        parent[rv] = ru
        size[ru] += size[rv]
        a[ru] += a[rv]
        b[ru] += b[rv]

    print(ans)

if __name__ == "__main__":
    main()