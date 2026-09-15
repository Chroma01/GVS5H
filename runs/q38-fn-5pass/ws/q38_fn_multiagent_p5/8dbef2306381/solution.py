import sys
import heapq
from bisect import bisect_right


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M, A, B = data[0], data[1], data[2], data[3]

    # Merge adjacent/overlapping bad intervals.
    bad = []
    pos = 4
    for _ in range(M):
        L = data[pos]
        R = data[pos + 1]
        pos += 2
        if bad and L <= bad[-1][1] + 1:
            if R > bad[-1][1]:
                bad[-1][1] = R
        else:
            bad.append([L, R])

    # Build maximal safe intervals.
    intervals = []
    prev = 1
    for L, R in bad:
        if prev <= L - 1:
            intervals.append((prev, L - 1))
        prev = R + 1
    if prev <= N:
        intervals.append((prev, N))

    K = len(intervals)
    starts = [s for s, _ in intervals]
    ends = [e for _, e in intervals]

    INF = 10**30
    steps = list(range(A, B + 1))

    # Shortest total jump length to change residue modulo A.
    offset = [[INF] * A for _ in range(A)]
    for src in range(A):
        dist = [INF] * A
        dist[src] = 0
        heap = [(0, src)]
        while heap:
            d, u = heapq.heappop(heap)
            if d != dist[u]:
                continue
            for st in steps:
                v = (u + st) % A
                nd = d + st
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(heap, (nd, v))
        offset[src] = dist

    offset_pairs = []
    for src in range(A):
        pairs = []
        for r, off in enumerate(offset[src]):
            if off < INF:
                pairs.append((r, off))
        offset_pairs.append(pairs)

    # For each interval and offset 1..B, the safe interval containing end+offset.
    jump_target = []
    for e in ends:
        arr = [-1] * (B + 1)
        for off in range(1, B + 1):
            q = e + off
            if q > N:
                break
            j = bisect_right(starts, q) - 1
            if j >= 0 and q <= ends[j]:
                arr[off] = j
        jump_target.append(arr)

    # entries[i][r] = minimum reachable square in interval i with residue r mod A.
    entries = [[INF] * A for _ in range(K)]
    if K:
        entries[0][1 % A] = 1

    def close(entry, end):
        """Expand entry minima to all reachable positions inside one safe interval."""
        dist = [INF] * A
        for s, es in enumerate(entry):
            if es == INF or es > end:
                continue
            for r, off in offset_pairs[s]:
                val = es + off
                if val <= end and val < dist[r]:
                    dist[r] = val
        return dist

    for idx in range(K):
        entry = entries[idx]
        if min(entry) == INF:
            continue

        s, e = intervals[idx]
        dist = close(entry, e)
        jt = jump_target[idx]

        # A jump leaving this interval lands at q = e + off, 1 <= off <= B.
        for off in range(1, B + 1):
            t = jt[off]
            if t == -1:
                continue

            q = e + off
            qr = q % A
            ent_t = entries[t]

            # If a smaller same-residue entry already exists, it can simulate q by +A steps.
            if q >= ent_t[qr]:
                continue

            # Need p = q - step, with step in [A, B], p in [s, e].
            start_step = A if A > off else off
            if start_step > B:
                continue

            end_step = B
            max_step = q - s
            if end_step > max_step:
                end_step = max_step

            if start_step > end_step:
                continue

            for step in range(start_step, end_step + 1):
                p = q - step
                if p >= dist[p % A]:
                    ent_t[qr] = q
                    break

    if K == 0:
        print("No")
        return

    entry = entries[-1]
    if min(entry) == INF:
        print("No")
    else:
        dist = close(entry, intervals[-1][1])
        print("Yes" if N >= dist[N % A] else "No")


if __name__ == "__main__":
    solve()