import sys


def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    A = int(next(it))
    B = int(next(it))

    intervals = []
    for _ in range(M):
        L = int(next(it))
        R = int(next(it))
        intervals.append((L, R))

    # Merge bad intervals that overlap or touch.
    intervals.sort()
    merged = []
    for L, R in intervals:
        if not merged or L > merged[-1][1] + 1:
            merged.append([L, R])
        else:
            if R > merged[-1][1]:
                merged[-1][1] = R

    # Maximal safe segments.
    segments = []
    cur = 1
    for L, R in merged:
        if cur <= L - 1:
            segments.append((cur, L - 1))
        cur = R + 1
    if cur <= N:
        segments.append((cur, N))

    S = len(segments)

    # The official constraints guarantee 1 and N are safe.
    # These checks are only for robustness.
    if (
        S == 0
        or not (segments[0][0] <= 1 <= segments[0][1])
        or not (segments[-1][0] <= N <= segments[-1][1])
    ):
        print("No")
        return

    INF = 10**30

    # Shortest total jump length to change residue modulo A.
    dist = [[INF] * A for _ in range(A)]
    for i in range(A):
        dist[i][i] = 0

    for d in range(A, B + 1):
        for u in range(A):
            v = (u + d) % A
            if d < dist[u][v]:
                dist[u][v] = d

    for k in range(A):
        dk = dist[k]
        for i in range(A):
            dik = dist[i][k]
            if dik == INF:
                continue
            di = dist[i]
            for j in range(A):
                nd = dik + dk[j]
                if nd < di[j]:
                    di[j] = nd

    trans = []
    for u in range(A):
        lst = []
        for v, d in enumerate(dist[u]):
            if d < INF:
                lst.append((v, d))
        trans.append(lst)

    # entries[i][r] = earliest reachable square in segment i with residue r.
    entries = [[INF] * A for _ in range(S)]
    entries[0][1 % A] = 1

    starts = [s for s, _ in segments]
    ends = [e for _, e in segments]

    last_closed = [INF] * A

    for idx, (l, r) in enumerate(segments):
        ent = entries[idx]

        # Close reachability inside this safe segment.
        closed = [INF] * A
        any_closed = False

        for u, base in enumerate(ent):
            if base == INF or base > r:
                continue
            for v, d in trans[u]:
                val = base + d
                if val <= r and val < closed[v]:
                    closed[v] = val
                    any_closed = True

        if idx == S - 1:
            last_closed = closed

        if not any_closed or idx == S - 1:
            continue

        # Only squares within B of the segment end can jump outside it.
        start_x = r - B + 1
        if start_x < l:
            start_x = l

        reachable_xs = []
        for x in range(start_x, r + 1):
            if closed[x % A] <= x:
                reachable_xs.append(x)

        if not reachable_xs:
            continue

        # For each offset 1..B after r, find the safe segment containing r+offset.
        land_seg = [-1] * (B + 1)
        p = idx + 1
        off_max = B
        if r + off_max > N:
            off_max = N - r

        for off in range(1, off_max + 1):
            y = r + off
            while p < S and ends[p] < y:
                p += 1
            if p < S and starts[p] <= y:
                land_seg[off] = p

        # Try all jumps that leave this segment.
        for x in reachable_xs:
            maxd = B
            rem = N - x
            if maxd > rem:
                maxd = rem

            # Need x + d > r to leave the current segment.
            start_d = A
            cross_d = r + 1 - x
            if start_d < cross_d:
                start_d = cross_d

            if start_d > maxd:
                continue

            for d in range(start_d, maxd + 1):
                off = x + d - r
                j = land_seg[off]
                if j != -1:
                    y = x + d
                    ry = y % A
                    if y < entries[j][ry]:
                        entries[j][ry] = y

    print("Yes" if last_closed[N % A] <= N else "No")


if __name__ == "__main__":
    solve()