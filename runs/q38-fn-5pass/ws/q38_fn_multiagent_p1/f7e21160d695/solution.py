import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    idx = 0
    N = data[idx]
    M = data[idx + 1]
    K = data[idx + 2]
    idx += 3

    edges = []
    append = edges.append
    for _ in range(M):
        u = data[idx] - 1
        v = data[idx + 1] - 1
        w = data[idx + 2]
        idx += 3
        append((w, u, v))

    balance = [0] * N

    for _ in range(K):
        balance[data[idx] - 1] += 1
        idx += 1

    for _ in range(K):
        balance[data[idx] - 1] -= 1
        idx += 1

    del data

    edges.sort()

    parent = list(range(N))
    size = [1] * N

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

        if size[ru] < size[rv]:
            ru, rv = rv, ru

        bu = balance[ru]
        bv = balance[rv]

        if bu > 0 and bv < 0:
            if bu < -bv:
                ans += w * bu
            else:
                ans += w * (-bv)
        elif bu < 0 and bv > 0:
            if -bu < bv:
                ans += w * (-bu)
            else:
                ans += w * bv

        parent[rv] = ru
        size[ru] += size[rv]
        balance[ru] = bu + bv

    print(ans)


if __name__ == "__main__":
    main()