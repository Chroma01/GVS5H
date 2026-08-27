import sys
import heapq


def solve():
    input = sys.stdin.readline
    n = int(input())
    grid = [input().strip() for _ in range(n)]

    incoming = [[[] for _ in range(n)] for _ in range(26)]
    outgoing = [[[] for _ in range(n)] for _ in range(26)]

    dist = [10**18] * (n * n)
    heap = []
    finite_count = 0

    for i in range(n):
        idx = i * n + i
        dist[idx] = 0
        heapq.heappush(heap, (0, idx))

    for i in range(n):
        row = grid[i]
        for j, ch in enumerate(row):
            if ch == '-':
                continue
            c = ord(ch) - 97
            outgoing[c][i].append(j)
            incoming[c][j].append(i)

            idx = i * n + j
            if dist[idx] == 10**18:
                dist[idx] = 1
                finite_count += 1
                heapq.heappush(heap, (1, idx))

    finite_count += n

    while heap:
        d, state = heapq.heappop(heap)
        if dist[state] != d:
            continue

        x, y = divmod(state, n)
        nd = d + 2

        # Once every pair is reachable, no transition can improve a state
        # whose current distance is at most nd.
        all_reachable = finite_count == n * n

        for c in range(26):
            left = incoming[c][x]
            right = outgoing[c][y]
            if not left or not right:
                continue

            if all_reachable:
                # Since all distances are finite, this coarse bound safely
                # skips the Cartesian product when no value can improve.
                minimum_possible_improvement = False
                for u in left:
                    base = u * n
                    for v in right:
                        if dist[base + v] > nd:
                            minimum_possible_improvement = True
                            break
                    if minimum_possible_improvement:
                        break
                if not minimum_possible_improvement:
                    continue

            for u in left:
                base = u * n
                for v in right:
                    nxt = base + v
                    if dist[nxt] > nd:
                        if dist[nxt] == 10**18:
                            finite_count += 1
                        dist[nxt] = nd
                        heapq.heappush(heap, (nd, nxt))

    out = []
    for i in range(n):
        out.append(' '.join(
            '-1' if dist[i * n + j] == 10**18 else str(dist[i * n + j])
            for j in range(n)
        ))
    sys.stdout.write('\n'.join(out))


if __name__ == "__main__":
    solve()