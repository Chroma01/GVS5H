import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
        
    N = int(data[0])
    X = []
    H = []
    
    idx = 1
    for i in range(N):
        X.append(int(data[idx]))
        H.append(int(data[idx+1]))
        idx += 2
        
    # We need to compute M_j = max_{i < j} C_{i,j}
    # where C_{i,j} = (H_i * X_j - H_j * X_i) / (X_j - X_i)
    # This is the y-intercept of the line passing through (X_i, H_i) and (X_j, H_j).
    # We want to find the maximum y-intercept for each j.
    # This is equivalent to finding the tangent from (X_j, H_j) to the upper convex hull of previous points.
    
    # Upper convex hull maintenance
    # We store points on the upper hull in a list 'hull'
    # The hull will be sorted by X coordinate.
    # We want the upper hull, so we keep points that make left turns (counter-clockwise)
    # when traversing from left to right? No, for upper hull, we want the boundary that is "above".
    # Standard convex hull: for upper hull, we want points such that the slope between consecutive points is decreasing.
    
    hull = [] # List of indices of points on the upper hull
    
    def cross_product(o, a, b):
        # Returns the cross product of vectors OA and OB
        # (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)
        return (X[a] - X[o]) * (H[b] - H[o]) - (H[a] - H[o]) * (X[b] - X[o])
        
    def get_y_intercept(i, j):
        # Y-intercept of line through (X[i], H[i]) and (X[j], H[j])
        # y = H[i] - slope * X[i]
        # slope = (H[j] - H[i]) / (X[j] - X[i])
        # y = H[i] - (H[j] - H[i]) * X[i] / (X[j] - X[i])
        #   = (H[i]*(X[j]-X[i]) - (H[j]-H[i])*X[i]) / (X[j]-X[i])
        #   = (H[i]*X[j] - H[i]*X[i] - H[j]*X[i] + H[i]*X[i]) / (X[j]-X[i])
        #   = (H[i]*X[j] - H[j]*X[i]) / (X[j]-X[i])
        return (H[i] * X[j] - H[j] * X[i]) / (X[j] - X[i])
        
    max_M = -float('inf')
    
    for j in range(N):
        # Query: Find i in hull that maximizes get_y_intercept(i, j)
        # The function f(i) = get_y_intercept(i, j) is unimodal on the upper convex hull.
        # We can use ternary search or binary search.
        # Since the hull is convex, the y-intercept as a function of the point on the hull
        # is concave? Let's check.
        # The y-intercept is the value at x=0. The line from (X_j, H_j) to (X_i, H_i).
        # As we move along the upper hull, the slope changes monotonically.
        # The y-intercept is H_i - slope * X_i.
        # It is known that the optimal point can be found by binary search for the tangent.
        
        # We want to find i that maximizes the y-intercept.
        # This is equivalent to finding the point on the hull such that the line from (X_j, H_j) to (X_i, H_i)
        # has the maximum y-intercept.
        # This is the tangent from (X_j, H_j) to the upper hull.
        # Since (X_j, H_j) is to the right of all points in the hull, the tangent will touch the hull at some point.
        # The slope of the line from (X_j, H_j) to (X_i, H_i) is (H_i - H_j) / (X_i - X_j).
        # We want to maximize the y-intercept.
        
        # Let's use binary search on the hull indices.
        # The function is unimodal.
        
        low = 0
        high = len(hull) - 1
        best_i = hull[0]
        best_val = get_y_intercept(hull[0], j)
        
        while low <= high:
            mid = (low + high) // 2
            i_curr = hull[mid]
            val_curr = get_y_intercept(i_curr, j)
            
            if val_curr > best_val:
                best_val = val_curr
                best_i = i_curr
                
            # Check neighbors to determine direction
            # If the function is increasing, go right. If decreasing, go left.
            # We can check the derivative by comparing with mid+1 and mid-1.
            
            # If mid+1 exists and gives a better value, the peak is to the right
            if mid + 1 <= high:
                i_next = hull[mid+1]
                val_next = get_y_intercept(i_next, j)
                if val_next > val_curr:
                    low = mid + 1
                else:
                    high = mid - 1
            else:
                high = mid - 1
                
        if best_val > max_M:
            max_M = best_val
            
        # Update hull: add point j
        # Remove points from the end of the hull that make a non-left turn (for upper hull, we want right turns? No.)
        # For upper hull, we want the boundary that is above.
        # When adding a new point to the right, we remove points from the end that are "below" the new line.
        # Specifically, if the last three points form a right turn (clockwise), the middle one is not on the upper hull.
        # Cross product: (b-a) x (c-b). If <= 0, then b is not on upper hull.
        
        while len(hull) >= 2:
            i1 = hull[-2]
            i2 = hull[-1]
            # Check if adding j makes i2 redundant
            # Cross product of (i2-i1) and (j-i2)
            # If cross product <= 0, then i2 is not on the upper hull
            cp = (X[i2] - X[i1]) * (H[j] - H[i2]) - (H[i2] - H[i1]) * (X[j] - X[i2])
            if cp <= 0:
                hull.pop()
            else:
                break
        hull.append(j)
        
    if max_M < 0:
        print("-1")
    else:
        print(f"{max_M:.20f}")

solve()