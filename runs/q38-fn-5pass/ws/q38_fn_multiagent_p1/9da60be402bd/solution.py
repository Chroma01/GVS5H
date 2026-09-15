import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    rows = data[1:1 + n]

    # out_masks[c][u]: bitset of vertices v such that edge u -> v has label c
    out_masks = [[0] * n for _ in range(26)]

    # in_edges[v]: list of (u, c) such that edge u -> v has label c
    in_edges = [[] for _ in range(n)]

    edges = []
    for i in range(n):
        row = rows[i]
        for j in range(n):
            ch = row[j]
            if ch != '-':
                c = ord(ch) - 97
                out_masks[c][i] |= 1 << j
                in_edges[j].append((i, c))
                edges.append((i, j))

    full = (1 << n) - 1
    dist = [[-1] * n for _ in range(n)]

    # unvisited[u] is a bitset of vertices v whose dist[u][v] is still unknown.
    unvisited = [full] * n

    queue = deque()
    remaining = n * n

    # Centers of even-length palindromes: empty paths.
    for i in range(n):
        dist[i][i] = 0
        unvisited[i] &= ~(1 << i)
        queue.append(i * n + i)
        remaining -= 1

    # Centers of odd-length palindromes: single edges.
    # Self-loop centers are unnecessary because dist[i][i] = 0 dominates them.
    for i, j in edges:
        if dist[i][j] == -1:
            dist[i][j] = 1
            unvisited[i] &= ~(1 << j)
            queue.append(i * n + j)
            remaining -= 1

    append = queue.append
    popleft = queue.popleft

    # Multi-source BFS. All transitions add 2 to the length.
    # Initial queue order is all distance 0, then all distance 1, so FIFO order
    # processes distances nondecreasingly: 0, 1, 2, 3, ...
    while queue and remaining:
        code = popleft()
        x = code // n
        y = code - x * n
        nd = dist[x][y] + 2

        # Extend palindrome outward:
        # need p -> x and y -> q with the same label.
        for p, c in in_edges[x]:
            up = unvisited[p]
            if not up:
                continue

            mask = out_masks[c][y] & up
            if not mask:
                continue

            # All states (p, q) for q in mask are newly reached.
            unvisited[p] ^= mask
            base = p * n
            m = mask
            while m:
                lsb = m & -m
                v = lsb.bit_length() - 1
                dist[p][v] = nd
                append(base + v)
                remaining -= 1
                m ^= lsb

            if remaining == 0:
                break

    sys.stdout.write('\n'.join(' '.join(map(str, row)) for row in dist) + '\n')


if __name__ == '__main__':
    main()