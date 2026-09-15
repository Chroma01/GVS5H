import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    rows = data[1:1 + N]

    INF = 10 ** 9
    succ = [[0] * N for _ in range(26)]
    pred = [[[] for _ in range(N)] for _ in range(26)]

    dist = [INF] * (N * N)
    vis0 = [0] * N
    vis1 = [0] * N
    fr0 = [0] * N
    fr1 = [0] * N

    for i in range(N):
        bit = 1 << i
        dist[i * N + i] = 0
        vis0[i] = bit
        fr0[i] = bit

    for i, row in enumerate(rows):
        base = i * N
        for j, ch in enumerate(row):
            if ch != 45:
                c = ch - 97
                bit = 1 << j
                succ[c][i] |= bit
                pred[c][j].append(i)
                if dist[base + j] > 1:
                    dist[base + j] = 1
                vis1[i] |= bit
                fr1[i] |= bit

    pred_info = [[] for _ in range(N)]
    for u in range(N):
        for c in range(26):
            if pred[c][u]:
                pred_info[u].append((c, pred[c][u]))

    def bfs(vis, fr, d):
        succ_l = succ
        pred_info_l = pred_info
        dist_l = dist
        N_l = N

        while True:
            active = [u for u, b in enumerate(fr) if b]
            if not active:
                return

            nxt = [0] * N_l
            nd = d + 2

            for u in active:
                B = fr[u]
                for c, plist in pred_info_l[u]:
                    sc = succ_l[c]
                    m = 0
                    BB = B
                    while BB:
                        lsb = BB & -BB
                        m |= sc[lsb.bit_length() - 1]
                        BB -= lsb

                    if m:
                        for x in plist:
                            add = m & ~vis[x]
                            if add:
                                vis[x] |= add
                                nxt[x] |= add
                                base = x * N_l
                                A = add
                                while A:
                                    lsb = A & -A
                                    idx = base + (lsb.bit_length() - 1)
                                    if dist_l[idx] > nd:
                                        dist_l[idx] = nd
                                    A -= lsb

            fr = nxt
            d = nd

    bfs(vis0, fr0, 0)
    bfs(vis1, fr1, 1)

    out = []
    for i in range(N):
        base = i * N
        out.append(' '.join(
            str(-1 if dist[base + j] >= INF else dist[base + j])
            for j in range(N)
        ))
    sys.stdout.write('\n'.join(out))

if __name__ == '__main__':
    main()