import sys

# Increase recursion depth just in case, though not used here
sys.setrecursionlimit(200005)

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

    X = []
    H = []
    for _ in range(N):
        X.append(int(next(iterator)))
        H.append(int(next(iterator)))

    # If there's only 1 building, it's always visible from height 0 (no obstacles).
    # The problem asks for max height where NOT all are visible.
    # If all are visible at height 0, output -1.
    if N == 1:
        print("-1")
        return

    # Stack to store indices of the upper convex hull of buildings processed so far.
    # The hull is maintained such that the slopes between consecutive points are decreasing.
    hull_indices = [0] 
    
    # We need to find the maximum required height h such that some building i is NOT visible.
    # This is equivalent to finding max_i (min_h_to_see_i).
    # min_h_to_see_i = max_{j < i} (intercept of line through j and i)
    # intercept = (X[i]*H[j] - X[j]*H[i]) / (X[i] - X[j])
    
    max_required_h = 0.0
    
    # We will iterate i from 1 to N-1 (0-indexed)
    # For each i, we query the hull (indices 0 to i-1) to find the j that maximizes the intercept.
    # Then we add i to the hull.
    
    for i in range(1, N):
        # Current building i
        xi, hi = X[i], H[i]
        
        # We need to find j in hull_indices that maximizes:
        # f(j) = (xi * H[j] - X[j] * hi) / (xi - X[j])
        # Note: xi > X[j] for all j in hull_indices because X is strictly increasing.
        
        # The function f(j) is convex/concave on the convex hull?
        # Geometrically, we are looking for the line from (xi, hi) to the hull that has the maximum y-intercept.
        # This corresponds to the tangent from (xi, hi) to the upper convex hull.
        # Since the hull is convex and (xi, hi) is to the right, the function is unimodal.
        # We can use ternary search.
        
        low = 0
        high = len(hull_indices) - 1
        
        # Ternary search for the index in hull_indices
        while high - low > 2:
            m1 = low + (high - low) // 3
            m2 = high - (high - low) // 3
            
            j1 = hull_indices[m1]
            j2 = hull_indices[m2]
            
            # Calculate intercepts
            # Avoid division by zero (not possible here as X is strictly increasing)
            val1 = (xi * H[j1] - X[j1] * hi) / (xi - X[j1])
            val2 = (xi * H[j2] - X[j2] * hi) / (xi - X[j2])
            
            if val1 < val2:
                low = m1
            else:
                high = m2
        
        # Check the remaining candidates
        best_j = hull_indices[low]
        best_val = (xi * H[best_j] - X[best_j] * hi) / (xi - X[best_j])
        
        for k in range(low + 1, high + 1):
            j = hull_indices[k]
            val = (xi * H[j] - X[j] * hi) / (xi - X[j])
            if val > best_val:
                best_val = val
                best_j = j
        
        if best_val > max_required_h:
            max_required_h = best_val
        
        # Now add building i to the hull
        # We maintain the upper convex hull.
        # The condition for adding a point is that it doesn't make the previous point redundant.
        # Specifically, the slope from hull[-2] to hull[-1] must be >= slope from hull[-1] to i.
        # If slope(hull[-2], hull[-1]) < slope(hull[-1], i), then hull[-1] is below the line segment 
        # connecting hull[-2] and i, so it's not on the upper hull.
        
        while len(hull_indices) >= 2:
            j2 = hull_indices[-1]
            j1 = hull_indices[-2]
            
            # Slope between j1 and j2
            # slope = (H[j2] - H[j1]) / (X[j2] - X[j1])
            # Slope between j2 and i
            # slope_new = (H[i] - H[j2]) / (X[i] - X[j2])
            
            # We want to check if slope(j1, j2) < slope(j2, i)
            # To avoid floating point issues, use cross multiplication:
            # (H[j2] - H[j1]) * (X[i] - X[j2]) < (H[i] - H[j2]) * (X[j2] - X[j1])
            
            # Note: X is strictly increasing, so denominators are positive.
            # However, we are checking the upper hull.
            # If the new point i is "above" the line extending from j1 to j2, then j2 is redundant?
            # Actually, for upper hull, we want the sequence of slopes to be decreasing.
            # If slope(j1, j2) < slope(j2, i), then the sequence is increasing, which violates the upper hull property.
            # So we pop j2.
            
            num1 = H[j2] - H[j1]
            den1 = X[j2] - X[j1]
            num2 = H[i] - H[j2]
            den2 = X[i] - X[j2]
            
            # Check if slope1 < slope2
            if num1 * den2 < num2 * den1:
                hull_indices.pop()
            else:
                break
        
        hull_indices.append(i)

    # If max_required_h <= 0, it means even at height 0, all buildings are visible.
    # The problem asks for the max height where it is NOT possible to see all.
    # If at height 0 it IS possible, then the set of heights where it is NOT possible is empty (or negative).
    # The problem statement says: "if it is possible to see all buildings from coordinate 0 and height 0, print -1".
    # So if max_required_h <= 0, print -1.
    # Otherwise, print max_required_h.
    
    if max_required_h <= 1e-9: # Using epsilon for float comparison
        print("-1")
    else:
        print(f"{max_required_h:.20f}")

if __name__ == '__main__':
    solve()