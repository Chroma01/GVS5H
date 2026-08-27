import sys

# Increase recursion depth just in case, though not used here
sys.setrecursionlimit(2000)

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

    # If N=1, no building can block another. All visible from any height >= 0.
    if N == 1:
        print("-1")
        return

    # We need to find max_{i} ( max_{j < i} intercept(j, i) )
    # intercept(j, i) = (H[j]*X[i] - H[i]*X[j]) / (X[i] - X[j])
    # This is equivalent to finding the y-intercept of the line through (X[j], H[j]) and (X[i], H[i]).
    
    # We maintain the upper convex hull of points (X[0]..X[k]) to efficiently query the max intercept.
    # The hull will be a list of indices.
    hull = []
    
    # Helper to check if adding point 'new_idx' maintains upper convex hull property
    # We need the slope between (hull[-2], hull[-1]) to be > slope between (hull[-1], new_idx)
    # Slope(a, b) = (H[b] - H[a]) / (X[b] - X[a])
    # Condition: (H[last] - H[prev]) / (X[last] - X[prev]) > (H[new] - H[last]) / (X[new] - X[last])
    # Cross multiply to avoid division: (H[last] - H[prev]) * (X[new] - X[last]) > (H[new] - H[last]) * (X[last] - X[prev])
    
    def is_convex(prev, curr, nxt):
        # prev, curr, nxt are indices
        # Check if slope(prev, curr) > slope(curr, nxt)
        # (H[curr] - H[prev]) / (X[curr] - X[prev]) > (H[nxt] - H[curr]) / (X[nxt] - X[curr])
        # Since X is strictly increasing, denominators are positive.
        return (H[curr] - H[prev]) * (X[nxt] - X[curr]) > (H[nxt] - H[curr]) * (X[curr] - X[prev])

    def add_to_hull(idx):
        while len(hull) >= 2 and not is_convex(hull[-2], hull[-1], idx):
            hull.pop()
        hull.append(idx)

    def get_max_intercept(hull_indices, target_idx):
        # Find j in hull that maximizes intercept(j, target_idx)
        # intercept(j, i) = (H[j]*X[i] - H[i]*X[j]) / (X[i] - X[j])
        # Let f(j) = (H[j]*X[i] - H[i]*X[j]) / (X[i] - X[j])
        # We can use ternary search because the function is unimodal on the upper convex hull.
        
        low = 0
        high = len(hull_indices) - 1
        
        # Ternary search
        while high - low > 2:
            m1 = low + (high - low) // 3
            m2 = high - (high - low) // 3
            
            # Calculate intercepts
            # intercept = (H[j]*X[i] - H[i]*X[j]) / (X[i] - X[j])
            val1 = (H[hull_indices[m1]] * X[target_idx] - H[target_idx] * X[hull_indices[m1]]) / (X[target_idx] - X[hull_indices[m1]])
            val2 = (H[hull_indices[m2]] * X[target_idx] - H[target_idx] * X[hull_indices[m2]]) / (X[target_idx] - X[hull_indices[m2]])
            
            if val1 < val2:
                low = m1
            else:
                high = m2
        
        best_val = -1.0
        for k in range(low, high + 1):
            j = hull_indices[k]
            val = (H[j] * X[target_idx] - H[target_idx] * X[j]) / (X[target_idx] - X[j])
            if val > best_val:
                best_val = val
        return best_val

    max_intercept = -1.0
    
    # Process first building
    add_to_hull(0)
    
    # Process remaining buildings
    for i in range(1, N):
        # Find max intercept from any building in the current hull to building i
        current_max = get_max_intercept(hull, i)
        if current_max > max_intercept:
            max_intercept = current_max
        
        # Add building i to the hull
        add_to_hull(i)

    # If max_intercept < 0, it means even at height 0, all buildings are visible.
    # The problem asks for the maximum height h >= 0 such that it is NOT possible to see all buildings.
    # If max_intercept < 0, then for any h >= 0, h > max_intercept, so all buildings are visible.
    # Thus, no such h exists (or rather, the condition "not all visible" is never met for h >= 0).
    # The problem statement says: "if it is possible to see all buildings at height 0 at coordinate 0, report -1 instead."
    # If max_intercept < 0, then at height 0, all buildings are visible. So output -1.
    # If max_intercept >= 0, then at height = max_intercept, at least one building is not visible (since h <= intercept).
    # And for any h > max_intercept, all buildings are visible. So the answer is max_intercept.
    
    if max_intercept < 0:
        print("-1")
    else:
        print(f"{max_intercept:.20f}")

if __name__ == '__main__':
    solve()