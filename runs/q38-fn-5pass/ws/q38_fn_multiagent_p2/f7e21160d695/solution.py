import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    idx = 0
    N = int(data[idx])
    idx += 1
    M = int(data[idx])
    idx += 1
    K = int(data[idx])
    idx += 1

    edges = []
    append = edges.append
    for _ in range(M):
        u = int(data[idx]) - 1
        v = int(data[idx + 1]) - 1
        w = int(data[idx + 2])
        idx += 3
        append((w, u, v))

    # surplus[v] > 0: unmatched A occurrences in this component
    # surplus[v] < 0: unmatched B occurrences in this component
    surplus = [0] * N

    for _ in range(K):
        a = int(data[idx]) - 1
        idx += 1
        surplus[a] += 1

    for _ in range(K):
        b = int(data[idx]) - 1
        idx += 1
        surplus[b] -= 1

    del data

    edges.sort()

    parent = list(range(N))
    size = [1] * N

    def find(x, parent=parent):
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

        su = surplus[ru]
        sv = surplus[rv]

        if su > 0 and sv < 0:
            matched = su if su < -sv else -sv
            ans += w * matched
        elif su < 0 and sv > 0:
            matched = -su if -su < sv else sv
            ans += w * matched

        surplus[ru] = su + sv
        parent[rv] = ru
        size[ru] += size[rv]

    print(ans)


if __name__ == "__main__":
    main()