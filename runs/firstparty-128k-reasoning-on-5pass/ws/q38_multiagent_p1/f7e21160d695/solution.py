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

    edges = [None] * M
    for i in range(M):
        u = int(data[idx])
        v = int(data[idx + 1])
        w = int(data[idx + 2])
        idx += 3
        edges[i] = (w, u, v)

    a_cnt = [0] * (N + 1)
    for _ in range(K):
        a_cnt[int(data[idx])] += 1
        idx += 1

    b_cnt = [0] * (N + 1)
    for _ in range(K):
        b_cnt[int(data[idx])] += 1
        idx += 1

    del data

    # If the same vertex appears in both sequences, those pairs cost 0.
    # Under the stated guarantee this loop is a no-op, but it keeps the
    # invariant "each component has only one unmatched color" robust.
    for i in range(1, N + 1):
        ai = a_cnt[i]
        bi = b_cnt[i]
        if ai and bi:
            if ai < bi:
                a_cnt[i] = 0
                b_cnt[i] = bi - ai
            else:
                a_cnt[i] = ai - bi
                b_cnt[i] = 0

    edges.sort()

    parent = list(range(N + 1))
    size = [1] * (N + 1)
    ans = 0

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue

        if size[ru] < size[rv]:
            ru, rv = rv, ru

        a = a_cnt[ru] + a_cnt[rv]
        b = b_cnt[ru] + b_cnt[rv]

        if a < b:
            ans += a * w
            b -= a
            a = 0
        else:
            ans += b * w
            a -= b
            b = 0

        parent[rv] = ru
        size[ru] += size[rv]
        a_cnt[ru] = a
        b_cnt[ru] = b
        a_cnt[rv] = 0
        b_cnt[rv] = 0

    print(ans)


if __name__ == "__main__":
    main()