import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(map(int, data))

    N = next(it)
    M = next(it)
    K = next(it)

    edges = []
    for _ in range(M):
        u = next(it)
        v = next(it)
        w = next(it)
        edges.append((w, u, v))

    surplus = [0] * (N + 1)
    for _ in range(K):
        surplus[next(it)] += 1
    for _ in range(K):
        surplus[next(it)] -= 1

    edges.sort()

    parent = list(range(N + 1))
    size = [1] * (N + 1)

    def find(x, p=parent):
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x

    ans = 0

    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue

        su = surplus[ru]
        sv = surplus[rv]

        if su > 0:
            if sv < 0:
                if su < -sv:
                    ans += w * su
                else:
                    ans += w * (-sv)
        elif su < 0:
            if sv > 0:
                if sv < -su:
                    ans += w * sv
                else:
                    ans += w * (-su)

        if size[ru] < size[rv]:
            ru, rv = rv, ru

        parent[rv] = ru
        surplus[ru] += surplus[rv]
        size[ru] += size[rv]

    print(ans)

if __name__ == "__main__":
    main()