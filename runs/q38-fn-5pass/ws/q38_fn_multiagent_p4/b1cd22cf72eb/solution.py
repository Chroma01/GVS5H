import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    x = data[1]

    pairs = []
    append = pairs.append
    total = 0
    high = 10**30

    idx = 2
    for _ in range(n):
        u = data[idx]
        d = data[idx + 1]
        idx += 2
        append((u, d))
        s = u + d
        total += s
        if s < high:
            high = s

    del data

    first_u, first_d = pairs[0]
    tail = pairs[1:]
    del pairs

    def feasible(h: int, fu: int = first_u, fd: int = first_d,
                 tail_list: list = tail, x_limit: int = x) -> bool:
        # Possible final upper length of the first tooth.
        lo = h - fd
        if lo < 0:
            lo = 0
        hi = fu if fu < h else h

        if lo > hi:
            return False

        for u, d in tail_list:
            # Values reachable from the previous possible interval.
            lo -= x_limit
            hi += x_limit

            # Current tooth's own interval.
            cur_lo = h - d
            if cur_lo < 0:
                cur_lo = 0
            cur_hi = u if u < h else h

            # Intersect.
            if cur_lo > lo:
                lo = cur_lo
            if cur_hi < hi:
                hi = cur_hi

            if lo > hi:
                return False

        return True

    low = 0
    while low < high:
        mid = (low + high + 1) // 2
        if feasible(mid):
            low = mid
        else:
            high = mid - 1

    print(total - n * low)


if __name__ == "__main__":
    solve()