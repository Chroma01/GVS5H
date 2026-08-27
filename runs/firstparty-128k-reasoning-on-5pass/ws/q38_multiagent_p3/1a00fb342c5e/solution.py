import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    M = int(data[1])

    if M == 0:
        sys.stdout.write('0 ' * (N - 1) + '0\n')
        return

    adj = [[] for _ in range(N)]
    or_z = 0
    idx = 2

    for _ in range(M):
        x = int(data[idx]) - 1
        y = int(data[idx + 1]) - 1
        z = int(data[idx + 2])
        idx += 3

        or_z |= z
        adj[x].append((y, z))
        if x != y:
            adj[y].append((x, z))

    del data

    B = max(1, or_z.bit_length())
    pot = [-1] * N
    ans = [0] * N
    range_B = range(B)

    for s in range(N):
        if pot[s] != -1:
            continue

        if not adj[s]:
            pot[s] = 0
            continue

        pot[s] = 0
        stack = [s]
        comp = [s]

        while stack:
            u = stack.pop()
            pu = pot[u]

            for v, z in adj[u]:
                pv = pot[v]
                if pv == -1:
                    pv = pu ^ z
                    pot[v] = pv
                    stack.append(v)
                    comp.append(v)
                elif (pu ^ pv) != z:
                    sys.stdout.write('-1\n')
                    return

        if len(comp) == 1:
            ans[s] = 0
            continue

        counts = [0] * B
        for p in comp:
            if p:
                x = p
                for b in range_B:
                    counts[b] += x & 1
                    x >>= 1

        half = len(comp) // 2
        mask = 0
        for b in range_B:
            if counts[b] > half:
                mask |= 1 << b

        for v in comp:
            ans[v] = pot[v] ^ mask

    sys.stdout.write(' '.join(map(str, ans)) + '\n')


if __name__ == '__main__':
    solve()