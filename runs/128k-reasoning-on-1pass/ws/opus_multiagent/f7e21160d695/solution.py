import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[0]); M = int(data[1]); K = int(data[2])
    base = 3
    end = base + 3 * M
    # tokens: u,v,w triples
    us = data[base:end:3]
    vs = data[base + 1:end:3]
    ws = data[base + 2:end:3]
    edges = sorted(zip(map(int, ws), map(int, us), map(int, vs)))

    A = data[end:end + K]
    B = data[end + K:end + 2 * K]

    surplus = [0] * (N + 1)
    for a in A:
        surplus[int(a)] += 1
    for b in B:
        surplus[int(b)] -= 1

    parent = list(range(N + 1))
    size = [1] * (N + 1)

    ans = 0
    for w, u, v in edges:
        # find root of u
        r = u
        while parent[r] != r:
            r = parent[r]
        # path compression
        x = u
        while parent[x] != r:
            nxt = parent[x]
            parent[x] = r
            x = nxt
        ru = r
        # find root of v
        r = v
        while parent[r] != r:
            r = parent[r]
        x = v
        while parent[x] != r:
            nxt = parent[x]
            parent[x] = r
            x = nxt
        rv = r

        if ru == rv:
            continue

        s1 = surplus[ru]
        s2 = surplus[rv]
        s = s1 + s2
        a1 = s1 if s1 >= 0 else -s1
        a2 = s2 if s2 >= 0 else -s2
        asum = s if s >= 0 else -s
        pairs = (a1 + a2 - asum) >> 1
        if pairs:
            ans += pairs * w

        if size[ru] < size[rv]:
            ru, rv = rv, ru
        parent[rv] = ru
        size[ru] += size[rv]
        surplus[ru] = s

    sys.stdout.write(str(ans) + "\n")

main()