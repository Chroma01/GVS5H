import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N = data[0]
    M = data[1]
    if M == 0:
        sys.stdout.write(' '.join(['0'] * N))
        return
    adj = [[] for _ in range(N)]
    idx = 2
    max_z = 0
    for _ in range(M):
        x = data[idx] - 1
        y = data[idx+1] - 1
        z = data[idx+2]
        idx += 3
        adj[x].append((y, z))
        adj[y].append((x, z))
        if z > max_z:
            max_z = z
    # If all z zero, all zeros is optimal and consistent.
    if max_z == 0:
        sys.stdout.write(' '.join(['0'] * N))
        return
    MAXB = max(31, max_z.bit_length())
    bit_range = range(MAXB)
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
        while stack:
            v = stack.pop()
            comp.append(v)
            pv = pot[v]
            for to, w in adj[v]:
                pt = pot[to]
                if pt == -1:
                    pot[to] = pv ^ w
                    stack.append(to)
                elif (pv ^ pt) != w:
                    sys.stdout.write('-1\n')
                    return
        size = len(comp)
        if size == 1:
            ans[comp[0]] = 0
            continue
        cnt = [0] * MAXB
        for p in comp:
            # p is non-negative
            for b in bit_range:
                cnt[b] += (p >> b) & 1
        mask = 0
        for b in bit_range:
            if cnt[b] > size - cnt[b]:
                mask |= 1 << b
        for v in comp:
            ans[v] = pot[v] ^ mask
    sys.stdout.write(' '.join(map(str, ans)))

if __name__ == '__main__':
    solve()