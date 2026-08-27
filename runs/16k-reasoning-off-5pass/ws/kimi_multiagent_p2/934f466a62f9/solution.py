import sys
from collections import defaultdict


def solve_case(v, K):
    N = len(v)
    M = [max(v[i]) for i in range(N)]
    order = sorted(range(N), key=lambda i: -M[i])
    twoK = 2 * K
    sel = order[:twoK]
    inT = [False] * N
    U = 0
    assign = [0] * N
    cnt = [0, 0, 0]
    for i in sel:
        inT[i] = True
        U += M[i]
        if v[i][0] == M[i]:
            a = 0
        elif v[i][1] == M[i]:
            a = 1
        else:
            a = 2
        assign[i] = a
        cnt[a] += 1
    odds = [c for c in range(3) if cnt[c] % 2 == 1]
    if not odds:
        return U
    P, Q = odds[0], odds[1]
    R = 3 - P - Q
    INF = float('inf')

    def mask_key(a, b):
        return (a, b) if a < b else (b, a)

    cand = {mask_key(P, Q): [], mask_key(P, R): [], mask_key(Q, R): []}
    rec = defaultdict(list)
    on_cakes = [[], [], []]
    for i in sel:
        a = assign[i]
        on_cakes[a].append((M[i], i))
        for b in range(3):
            if b != a:
                rec[(a, b)].append((M[i] - v[i][b], i))
    out_cakes = [[], [], []]
    for j in range(N):
        if not inT[j]:
            for b in range(3):
                out_cakes[b].append((v[j][b], j))
    KEEP = 6
    for b in range(3):
        out_cakes[b].sort(key=lambda t: -t[0])
        out_cakes[b] = out_cakes[b][:KEEP]
    for a in range(3):
        on_cakes[a].sort(key=lambda t: t[0])
        on_cakes[a] = on_cakes[a][:KEEP]
    for key in rec:
        rec[key].sort()
        rec[key] = rec[key][:KEEP]
    masks = [mask_key(P, Q), mask_key(P, R), mask_key(Q, R)]
    for mk in masks:
        a, b = mk
        lst = cand[mk]
        for cost, i in rec[(a, b)]:
            lst.append((cost, (i,)))
        for cost, i in rec[(b, a)]:
            lst.append((cost, (i,)))
        for mi, i in on_cakes[a]:
            for vj, j in out_cakes[b]:
                lst.append((mi - vj, (i, j)))
        for mi, i in on_cakes[b]:
            for vj, j in out_cakes[a]:
                lst.append((mi - vj, (i, j)))
        lst.sort(key=lambda t: t[0])
        cand[mk] = lst[:KEEP]
    best = INF
    for cost, ids in cand[mask_key(P, Q)]:
        if cost < best:
            best = cost
    for c1, ids1 in cand[mask_key(P, R)]:
        if c1 >= best:
            continue
        s1 = set(ids1)
        for c2, ids2 in cand[mask_key(Q, R)]:
            if c1 + c2 >= best:
                break
            if s1.isdisjoint(ids2):
                best = c1 + c2
                break
    return U - best


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    T = int(data[pos]); pos += 1
    out = []
    for _ in range(T):
        N = int(data[pos]); K = int(data[pos + 1]); pos += 2
        v = []
        for _ in range(N):
            x = int(data[pos]); y = int(data[pos + 1]); z = int(data[pos + 2])
            pos += 3
            v.append((x, y, z))
        out.append(str(solve_case(v, K)))
    sys.stdout.write("\n".join(out) + "\n")


main()