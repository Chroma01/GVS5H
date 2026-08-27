import sys
from collections import deque

def solve():
    input = sys.stdin.readline
    n = int(input())
    graph = [input().strip() for _ in range(n)]

    # in_masks[c][v]: bitmask of vertices u with edge u -> v labeled c
    # out_masks[c][u]: bitmask of vertices v with edge u -> v labeled c
    in_masks = [[0] * n for _ in range(26)]
    out_masks = [[0] * n for _ in range(26)]

    for u in range(n):
        row = graph[u]
        for v, ch in enumerate(row):
            if ch != '-':
                c = ord(ch) - ord('a')
                out_masks[c][u] |= 1 << v
                in_masks[c][v] |= 1 << u

    def bfs(is_odd):
        dist = [-1] * (n * n)
        seen_rows = [0] * n
        q = deque()

        if is_odd:
            # Every single edge is an odd-length palindrome center.
            for u in range(n):
                mask = 0
                for c in range(26):
                    mask |= out_masks[c][u]
                seen_rows[u] = mask
                while mask:
                    bit = mask & -mask
                    v = bit.bit_length() - 1
                    state = u * n + v
                    dist[state] = 0
                    q.append(state)
                    mask -= bit
        else:
            # Every vertex is an empty-string (even-length) palindrome center.
            for u in range(n):
                seen_rows[u] |= 1 << u
                state = u * n + u
                dist[state] = 0
                q.append(state)

        while q:
            state = q.popleft()
            u, v = divmod(state, n)
            next_d = dist[state] + 1

            for c in range(26):
                predecessors = in_masks[c][u]
                successors = out_masks[c][v]
                if predecessors == 0 or successors == 0:
                    continue

                pm = predecessors
                while pm:
                    bit_u = pm & -pm
                    a = bit_u.bit_length() - 1

                    new_vertices = successors & ~seen_rows[a]
                    if new_vertices:
                        seen_rows[a] |= new_vertices
                        bm = new_vertices
                        base = a * n
                        while bm:
                            bit_v = bm & -bm
                            b = bit_v.bit_length() - 1
                            nxt = base + b
                            dist[nxt] = next_d
                            q.append(nxt)
                            bm -= bit_v

                    pm -= bit_u

        return dist

    even_layers = bfs(False)
    odd_layers = bfs(True)

    out = []
    for i in range(n):
        row = []
        base = i * n
        for j in range(n):
            state = base + j
            ans = -1
            if even_layers[state] != -1:
                ans = 2 * even_layers[state]
            if odd_layers[state] != -1:
                odd_length = 2 * odd_layers[state] + 1
                if ans == -1 or odd_length < ans:
                    ans = odd_length
            row.append(str(ans))
        out.append(" ".join(row))

    print("\n".join(out))

if __name__ == "__main__":
    solve()