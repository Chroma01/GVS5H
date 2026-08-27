import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    buildings = []
    for _ in range(N):
        x = int(next(iterator))
        h = int(next(iterator))
        buildings.append((x, h))

    # Upper convex hull maintenance
    # hull is a list of points (x, h) forming the upper convex hull
    # We maintain it such that it is convex (upper chain).
    # When adding a new point, we remove points from the end that make the hull non-convex.
    
    hull = []
    
    # Function to check if the last three points in hull make a non-left turn (or right turn/collinear)
    # For upper hull, we want counter-clockwise turns.
    # Cross product of (b-a) and (c-b) should be > 0 for left turn.
    # If <= 0, then b is not part of the upper hull.
    def cross_product(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    ans = 0.0
    
    for i in range(N):
        x_j, h_j = buildings[i]
        
        # 1. Find the tangent point on the current hull that maximizes the y-intercept
        # The y-intercept of the line connecting (x_k, h_k) and (x_j, h_j) is:
        # I = (h_k * x_j - h_j * x_k) / (x_j - x_k)
        # We want to maximize I over k in hull.
        # This is equivalent to finding the upper tangent from (x_j, h_j) to the hull.
        
        # Binary search for the tangent point
        # The slope of the line from (x_j, h_j) to (x_k, h_k) is m_k = (h_j - h_k) / (x_j - x_k)
        # The intercept is h_k - m_k * x_k.
        # The function of intercept with respect to the index on the hull is unimodal.
        
        low = 0
        high = len(hull) - 1
        best_idx = -1
        best_intercept = -float('inf')
        
        # If hull is empty, intercept is -inf (so min_h is 0)
        if hull:
            # Ternary search or binary search for the peak
            # Since it's a convex function (unimodal), we can use binary search on the derivative (slope)
            # Or simply ternary search on the discrete indices.
            
            l, r = 0, len(hull) - 1
            while r - l > 2:
                m1 = l + (r - l) // 3
                m2 = r - (r - l) // 3
                
                # Calculate intercepts
                x1, h1 = hull[m1]
                x2, h2 = hull[m2]
                
                # Intercept for m1
                # I1 = (h1 * x_j - h_j * x1) / (x_j - x1)
                # To avoid division, we can compare I1 and I2 by cross-multiplying
                # I1 > I2 <=> (h1*x_j - h_j*x1)/(x_j-x1) > (h2*x_j - h_j*x2)/(x_j-x2)
                # Since x_j > x1 and x_j > x2, denominators are positive.
                
                val1 = (h1 * x_j - h_j * x1) * (x_j - x2)
                val2 = (h2 * x_j - h_j * x2) * (x_j - x1)
                
                if val1 < val2:
                    # Peak is in [m2, r]
                    l = m1
                else:
                    # Peak is in [l, m1]
                    r = m2
            
            # Check remaining points
            for k in range(l, r + 1):
                x_k, h_k = hull[k]
                intercept = (h_k * x_j - h_j * x_k) / (x_j - x_k)
                if intercept > best_intercept:
                    best_intercept = intercept
                    best_idx = k
        
        if best_idx != -1:
            min_h_j = max(0.0, best_intercept)
        else:
            min_h_j = 0.0
            
        if min_h_j > ans:
            ans = min_h_j
            
        # 2. Add current building to the hull
        # Maintain upper convex hull
        current_point = (x_j, h_j)
        while len(hull) >= 2:
            # Check if adding current_point makes the last segment non-convex
            # We want to keep left turns. If cross_product(hull[-2], hull[-1], current_point) <= 0,
            # then hull[-1] is not part of the upper hull.
            cp = cross_product(hull[-2], hull[-1], current_point)
            if cp <= 0:
                hull.pop()
            else:
                break
        hull.append(current_point)

    if ans == 0:
        # Check if it's possible to see all buildings at height 0.
        # If ans is 0, it means for all j, min_h(j) == 0.
        # This implies all buildings are visible at height 0.
        print("-1")
    else:
        print(f"{ans:.20f}")

solve()