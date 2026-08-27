import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(200005)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
    except StopIteration:
        return

    buildings = []
    for _ in range(n):
        x = int(next(iterator))
        h = int(next(iterator))
        buildings.append((x, h))

    # If there is only 1 building, it is always visible from any height >= 0.
    # Thus, the set of heights where we cannot see all buildings is empty.
    # The problem asks for the maximum height where it is NOT possible to see all.
    # If it is always possible to see all (for all h >= 0), we output -1.
    if n == 1:
        print("-1")
        return

    # We need to find the maximum height h at x=0 such that there exists at least one building i
    # that is completely hidden by some building j (j < i).
    # A building i is hidden by j if the line of sight from (0, h) to the top of i (X_i, H_i)
    # passes through or below the top of j (X_j, H_j).
    # The critical case is when the line passes exactly through (X_j, H_j).
    # The height h for a pair (j, i) is the y-intercept of the line passing through (X_j, H_j) and (X_i, H_i).
    # h = (H_j * X_i - H_i * X_j) / (X_i - X_j)
    # We want to maximize this h over all pairs j < i.
    # The maximum y-intercept of a line passing through two points in a set is achieved by a pair of points
    # on the upper convex hull of the set. Furthermore, for the upper convex hull, the maximum intercept
    # is achieved by a pair of adjacent vertices on the hull.

    # Step 1: Compute the upper convex hull using a monotonic stack.
    # Since X coordinates are sorted, we process buildings in order.
    # We maintain a stack of points that form the upper hull.
    # For a new point P, if the slope from the second-to-last point to the last point is >= 
    # the slope from the last point to P, then the last point is not on the upper hull (it's below the line).
    # We pop it.
    
    stack = []
    for i in range(n):
        x, h = buildings[i]
        while len(stack) >= 2:
            x2, h2 = stack[-1]
            x1, h1 = stack[-2]
            
            # Check if (x2, h2) is below or on the line segment (x1, h1) -> (x, h)
            # Slope 1: (h2 - h1) / (x2 - x1)
            # Slope 2: (h - h2) / (x - x2)
            # Condition to pop: Slope 1 >= Slope 2
            # (h2 - h1) * (x - x2) >= (h - h2) * (x2 - x1)
            if (h2 - h1) * (x - x2) >= (h - h2) * (x2 - x1):
                stack.pop()
            else:
                break
        stack.append((x, h))
    
    # Step 2: Iterate through adjacent pairs in the hull stack to find the maximum intercept.
    max_h_val = -1.0
    
    for i in range(len(stack) - 1):
        x1, h1 = stack[i]
        x2, h2 = stack[i+1]
        
        # Calculate y-intercept of the line passing through (x1, h1) and (x2, h2)
        # Equation: y - h1 = m * (x - x1) => y = m*x - m*x1 + h1
        # m = (h2 - h1) / (x2 - x1)
        # intercept = h1 - m * x1 = h1 - (h2 - h1)/(x2 - x1) * x1
        #           = (h1*(x2-x1) - (h2-h1)*x1) / (x2-x1)
        #           = (h1*x2 - h1*x1 - h2*x1 + h1*x1) / (x2-x1)
        #           = (h1*x2 - h2*x1) / (x2-x1)
        
        num = h1 * x2 - h2 * x1
        den = x2 - x1
        
        # Since x2 > x1 (sorted input), den > 0.
        h_val = num / den
        
        if h_val > max_h_val:
            max_h_val = h_val
            
    # If the maximum height found is <= 0, it means even at height 0, no building is blocked 
    # (or the blocking height is negative, which is impossible for h >= 0).
    # In this case, all buildings are visible for all h >= 0.
    if max_h_val <= 0:
        print("-1")
    else:
        # Output with high precision
        print(f"{max_h_val:.20f}")

if __name__ == '__main__':
    solve()