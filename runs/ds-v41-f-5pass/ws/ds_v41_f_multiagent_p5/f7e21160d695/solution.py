import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    k = int(data[idx]); idx += 1

    edges = []
    for _ in range(m):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        w = int(data[idx]); idx += 1
        edges.append((w, u, v))

    A = data[idx:idx + k]; idx += k
    B = data[idx:idx + k]; idx += k

    # surplus[v] = (#unmatched A at v) - (#unmatched B at v)
    surplus = [0] * (n + 1)
    for x in A:
        surplus[int(x)] += 1
    for x in B:
        surplus[int(x)] -= 1

    edges.sort()

    parent = list(range(n + 1))
    size = [1] * (n + 1)

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    ans = 0
    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue
        if size[ru] < size[rv]:
            ru, rv = rv, ru
        parent[rv] = ru
        size[ru] += size[rv]

        su = surplus[ru]
        sv = surplus[rv]
        if su > 0 and sv < 0:
            matched = su if su <= -sv else -sv
            ans += matched * w
        elif su < 0 and sv > 0:
            matched = -su if -su <= sv else sv
            ans += matched * w
        surplus[ru] = su + sv

    sys.stdout.write(str(ans) + "\n")

main()