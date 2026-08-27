import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M = data[0], data[1]
    adj = [[] for _ in range(N)]
    max_z = 0
    idx = 2

    for _ in range(M):
        x = data[idx] - 1
        y = data[idx + 1] - 1
        z = data[idx + 2]
        idx += 3
        if z > max_z:
            max_z = z
        adj[x].append((y, z))
        adj[y].append((x, z))

    del data

    B = max(1, max_z.bit_length())
    bit_range = range(B)

    pot = [-1] * N
    ans = [0] * N

    for s in range(N):
        if pot[s] != -1:
            continue

        if not adj[s]:
            pot[s] = 0
            ans[s] = 0
            continue

        pot[s] = 0
        stack = [s]
        comp = []
        cnt = [0] * B

        while stack:
            u = stack.pop()
            comp.append(u)
            d = pot[u]

            if d:
                x = d
                for b in bit_range:
                    cnt[b] += x & 1
                    x >>= 1

            for v, z in adj[u]:
                nd = d ^ z
                if pot[v] == -1:
                    pot[v] = nd
                    stack.append(v)
                elif pot[v] != nd:
                    sys.stdout.write("-1\n")
                    return

        size = len(comp)
        c = 0
        for b in bit_range:
            if cnt[b] * 2 > size:
                c |= 1 << b

        for v in comp:
            ans[v] = c ^ pot[v]

    sys.stdout.write(" ".join(map(str, ans)) + "\n")


if __name__ == "__main__":
    solve()