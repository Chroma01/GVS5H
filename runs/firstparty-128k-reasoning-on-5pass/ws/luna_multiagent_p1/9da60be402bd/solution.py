import sys


def solve():
    input = sys.stdin.readline
    n = int(input())
    c = [input().strip() for _ in range(n)]

    # in_by_char[x][ch] contains all u such that u -> x has label ch.
    in_by_char = [[[] for _ in range(26)] for _ in range(n)]

    # out_mask[ch][y] is the bitmask of all v such that y -> v has label ch.
    out_mask = [[0] * n for _ in range(26)]

    edges = []
    for u in range(n):
        for v, ch in enumerate(c[u]):
            if ch != '-':
                k = ord(ch) - 97
                edges.append((u, v))
                in_by_char[v][k].append(u)
                out_mask[k][u] |= 1 << v

    total = n * n
    inf = 10**9
    dist = [inf] * total
    buckets = {}

    # Empty paths.
    for i in range(n):
        idx = i * n + i
        dist[idx] = 0
    buckets[0] = [i * n + i for i in range(n)]

    # One-edge palindromes.
    for u, v in edges:
        idx = u * n + v
        if dist[idx] > 1:
            dist[idx] = 1
            buckets.setdefault(1, []).append(idx)

    current = 0
    remaining = len(buckets)

    while remaining:
        while current not in buckets:
            current += 1
        active = buckets.pop(current)
        remaining -= 1
        nd = current + 2

        # For each character and outer starting vertex u, aggregate all
        # possible inner ending vertices y reachable from current states.
        aggregates = [0] * (26 * n)
        touched = []

        for state in active:
            x, y = divmod(state, n)
            bit_y = 1 << y
            for ch in range(26):
                for u in in_by_char[x][ch]:
                    pos = ch * n + u
                    if aggregates[pos] == 0:
                        touched.append(pos)
                    aggregates[pos] |= bit_y

        new_states = []

        for pos in touched:
            y_mask = aggregates[pos]
            ch, u = divmod(pos, n)

            # Convert the set of possible y values into possible ending
            # vertices v using edges y -> v of the same character.
            v_mask = 0
            mask = y_mask
            while mask:
                low = mask & -mask
                y = low.bit_length() - 1
                v_mask |= out_mask[ch][y]
                mask ^= low

            while v_mask:
                low = v_mask & -v_mask
                v = low.bit_length() - 1
                idx = u * n + v
                if dist[idx] == inf:
                    dist[idx] = nd
                    new_states.append(idx)
                v_mask ^= low

        if new_states:
            buckets.setdefault(nd, []).extend(new_states)
            remaining += 1

    out = []
    for i in range(n):
        row = []
        base = i * n
        for j in range(n):
            value = dist[base + j]
            row.append(str(-1 if value == inf else value))
        out.append(" ".join(row))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()