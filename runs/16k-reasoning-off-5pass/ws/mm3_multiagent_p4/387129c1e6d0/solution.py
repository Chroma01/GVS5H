import sys
import bisect
from collections import defaultdict

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    Sx = int(next(it))
    Sy = int(next(it))

    # Group houses for fast queries
    by_y = defaultdict(list)  # y -> list of x
    by_x = defaultdict(list)  # x -> list of y
    for _ in range(N):
        x = int(next(it))
        y = int(next(it))
        by_y[y].append(x)
        by_x[x].append(y)

    # Sort the lists for binary search
    for y in by_y:
        by_y[y].sort()
    for x in by_x:
        by_x[x].sort()

    visited = set()
    cur_x, cur_y = Sx, Sy

    for _ in range(M):
        D = next(it).decode()
        C = int(next(it))

        if D == 'U':
            new_y = cur_y + C
            # vertical move, x = cur_x
            xs = by_x.get(cur_x)
            if xs:
                lo, hi = cur_y, new_y
                if lo > hi:
                    lo, hi = hi, lo
                # find y in (lo, hi] if we consider inclusive end? 
                # Houses strictly between, and possibly the endpoint if a house is there.
                # The endpoint new_y may be added via final point below.
                left = bisect.bisect_right(xs, lo)
                right = bisect.bisect_left(xs, hi)
                # we need houses with y in (lo, hi]
                # lo < y <= hi
                for y in xs[left:right]:
                    visited.add((cur_x, y))
            cur_y = new_y
            visited.add((cur_x, cur_y))
        elif D == 'D':
            new_y = cur_y - C
            xs = by_x.get(cur_x)
            if xs:
                lo, hi = new_y, cur_y
                if lo > hi:
                    lo, hi = hi, lo
                # y in [lo, hi) for downward move, endpoint cur_y already considered? 
                # Actually we will add cur_y after move, but we also need to consider 
                # houses strictly between, and possibly new_y.
                # Safe: y in (lo, hi)  -> lo < y < hi
                left = bisect.bisect_right(xs, lo)
                right = bisect.bisect_left(xs, hi)
                for y in xs[left:right]:
                    visited.add((cur_x, y))
            cur_y = new_y
            visited.add((cur_x, cur_y))
        elif D == 'R':
            new_x = cur_x + C
            ys = by_y.get(cur_y)
            if ys:
                lo, hi = cur_x, new_x
                if lo > hi:
                    lo, hi = hi, lo
                # x in (lo, hi] for rightward move
                left = bisect.bisect_right(ys, lo)
                right = bisect.bisect_left(ys, hi)
                for x in ys[left:right]:
                    visited.add((x, cur_y))
            cur_x = new_x
            visited.add((cur_x, cur_y))
        elif D == 'L':
            new_x = cur_x - C
            ys = by_y.get(cur_y)
            if ys:
                lo, hi = new_x, cur_x
                if lo > hi:
                    lo, hi = hi, lo
                # x in [lo, hi) for leftward move
                left = bisect.bisect_right(ys, lo)
                right = bisect.bisect_left(ys, hi)
                for x in ys[left:right]:
                    visited.add((x, cur_y))
            cur_x = new_x
            visited.add((cur_x, cur_y))

    print(cur_x, cur_y, len(visited))

if __name__ == "__main__":
    solve()