import sys
import heapq


def solve():
    input = sys.stdin.readline
    n = int(input())
    graph = [input().strip() for _ in range(n)]

    incoming = [[[] for _ in range(26)] for _ in range(n)]
    outgoing_mask = [[0] * 26 for _ in range(n)]

    for i in range(n):
        row = graph[i]
        for j, ch in enumerate(row):
            if ch != '-':
                c = ord(ch) - 97
                incoming[j][c].append(i)
                outgoing_mask[i][c] |= 1 << j

    total = n * n
    inf = 10**18
    dist = [inf] * total
    heap = []

    # Buckets are used to track all states whose current tentative
    # distance is at most the current relaxation threshold.
    buckets = [[] for _ in range(2 * total + 2)]

    for i in range(n):
        state = i * n + i
        dist[state] = 0
        heapq.heappush(heap, (0, state))
        buckets[0].append(state)

    for i in range(n):
        for j, ch in enumerate(graph[i]):
            if ch != '-':
                state = i * n + j
                if dist[state] > 1:
                    dist[state] = 1
                    heapq.heappush(heap, (1, state))
                    buckets[1].append(state)

    blocked = [0] * n
    bucket_pointer = 0

    while heap:
        d, state = heapq.heappop(heap)
        if dist[state] != d:
            continue

        # Any state with tentative distance <= d + 2 cannot be improved
        # by the current state's two-edge extension.
        threshold = d + 2
        while bucket_pointer <= threshold:
            for sid in buckets[bucket_pointer]:
                x = sid // n
                y = sid - x * n
                blocked[x] |= 1 << y
            bucket_pointer += 1

        u = state // n
        v = state - u * n
        nd = d + 2

        for c in range(26):
            targets = outgoing_mask[v][c]
            if targets == 0:
                continue

            for x in incoming[u][c]:
                mask = targets & ~blocked[x]
                while mask:
                    bit = mask & -mask
                    y = bit.bit_length() - 1
                    sid = x * n + y

                    dist[sid] = nd
                    blocked[x] |= bit
                    heapq.heappush(heap, (nd, sid))
                    buckets[nd].append(sid)

                    mask ^= bit

    out = []
    for i in range(n):
        row = []
        for j in range(n):
            value = dist[i * n + j]
            row.append(str(value if value != inf else -1))
        out.append(" ".join(row))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()