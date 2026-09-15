import sys
from collections import deque


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return

    N = int(tokens[0])
    rows = tokens[1:1 + N]

    pred = [[[] for _ in range(26)] for _ in range(N)]
    succ_mask = [[0] * 26 for _ in range(N)]

    total = N * N
    full_mask = (1 << N) - 1
    dist = [-1] * total
    unvisited = [full_mask] * N
    q = deque()

    # Empty paths: distance 0 for (i, i).
    for i in range(N):
        idx = i * N + i
        dist[idx] = 0
        unvisited[i] &= ~(1 << i)
        q.append(idx)

    # Single-edge paths: distance 1 for every directed edge.
    for i, s in enumerate(rows):
        for j, ch in enumerate(s[:N]):
            if ch == '-':
                continue
            c = ord(ch) - 97
            pred[j][c].append(i)
            succ_mask[i][c] |= 1 << j

            idx = i * N + j
            if dist[idx] == -1:
                dist[idx] = 1
                unvisited[i] &= ~(1 << j)
                q.append(idx)

    pred_nonempty = [
        [(c, pred[u][c]) for c in range(26) if pred[u][c]]
        for u in range(N)
    ]

    append = q.append
    popleft = q.popleft
    dist_local = dist
    unvisited_local = unvisited
    succ_local = succ_mask
    N_local = N

    while q:
        idx = popleft()
        u, v = divmod(idx, N_local)
        nd = dist_local[idx] + 2

        for c, predecessors in pred_nonempty[u]:
            targets = succ_local[v][c]
            if not targets:
                continue

            for x in predecessors:
                m = unvisited_local[x] & targets
                if not m:
                    continue

                # Mark all newly reachable states with first endpoint x at once.
                unvisited_local[x] &= ~m
                bits = m
                base = x * N_local

                while bits:
                    lsb = bits & -bits
                    y = lsb.bit_length() - 1
                    nidx = base + y
                    dist_local[nidx] = nd
                    append(nidx)
                    bits ^= lsb

    out = []
    for i in range(N):
        base = i * N
        out.append(' '.join(str(dist[base + j]) for j in range(N)))

    sys.stdout.write('\n'.join(out))


if __name__ == "__main__":
    main()