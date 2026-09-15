import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    K = int(next(it))

    edges = []
    append = edges.append
    for _ in range(M):
        u = int(next(it))
        v = int(next(it))
        w = int(next(it))
        append((w, u - 1, v - 1))

    cnt_a = [0] * N
    cnt_b = [0] * N

    for _ in range(K):
        cnt_a[int(next(it)) - 1] += 1
    for _ in range(K):
        cnt_b[int(next(it)) - 1] += 1

    parent = list(range(N))
    size = [1] * N

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    edges.sort(key=lambda e: e[0])

    ans = 0

    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue

        if size[ru] < size[rv]:
            ru, rv = rv, ru

        au = cnt_a[ru]
        bu = cnt_b[ru]
        av = cnt_a[rv]
        bv = cnt_b[rv]

        inc = min(au + av, bu + bv) - min(au, bu) - min(av, bv)
        if inc:
            ans += w * inc

        parent[rv] = ru
        size[ru] += size[rv]
        cnt_a[ru] = au + av
        cnt_b[ru] = bu + bv

    print(ans)


if __name__ == "__main__":
    main()