import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    grid = data[1:1+N]

    pred = [[0] * N for _ in range(26)]
    succ = [[0] * N for _ in range(26)]

    for i in range(N):
        row = grid[i]
        for j, ch in enumerate(row):
            if ch != '-':
                c = ord(ch) - 97
                succ[c][i] |= 1 << j
                pred[c][j] |= 1 << i

    dist = [[-1] * N for _ in range(N)]
    row_mask = [0] * N
    q = deque()

    # length 0: empty path
    for i in range(N):
        dist[i][i] = 0
        row_mask[i] |= 1 << i
        q.append((i, i))

    # length 1: single edge
    for i in range(N):
        row = grid[i]
        for j, ch in enumerate(row):
            if ch != '-' and dist[i][j] == -1:
                dist[i][j] = 1
                row_mask[i] |= 1 << j
                q.append((i, j))

    while q:
        u, v = q.popleft()
        nd = dist[u][v] + 2

        for c in range(26):
            sm = succ[c][v]
            if not sm:
                continue
            pm = pred[c][u]
            if not pm:
                continue

            t = pm
            while t:
                lsb = t & -t
                x = lsb.bit_length() - 1
                t ^= lsb

                new = sm & ~row_mask[x]
                if new:
                    while new:
                        lsb2 = new & -new
                        y = lsb2.bit_length() - 1
                        new ^= lsb2
                        dist[x][y] = nd
                        row_mask[x] |= 1 << y
                        q.append((x, y))

    out = []
    for i in range(N):
        out.append(' '.join(str(dist[i][j]) for j in range(N)))
    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == '__main__':
    main()