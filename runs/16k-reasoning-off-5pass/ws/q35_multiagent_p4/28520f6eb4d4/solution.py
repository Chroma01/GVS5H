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
    # hull will store indices of buildings that form the upper convex hull
    # The points are added in increasing order of X.
    # We maintain the upper hull such that the slopes of consecutive segments are decreasing.
    hull = []

    def cross_product(o, a, b):
        """
        Returns the cross product of vectors OA and OB.
        o, a, b are tuples (x, y).
        Positive if OAB makes a counter-clockwise turn (left turn).
        Negative if clockwise turn (right turn).
        Zero if collinear.
        For upper hull with increasing X, we want right turns or straight.
        So we remove points that make a left turn.
        """
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    max_R = -float('inf')

    for i in range(N):
        x_i, h_i = buildings[i]
        
        # Query the hull for the maximum y-intercept line from (x_i, h_i) to any point on the hull
        if hull:
            # We want to find j in hull that maximizes:
            # R_j = (h_j * x_i - h_i * x_j) / (x_i - x_j)
            # This is equivalent to finding the tangent from (x_i, h_i) to the upper convex hull.
            # The function of intercept vs index on the hull is concave (unimodal).
            # We can use binary search (ternary search or derivative check).
            
            # Let's use a pointer approach or binary search.
            # Since the hull is concave, the slope of the line from (x_i, h_i) to hull[k]
            # is decreasing as k increases? Not necessarily monotonic in a simple way for binary search
            # unless we check the derivative condition.
            
            # Condition for optimal k:
            # The line from P_i to P_k should be above all other points on the hull.
            # This means the slope from P_i to P_k should be greater than the slope from P_i to P_{k+1}
            # and less than the slope from P_i to P_{k-1}?
            # Actually, for the upper hull, the tangent point T satisfies:
            # slope(P_i, T) >= slope(P_i, T_next) and slope(P_i, T) >= slope(P_i, T_prev) ?
            # Let's check the derivative of the intercept function.
            # It's easier to just use ternary search or binary search on the condition.
            
            # Let f(k) be the intercept of line from (x_i, h_i) to hull[k].
            # We want max f(k).
            # f(k) is concave. We can find the peak.
            
            low = 0
            high = len(hull) - 1
            
            while low < high:
                mid = (low + high) // 2
                mid_next = mid + 1
                
                # Calculate intercepts
                x_m, h_m = buildings[hull[mid]]
                x_n, h_n = buildings[hull[mid_next]]
                
                # Intercept for mid
                # R = (h_m * x_i - h_i * x_m) / (x_i - x_m)
                # To avoid division, compare R_mid and R_mid_next
                # R_mid >= R_mid_next <=> (h_m * x_i - h_i * x_m) / (x_i - x_m) >= (h_n * x_i - h_i * x_n) / (x_i - x_n)
                # Since x_i > x_m and x_i > x_n, denominators are positive.
                # (h_m * x_i - h_i * x_m) * (x_i - x_n) >= (h_n * x_i - h_i * x_n) * (x_i - x_m)
                
                val_m = (h_m * x_i - h_i * x_m) * (x_i - x_n)
                val_n = (h_n * x_i - h_i * x_n) * (x_i - x_m)
                
                if val_m >= val_n:
                    # Peak is at mid or to the left
                    high = mid
                else:
                    # Peak is to the right
                    low = mid_next
            
            # low is the index in hull that gives the maximum intercept
            best_idx = hull[low]
            x_j, h_j = buildings[best_idx]
            
            # Calculate R_i
            # R_i = (h_j * x_i - h_i * x_j) / (x_i - x_j)
            R_i = (h_j * x_i - h_i * x_j) / (x_i - x_j)
            if R_i > max_R:
                max_R = R_i

        # Update the upper convex hull with the new point (x_i, h_i)
        while len(hull) >= 2:
            # Check the last two points in hull and the new point
            # Let a = hull[-2], b = hull[-1], c = new point
            # We want to keep the upper hull, so we remove b if it makes a right turn?
            # For upper hull with increasing X, we want the sequence to turn right (clockwise) or be straight.
            # If it turns left (counter-clockwise), then b is below the line ac, so remove b.
            # Cross product of (b-a) and (c-b) should be <= 0 for upper hull?
            # Let's use the cross product function defined above.
            # o = hull[-2], a = hull[-1], b = new point
            # If cross_product(o, a, b) > 0, it's a left turn, so remove a.
            
            a_idx = hull[-2]
            b_idx = hull[-1]
            
            x_a, y_a = buildings[a_idx]
            x_b, y_b = buildings[b_idx]
            
            # Cross product of (b-a) and (c-b) where c is new point
            # Vector ab = (x_b - x_a, y_b - y_a)
            # Vector bc = (x_i - x_b, h_i - y_b)
            # Cross = (x_b - x_a)*(h_i - y_b) - (y_b - y_a)*(x_i - x_b)
            # If Cross > 0, it's a left turn, so remove b.
            
            cp = (x_b - x_a) * (h_i - y_b) - (y_b - y_a) * (x_i - x_b)
            
            if cp > 0:
                hull.pop()
            else:
                break
        hull.append(i)

    if max_R <= 0:
        print("-1")
    else:
        print(f"{max_R:.20f}")

solve()