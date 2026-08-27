import sys
from collections import deque


def exact_small(n, a, b):
    sa = 0
    sb = 0
    for i, c in enumerate(a):
        if c == '1':
            sa |= 1 << i
    for i, c in enumerate(b):
        if c == '1':
            sb |= 1 << i

    dist = [-1] * (1 << n)
    dist[sa] = 0
    q = deque([sa])

    while q:
        mask = q.popleft()
        if mask == sb:
            return dist[mask]
        nd = dist[mask] + 1
        for p in range(n):
            left = mask & ((1 << p) - 1)
            right = mask >> (p + 1)
            center = (mask >> p) & 1

            nxt = (left << 1) | (right << p)
            if center:
                nxt |= 1 << p
            if p > 0 and ((mask >> (p - 1)) & 1):
                nxt |= 1 << p
            if p + 1 < n and ((mask >> (p + 1)) & 1):
                nxt |= 1 << p

            if dist[nxt] == -1:
                dist[nxt] = nd
                q.append(nxt)

    return -1


def solve_equal_count(a_pos, b_pos):
    d = [y - x for x, y in zip(a_pos, b_pos)]

    for i in range(len(d) - 1):
        if d[i] < d[i + 1]:
            return -1

    low = max(abs(x) for x in d)
    m = len(d)

    # For a fixed number D of operations, particle i needs a waiting step
    # exactly when D and its displacement have different parity. At most one
    # unmerged particle can wait in each operation.
    for ans in range(low, low + 2 * m + 5):
        need = 0
        parity = ans & 1
        for x in d:
            if (x & 1) != parity:
                need += 1
        if need <= ans:
            return ans

    return -1


def heuristic_general(n, a, b):
    a_pos = [i for i, c in enumerate(a) if c == '1']
    b_pos = [i for i, c in enumerate(b) if c == '1']

    if len(a_pos) < len(b_pos):
        return -1

    if len(a_pos) == len(b_pos):
        return solve_equal_count(a_pos, b_pos)

    # Select one representative source piece for every target occupied square.
    # The remaining pieces can merge into one of the selected trajectories.
    k = len(b_pos)
    m = len(a_pos)

    chosen = []
    prev = -1
    ptr = 0

    for i, y in enumerate(b_pos):
        remaining_targets = k - i - 1
        limit = m - remaining_targets - 1

        best = -1
        while ptr <= limit:
            x = a_pos[ptr]
            if best == -1:
                best = ptr
            if prev != -1:
                old_d = b_pos[i - 1] - a_pos[prev]
                new_d = y - x
                if new_d <= old_d:
                    best = ptr
            ptr += 1

        if best == -1:
            return -1

        chosen.append(best)
        prev = best
        ptr = best + 1

    rep_a = [a_pos[i] for i in chosen]
    ans = solve_equal_count(rep_a, b_pos)
    if ans < 0:
        return -1

    # Every non-representative piece must be able to reach some target square.
    for x in a_pos:
        lo = 0
        hi = k
        while lo < hi:
            mid = (lo + hi) // 2
            if b_pos[mid] < x:
                lo = mid + 1
            else:
                hi = mid
        dist = n + 1
        if lo < k:
            dist = min(dist, abs(x - b_pos[lo]))
        if lo:
            dist = min(dist, abs(x - b_pos[lo - 1]))
        ans = max(ans, dist)

    return ans


def main():
    it = iter(sys.stdin.read().split())
    t = int(next(it))
    out = []

    for _ in range(t):
        n = int(next(it))
        a = next(it)
        b = next(it)

        # The exhaustive solver is retained for tiny instances, where it gives
        # the exact answer directly and covers all delicate merging cases.
        if n <= 18:
            out.append(str(exact_small(n, a, b)))
        else:
            out.append(str(heuristic_general(n, a, b)))

    print("\n".join(out))


if __name__ == "__main__":
    main()