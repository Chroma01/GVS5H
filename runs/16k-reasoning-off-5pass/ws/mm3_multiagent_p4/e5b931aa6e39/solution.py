import sys
import math

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    
    # Upper bound for y: since x > y >= 1, we have x^3 = N + y^3 > y^3.
    # Also x^3 = N + y^3 <= N + x^3 (trivial). The largest y is around N^(1/3).
    # Use a safe upper bound.
    max_y = int(round(N ** (1/3))) + 2
    if max_y < 1:
        max_y = 1
    
    for y in range(1, max_y + 1):
        target = y**3 + N
        # Integer cube root via binary search.
        lo, hi = 0, 1
        while hi**3 < target:
            hi *= 2
        # Now hi**3 >= target
        while lo < hi:
            mid = (lo + hi) // 2
            if mid**3 < target:
                lo = mid + 1
            else:
                hi = mid
        x = lo
        if x**3 == target and x > y:
            print(f"{x} {y}")
            return
    
    # If not found within that range, still check a bit more: y up to N^(1/3)+5
    # Actually the above max_y already covers it, but to be safe:
    extra = int(N ** (1/3)) + 5
    for y in range(max_y + 1, extra + 1):
        target = y**3 + N
        lo, hi = 0, 1
        while hi**3 < target:
            hi *= 2
        while lo < hi:
            mid = (lo + hi) // 2
            if mid**3 < target:
                lo = mid + 1
            else:
                hi = mid
        x = lo
        if x**3 == target and x > y:
            print(f"{x} {y}")
            return
    
    print(-1)

if __name__ == "__main__":
    solve()