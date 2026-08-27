import sys

def main():
    it = map(int, sys.stdin.buffer.read().split())
    try:
        n = next(it)
    except StopIteration:
        return
    m = next(it)
    k = next(it)

    edges = []
    append = edges.append
    for _ in range(m):
        u = next(it)
        v = next(it)
        w = next(it)
        append((w, u, v))

    bal = [0] * (n + 1)
    for _ in range(k):
        bal[next(it)] += 1
    for _ in range(k):
        bal[next(it)] -= 1

    del it

    edges.sort()

    parent = list(range(n + 1))
    size = [1] * (n + 1)

    par = parent
    sz = size
    b = bal
    ab = abs

    def find(x, par=par):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    ans = 0
    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue

        cu = b[ru]
        cv = b[rv]
        s = cu + cv

        dec = (ab(cu) + ab(cv) - ab(s)) // 2
        if dec:
            ans += dec * w

        if sz[ru] < sz[rv]:
            ru, rv = rv, ru

        par[rv] = ru
        sz[ru] += sz[rv]
        b[ru] = s

    print(ans)

if __name__ == "__main__":
    main()