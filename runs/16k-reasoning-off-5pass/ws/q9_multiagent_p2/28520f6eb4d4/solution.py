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

    buildings = []
    for _ in range(N):
        x = int(next(iterator))
        h = int(next(iterator))
        buildings.append((x, h))

    # Edge case: If N <= 1, we can always see the only building.
    # The problem asks for the max height where it is NOT possible to see ALL buildings.
    # If N=1, we see it at any height, so we can see all. Output -1.
    if N <= 1:
        print("-1")
        return

    # Cross product of vectors (b-a) and (c-a)
    # Returns > 0 if counter-clockwise, < 0 if clockwise, 0 if collinear
    def cross_product(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Monotone Chain to build Upper and Lower Hulls
    # Since input is sorted by X, we can do this in O(N)
    
    # Lower Hull: builds the lower boundary
    lower = []
    for p in buildings:
        while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Upper Hull: builds the upper boundary
    # We iterate in reverse order (right to left) to build the upper chain
    upper = []
    for p in reversed(buildings):
        while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # The upper hull list 'upper' contains points from rightmost to leftmost.
    # We need to check all adjacent pairs in the upper hull to find the maximum y-intercept.
    # The y-intercept of the line passing through (x1, y1) and (x2, y2) (with x1 < x2) is:
    # c = (y1 * x2 - y2 * x1) / (x2 - x1)
    # This represents the height h at x=0 such that the line of sight to (x2, y2) passes through (x1, y1).
    # If h > c, the line of sight to (x2, y2) is blocked by (x1, y1).
    # We want the maximum c such that there exists a pair where blocking occurs.
    # If max_c <= 0, then even at h=0, no building is blocked (since h must be > c to block, and c <= 0).
    
    max_intercept = -1.0
    
    # Iterate through adjacent pairs in the upper hull
    # upper list contains points from rightmost to leftmost.
    # We iterate i from 0 to len(upper)-2.
    # Pair is (upper[i], upper[i+1]).
    # Since we go right to left, upper[i].x >= upper[i+1].x.
    # Let p_left be the one with smaller X, p_right be the one with larger X.
    
    for i in range(len(upper) - 1):
        p1 = upper[i]
        p2 = upper[i+1]
        
        # Ensure p1 is the left point (smaller X)
        if p1[0] > p2[0]:
            p1, p2 = p2, p1
        
        x1, y1 = p1
        x2, y2 = p2
        
        # Calculate intercept: c = (y1*x2 - y2*x1) / (x2 - x1)
        # Since x2 > x1, denominator is positive.
        numerator = y1 * x2 - y2 * x1
        denominator = x2 - x1
        
        if denominator != 0:
            intercept = numerator / denominator
            if intercept > max_intercept:
                max_intercept = intercept

    # If max_intercept <= 0, it means even at h=0, no building is hidden.
    # Output -1 in that case. Otherwise output max_intercept.
    if max_intercept <= 0:
        print("-1")
    else:
        print(f"{max_intercept:.20f}")

if __name__ == '__main__':
    solve()