import sys
from collections import deque

def solve():
    input = sys.stdin.readline
    n = int(input())
    graph = [input().strip() for _ in range(n)]

    incoming = [[0] * n for _ in range(26)]
    outgoing = [[0] * n for _ in range(26)]
    in_labels = [0] * n
    out_labels = [0] * n

    for i in range(n):
        row = graph[i]
        for j, ch in enumerate(row):
            if ch != '-':
                c = ord(ch) - ord('a')
                outgoing[c][i] |= 1 << j
                incoming[c][j] |= 1 << i
                out_labels[i] |= 1 << c
                in_labels[j] |= 1 << c

    dist = [[-1] * n for _ in range(n)]
    full_mask = (1 << n) - 1
    unvisited = [full_mask] * n
    q = deque()

    remaining = n * n

    # Empty palindrome: i -> i.
    for i in range(n):
        dist[i][i] = 0
        unvisited[i] &= ~(1 << i)
        q.append(i * n + i)
        remaining -= 1

    # One-edge palindrome: every direct edge.
    for i in range(n):
        for j, ch in enumerate(graph[i]):
            if ch != '-' and dist[i][j] == -1:
                dist[i][j] = 1
                unvisited[i] &= ~(1 << j)
                q.append(i * n + j)
                remaining -= 1

    # Queue order is nondecreasing in distance:
    # initial states have distances 0 and 1, and every transition adds 2.
    while q and remaining:
        state = q.popleft()
        u, v = divmod(state, n)
        nd = dist[u][v] + 2

        common = in_labels[u] & out_labels[v]
        while common:
            bit_c = common & -common
            c = bit_c.bit_length() - 1
            common -= bit_c

            # Choose a -> u and v -> b with the same label c.
            predecessors = incoming[c][u]
            successors = outgoing[c][v]

            while predecessors:
                bit_a = predecessors & -predecessors
                a = bit_a.bit_length() - 1
                predecessors -= bit_a

                candidates = successors & unvisited[a]
                while candidates:
                    bit_b = candidates & -candidates
                    b = bit_b.bit_length() - 1
                    candidates -= bit_b

                    dist[a][b] = nd
                    unvisited[a] &= ~bit_b
                    q.append(a * n + b)
                    remaining -= 1

                    if remaining == 0:
                        break
                if remaining == 0:
                    break
            if remaining == 0:
                break

    sys.stdout.write("\n".join(" ".join(map(str, row)) for row in dist))

if __name__ == "__main__":
    solve()