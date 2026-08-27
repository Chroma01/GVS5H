import sys

def solve():
    input = sys.stdin.readline
    N = int(input().strip())
    X = []
    H = []
    for _ in range(N):
        x, h = map(int, input().split())
        X.append(x)
        H.append(h)

    # Maintain upper convex hull of previous points (X_j, H_j)
    hull = []  # list of (X, H) in order of increasing X, upper convex hull

    def add_point(x, h):
        # Add point to upper convex hull, maintaining decreasing slopes
        hull.append((x, h))
        while len(hull) >= 3:
            x1, h1 = hull[-3]
            x2, h2 = hull[-2]
            x3, h3 = hull[-1]
            # Check if middle point is below line connecting outer points
            # (h2 - h1) * (x3 - x2) <= (h3 - h2) * (x2 - x1) => pop h2
            if (h2 - h1) * (x3 - x2) <= (h3 - h2) * (x2 - x1):
                hull.pop(-2)
            else:
                break

    def query_hull(xq, hq):
        # Find maximum y-intercept of line from (xq, hq) to any point in hull
        # y-intercept = (H_j * xq - hq * X_j) / (xq - X_j)
        if not hull:
            return -float('inf')
        if len(hull) == 1:
            xp, hp = hull[0]
            return (hp * xq - hq * xp) / (xq - xp)
        
        # Ternary search on the hull indices (function is unimodal on convex hull)
        l = 0
        r = len(hull) - 1
        
        while r - l >= 3:
            m1 = l + (r - l) // 3
            m2 = r - (r - l) // 3
            
            # Compare f(m1) and f(m2) using cross multiplication
            x1, h1 = hull[m1]
            x2, h2 = hull[m2]
            
            # f(m1) < f(m2) ?
            # (h1 * xq - hq * x1) / (xq - x1)  <  (h2 * xq - hq * x2) / (xq - x2)
            # Cross multiply (denominators positive since xq > all X_j):
            # (h1 * xq - hq * x1) * (xq - x2)  <  (h2 * xq - hq * x2) * (xq - x1)
            val1 = (h1 * xq - hq * x1) * (xq - x2)
            val2 = (h2 * xq - hq * x2) * (xq - x1)
            
            if val1 < val2:
                l = m1
            else:
                r = m2
        
        # Check remaining candidates
        best = -float('inf')
        for idx in range(l, r + 1):
            xp, hp = hull[idx]
            val = (hp * xq - hq * xp) / (xq - xp)
            if val > best:
                best = val
        
        return best

    ans = -float('inf')
    
    for i in range(N):
        xq, hq = X[i], H[i]
        if i == 0:
            add_point(xq, hq)
            continue
        
        # Query the hull for maximum y-intercept
        val = query_hull(xq, hq)
        if val > ans:
            ans = val
        
        add_point(xq, hq)

    # If ans < 0, all buildings are visible at height 0, output -1
    # If ans >= 0, output the value
    if ans < -1e-12:
        print(-1)
    else:
        print(f"{ans:.18f}")

if __name__ == "__main__":
    solve()