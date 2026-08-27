import sys

# Increase recursion depth just in case, though not used here
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    points = []
    for _ in range(N):
        x = int(next(iterator))
        h = int(next(iterator))
        points.append((x, h))

    # If there are 0 or 1 buildings, it's impossible to block visibility 
    # (or trivially all visible), so output -1.
    if N <= 1:
        print("-1")
        return

    # The problem asks for the maximum height h at x=0 such that NOT all buildings are visible.
    # A building i is blocked by building j (j < i) if the line of sight from (0, h) to (Xi, Hi)
    # passes below (Xj, Hj). This happens if h <= intercept(j, i), where intercept(j, i) is the
    # y-intercept of the line passing through (Xj, Hj) and (Xi, Hi).
    # To have at least one building blocked, we need h <= max(intercept(j, i)) for all pairs j < i.
    # The maximum such h is exactly max(intercept(j, i)).
    # Geometrically, the line with the maximum y-intercept passing through any two points in a set
    # is always an edge of the Convex Hull of that set.
    # Thus, we compute the Convex Hull and check the intercepts of its edges.

    # Sort points by x-coordinate. The problem guarantees X_i are strictly increasing,
    # but sorting ensures robustness.
    points.sort()

    # Monotone Chain algorithm to compute Convex Hull
    # Build lower hull
    lower = []
    for p in points:
        while len(lower) >= 2:
            a = lower[-2]
            b = lower[-1]
            c = p
            # Cross product (b-a) x (c-a)
            # (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)
            cross = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
            # If cross <= 0, it's a right turn or collinear. We remove 'b' to maintain convexity.
            # We want strictly convex hull for edges, but collinear points on the hull edge
            # yield the same intercept as the endpoints, so removing them is safe.
            if cross <= 0:
                lower.pop()
            else:
                break
        lower.append(p)

    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2:
            a = upper[-2]
            b = upper[-1]
            c = p
            cross = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
            if cross <= 0:
                upper.pop()
            else:
                break
        upper.append(p)

    # Concatenate to get full hull. 
    # lower contains [p0, ..., pk] where pk is the rightmost point.
    # upper contains [pk, ..., p0].
    # We remove the last point of each list to avoid duplication of start/end points.
    hull = lower[:-1] + upper[:-1]

    if not hull:
        print("-1")
        return

    max_intercept = -1.0

    # Iterate over all edges of the convex hull
    m = len(hull)
    for i in range(m):
        p1 = hull[i]
        p2 = hull[(i + 1) % m]
        
        x1, y1 = p1
        x2, y2 = p2
        
        # Calculate intercept: y = m*x + c => c = y - m*x
        # m = (y2 - y1) / (x2 - x1)
        # c = y1 - (y2 - y1) * x1 / (x2 - x1)
        #   = (y1*(x2-x1) - (y2-y1)*x1) / (x2-x1)
        #   = (y1*x2 - y1*x1 - y2*x1 + y1*x1) / (x2-x1)
        #   = (y1*x2 - y2*x1) / (x2 - x1)
        
        # Since X_i are strictly increasing, x1 != x2 for any distinct points in hull
        intercept = (y1 * x2 - y2 * x1) / (x2 - x1)
        
        if intercept > max_intercept:
            max_intercept = intercept

    # If max_intercept < 0, it means even at height 0, all buildings are visible.
    # The problem asks for max height h such that NOT all buildings are visible.
    # If at h=0 all are visible, then no such non-negative h exists.
    # Thus we output -1.
    # If max_intercept >= 0, then for h = max_intercept, there is a blocking line.
    # So the answer is max_intercept.
    
    if max_intercept < 0:
        print("-1")
    else:
        print(f"{max_intercept:.20f}")

if __name__ == '__main__':
    solve()