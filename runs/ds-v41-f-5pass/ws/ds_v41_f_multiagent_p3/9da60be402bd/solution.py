import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    grid = data[1:1 + N]

    # pred_lists[c][u] = list of p such that edge p->u has label c
    # succ[c][u]      = bitmask of q such that edge u->q has label c
    pred_lists = [[[] for _ in range(N)] for _ in range(26)]
    succ = [[0] * N for _ in range(26)]

    for i in range(N):
        row = grid[i]
        for j in range(N):
            ch = row[j]
            if ch != 45:  # '-'
                c = ch - 97
                pred_lists[c][j].append(i)
                succ[c][i] |= (1 << j)

    # For each left endpoint u, only keep non-empty label buckets.
    pred_by_u = [None] * N
    for u in range(N):
        lst = []
        for c in range(26):
            pl = pred_lists[c][u]
            if pl:
                lst.append((c, pl))
        pred_by_u[u] = lst

    dist = [[-1] * N for _ in range(N)]
    vis = [0] * N            # vis[p] = bitmask of q already discovered for pair (p,q)
    dq = deque()

    # even base: empty palindrome
    for i in range(N):
        dist[i][i] = 0
        vis[i] = 1 << i
        dq.append((i, i))

    # odd base: single edge
    for i in range(N):
        row = grid[i]
        vi = vis[i]
        for j in range(N):
            if row[j] != 45 and dist[i][j] == -1:
                dist[i][j] = 1
                vi |= (1 << j)
                dq.append((i, j))
        vis[i] = vi

    while dq:
        u, v = dq.popleft()
        nd = dist[u][v] + 2
        su = pred_by_u[u]
        if not su:
            continue
        for c, plist in su:
            sv = succ[c][v]
            if not sv:
                continue
            for p in plist:                      # prepend edge p->u (label c)
                newbits = sv & ~vis[p]           # append edge v->q (label c)
                if newbits:
                    vis[p] |= sv
                    while newbits:
                        low = newbits & -newbits
                        q = low.bit_length() - 1
                        newbits ^= low
                        dist[p][q] = nd
                        dq.append((p, q))

    out = []
    for i in range(N):
        out.append(' '.join(map(str, dist[i])))
    sys.stdout.write('\n'.join(out) + '\n')


main()