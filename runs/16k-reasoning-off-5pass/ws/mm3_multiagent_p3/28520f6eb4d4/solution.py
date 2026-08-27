import sys
from collections import deque

def solve():
    input = sys.stdin.readline
    N = int(input())
    points = []
    for _ in range(N):
        x, h = map(int, input().split())
        points.append((x, h))
    
    # deque will store points on the upper convex hull as (X, H)
    hull = deque()
    max_L = -float('inf')
    
    # Helper to compute cross product for determining convexity
    # For upper hull, we want to keep points that make a right turn (clockwise)
    # i.e., the new point should be above the line from second-last to last.
    # Cross product: (last - second_last) x (new - second_last) < 0 for right turn.
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    
    # Helper to compute slope from point p to (X_i, H_i)
    def slope(p, x, h):
        return (h - p[1]) / (x - p[0])
    
    for i in range(N):
        x, h = points[i]
        # Maintain upper convex hull: remove points that are not part of the upper hull
        # For upper convex hull, we want to keep points that make a right turn (cross < 0)
        # If cross >= 0, the middle point is below or on the line, so pop it.
        while len(hull) >= 2 and cross(hull[-2], hull[-1], (x, h)) >= 0:
            hull.pop()
        
        # Now find the point on the hull that minimizes the slope to (x, h)
        # Since the hull is upper convex, the slope function is convex.
        # The slope to the front is slope(hull[0], x, h).
        # As we move along the hull, the slope first decreases then increases.
        # So we can pop the front while the slope to the next point is smaller.
        if hull:
            while len(hull) >= 2:
                p1 = hull[0]
                p2 = hull[1]
                m1 = slope(p1, x, h)
                m2 = slope(p2, x, h)
                if m2 < m1:
                    hull.popleft()
                else:
                    break
            # Now the front point gives the minimum slope
            p_front = hull[0]
            # Compute L_i = (H_j * X_i - H_i * X_j) / (X_i - X_j)
            L_i = (p_front[1] * x - h * p_front[0]) / (x - p_front[0])
            if L_i > max_L:
                max_L = L_i
        
        # Add the new point to the hull
        hull.append((x, h))
    
    if max_L <= 0:
        print(-1)
    else:
        # Print with enough precision
        print(f"{max_L:.18f}")

if __name__ == "__main__":
    solve()