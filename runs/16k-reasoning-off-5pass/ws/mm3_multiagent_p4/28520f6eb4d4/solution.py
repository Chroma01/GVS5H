import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    points = []
    for _ in range(N):
        x = int(next(it))
        h = int(next(it))
        points.append((x, h))
    
    # If only one building, it is always visible from any h>=0.
    if N == 1:
        print(-1)
        return

    # Build upper convex hull in (U, S) plane with U = -1/x, S = h/x
    # U increases as x increases.
    hull = []
    for x, h in points:
        u = -1.0 / x
        s = h / x
        while len(hull) >= 2:
            u1, s1 = hull[-2]
            u2, s2 = hull[-1]
            # For upper hull, slopes between consecutive points must be strictly decreasing.
            # If slope(penultimate->last) <= slope(last->new), pop last.
            # Use cross multiplication to avoid floating point errors:
            # (s2 - s1) * (u - u2) <= (s - s2) * (u2 - u1)
            if (s2 - s1) * (u - u2) <= (s - s2) * (u2 - u1):
                hull.pop()
            else:
                break
        hull.append((u, s))
    
    # Compute maximum slope between consecutive points on the upper hull.
    max_slope = -float('inf')
    for i in range(1, len(hull)):
        u1, s1 = hull[i-1]
        u2, s2 = hull[i]
        # u2 > u1 since we process in increasing u, so denominator is positive
        slope = (s2 - s1) / (u2 - u1)  # This equals T(i,j) for some pair
        if slope > max_slope:
            max_slope = slope
    
    # The answer is max_slope if it is non-negative; otherwise, all buildings are visible from any h>=0.
    if max_slope < 0:
        print(-1)
    else:
        # If max_slope is very small negative due to floating errors, treat as 0.
        if max_slope < 0:
            max_slope = 0.0
        print("{:.18f}".format(max_slope))

if __name__ == "__main__":
    solve()