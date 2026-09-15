import sys
from collections import deque


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    rows = data[1:1 + N]

    size = N * N
    bits = [1 << i for i in range(N)]
    full = (1 << N) - 1

    # in_bits[u][c]: bitset of vertices p with edge p -> u labeled c
    # out_bits[v][c]: bitset of vertices q with edge v -> q labeled c
    in_bits = [[0] * 26 for _ in range(N)]
    out_bits = [[0] * 26 for _ in range(N)]

    # dist[u*N+v] = shortest palindrome length from u to v
    dist = [-1] * size

    # row_unvis[p] is a bitset of q such that state (p, q) is not discovered yet
    row_unvis = [full] * N

    queue = deque()
    visited = 0

    # Base case 1: empty paths, length 0 from i to i.
    for i in range(N):
        st = i * N + i
        dist[st] = 0
        row_unvis[i] &= ~bits[i]
        queue.append(st)
        visited += 1

    # Base case 2: single edges, length 1.
    # Also build label bitsets while parsing.
    for i, row in enumerate(rows):
        biti = bits[i]
        base = i * N
        for j, ch in enumerate(row):
            if ch != 45:  # ord('-') == 45
                c = ch - 97  # ord('a') == 97
                bitj = bits[j]

                out_bits[i][c] |= bitj
                in_bits[j][c] |= biti

                st = base + j
                if dist[st] == -1:
                    dist[st] = 1
                    row_unvis[i] &= ~bitj
                    queue.append(st)
                    visited += 1

    remaining = size - visited

    if remaining:
        # Labels that appear on incoming edges to each vertex.
        in_labels = [[] for _ in range(N)]
        for u in range(N):
            row = in_bits[u]
            lab = in_labels[u]
            for c in range(26):
                if row[c]:
                    lab.append(c)

        # Local aliases for speed.
        in_bits_l = in_bits
        out_bits_l = out_bits
        in_labels_l = in_labels
        row_unvis_l = row_unvis
        dist_l = dist
        N_l = N
        append = queue.append
        popleft = queue.popleft

        # Multi-source BFS.
        # Queue initially has all distance-0 states, then all distance-1 states.
        # Every transition adds 2, so FIFO order remains nondecreasing.
        while queue and remaining:
            st = popleft()
            u = st // N_l
            labels = in_labels_l[u]
            if not labels:
                continue

            v = st - u * N_l
            nd = dist_l[st] + 2

            out_bits_v = out_bits_l[v]
            in_bits_u = in_bits_l[u]

            for c in labels:
                succ = out_bits_v[c]
                if not succ:
                    continue

                pred = in_bits_u[c]
                bits_iter = pred

                # Iterate only predecessors p. For each p, all valid q are found
                # by one bitset intersection.
                while bits_iter:
                    lsb = bits_iter & -bits_iter
                    p = lsb.bit_length() - 1

                    newbits = succ & row_unvis_l[p]
                    if newbits:
                        row_unvis_l[p] &= ~newbits
                        p_base = p * N_l

                        nb = newbits
                        while nb:
                            lsb2 = nb & -nb
                            qv = lsb2.bit_length() - 1
                            nst = p_base + qv

                            dist_l[nst] = nd
                            append(nst)
                            remaining -= 1

                            nb ^= lsb2

                        if remaining == 0:
                            break

                    bits_iter ^= lsb

                if remaining == 0:
                    break

    out_lines = []
    for i in range(N):
        base = i * N
        out_lines.append(' '.join(map(str, dist[base:base + N])))

    sys.stdout.write('\n'.join(out_lines))


if __name__ == "__main__":
    solve()