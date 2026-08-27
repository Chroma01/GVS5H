import sys
from collections import deque

def solve():
    input = sys.stdin.readline
    N = int(input())
    X = []
    H = []
    for _ in range(N):
        x, h = map(int, input().split())
        X.append(x)
        H.append(h)
    
    # Upper convex hull of points (X_j, H_j) processed so far.
    hull = deque()
    # Pointer to the best point on the hull for the current query.
    ptr = 0  # index in hull
    
    global_max = -float('inf')
    
    for i in range(N):
        xi, hi = X[i], H[i]
        if i == 0:
            # First building is always visible.
            hull.append((xi, hi))
            continue
        
        # Adjust ptr to valid range
        if ptr >= len(hull):
            ptr = len(hull) - 1
        if ptr < 0:
            ptr = 0
            
        # Move ptr right while the next point gives a smaller slope.
        while ptr + 1 < len(hull):
            xj, hj = hull[ptr]
            xk, hk = hull[ptr+1]
            # slope to j: (hi - hj)/(xi - xj)
            # slope to k: (hi - hk)/(xi - xk)
            # Move to k if slope to k < slope to j
            left = (hi - hk) * (xi - xj)
            right = (hi - hj) * (xi - xk)
            if left < right:
                ptr += 1
            else:
                break
        
        # Compute T = (hj*xi - hi*xj)/(xi - xj)
        xj, hj = hull[ptr]
        T = (hj * xi - hi * xj) / (xi - xj)
        if T > global_max:
            global_max = T
        
        # Add current point to hull, maintaining upper convex hull.
        while len(hull) >= 2:
            x1, h1 = hull[-2]
            x2, h2 = hull[-1]
            # If (xi, hi) makes (x2, h2) not on upper hull, pop it
            if (hi - h2) * (x2 - x1) >= (h2 - h1) * (xi - x2):
                hull.pop()
                if ptr >= len(hull):
                    ptr = len(hull) - 1
            else:
                break
        hull.append((xi, hi))
        if ptr >= len(hull):
            ptr = len(hull) - 1
    
    if global_max <= 0:
        print(-1)
    else:
        print("{:.18f}".format(global_max))

if __name__ == "__main__":
    solve()