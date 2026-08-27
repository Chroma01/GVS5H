import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))

    adj = [[] for _ in range(N)]
    for _ in range(M):
        x = int(next(it)) - 1
        y = int(next(it)) - 1
        z = int(next(it))
        adj[x].append((y, z))
        if x != y:
            adj[y].append((x, z))

    del data, it

    visited = [False] * N
    pot = [0] * N
    ans = [0] * N
    BITS = 31

    for s in range(N):
        if visited[s]:
            continue

        if not adj[s]:
            visited[s] = True
            continue

        visited[s] = True
        pot[s] = 0
        comp = [s]
        stack = [s]

        while stack:
            v = stack.pop()
            pv = pot[v]
            for to, z in adj[v]:
                if not visited[to]:
                    visited[to] = True
                    p = pv ^ z
                    pot[to] = p
                    comp.append(to)
                    stack.append(to)
                else:
                    if (pv ^ pot[to]) != z:
                        sys.stdout.write("-1\n")
                        return

        size = len(comp)
        if size == 1:
            ans[s] = 0
            continue

        counts = [0] * BITS
        for v in comp:
            x = pot[v]
            k = 0
            while x:
                counts[k] += x & 1
                x >>= 1
                k += 1

        c = 0
        for k, cnt in enumerate(counts):
            if cnt * 2 > size:
                c |= 1 << k

        for v in comp:
            ans[v] = pot[v] ^ c

    sys.stdout.write(" ".join(map(str, ans)) + "\n")

if __name__ == "__main__":
    solve()