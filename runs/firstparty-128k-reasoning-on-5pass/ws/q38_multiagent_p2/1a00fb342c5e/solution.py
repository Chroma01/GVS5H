import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M = data[0], data[1]
    adj = [[] for _ in range(N)]
    p = 2
    for _ in range(M):
        x = data[p] - 1
        y = data[p + 1] - 1
        z = data[p + 2]
        p += 3
        adj[x].append((y, z))
        if x != y:
            adj[y].append((x, z))
    del data

    B = 32
    bits = range(B)
    comp = [-1] * N
    dist = [0] * N
    bases = []

    for s in range(N):
        if comp[s] != -1:
            continue

        if not adj[s]:
            comp[s] = len(bases)
            bases.append(0)
            continue

        cid = len(bases)
        comp[s] = cid
        stack = [s]
        size = 1
        cnt = [0] * B

        while stack:
            v = stack.pop()
            d = dist[v]

            x = d
            for b in bits:
                cnt[b] += x & 1
                x >>= 1

            for to, z in adj[v]:
                if comp[to] == -1:
                    comp[to] = cid
                    dist[to] = d ^ z
                    stack.append(to)
                    size += 1
                elif (d ^ dist[to]) != z:
                    print(-1)
                    return

        half = size // 2
        base = 0
        for b in bits:
            if cnt[b] > half:
                base |= 1 << b
        bases.append(base)

    ans = [str(dist[i] ^ bases[comp[i]]) for i in range(N)]
    sys.stdout.write(" ".join(ans) + "\n")

if __name__ == "__main__":
    main()