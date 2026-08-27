import sys
from collections import deque

def solve():
    input = sys.stdin.readline
    N = int(input().strip())
    points = []
    for _ in range(N):
        x_str, h_str = input().split()
        points.append((int(x_str), int(h_str)))
    
    # We want max over i<j of (H_i * X_j - H_j * X_i) / (X_j - X_i)
    # We sweep j from left to right, maintaining a deque of candidate i's (the upper convex hull).
    # For each j, we query the deque for the best i.
    # The deque stores points (X, H). We maintain the upper convex hull such that the slopes between consecutive points are strictly decreasing.
    # To add a new point p = (x, h), we pop from the back while the last three points make a left turn (cross product >= 0).
    # To query for point p, we pop from the front while the next point gives a larger y-intercept than the first point.
    # We compare y-intercepts without division by cross-multiplying.
    
    dq = deque()
    dq.append(points[0])
    
    # Track the maximum as a fraction (num, den)
    max_num = -1  # numerator of max fraction (denominator always positive)
    max_den = 1
    
    # Helper to compare two fractions a/b and c/d: returns True if a/b > c/d
    def frac_gt(a, b, c, d):
        return a * d > c * b
    
    # Helper to check if point a, b, c make a left turn (cross product >= 0)
    # cross = (x_b - x_a)*(h_c - h_b) - (h_b - h_a)*(x_c - x_b)
    def is_left_turn(a, b, c):
        return (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0]) >= 0
    
    for i in range(1, N):
        cur_x, cur_h = points[i]
        
        # Query: pop from front while the next point gives a better y-intercept
        while len(dq) >= 2:
            # Compare f(dq[0], cur) and f(dq[1], cur)
            x1, h1 = dq[0]
            x2, h2 = dq[1]
            # f(j, i) = (h_j * x_i - h_i * x_j) / (x_i - x_j)
            # Compare f1 and f2: (h1*cur_x - cur_h*x1)/(cur_x - x1) vs (h2*cur_x - cur_h*x2)/(cur_x - x2)
            num1 = h1 * cur_x - cur_h * x1
            den1 = cur_x - x1
            num2 = h2 * cur_x - cur_h * x2
            den2 = cur_x - x2
            # If f2 > f1, pop dq[0]
            if frac_gt(num2, den2, num1, den1):
                dq.popleft()
            else:
                break
        
        # Now dq[0] is the best candidate for left point
        if dq:
            x1, h1 = dq[0]
            num = h1 * cur_x - cur_h * x1
            den = cur_x - x1
            # Update max if num/den > max_num/max_den
            if frac_gt(num, den, max_num, max_den):
                max_num = num
                max_den = den
        
        # Add current point to the hull: pop from back while left turn
        while len(dq) >= 2 and is_left_turn(dq[-2], dq[-1], points[i]):
            dq.pop()
        dq.append(points[i])
    
    # Determine answer
    if max_num < 0:
        print(-1)
    else:
        # max_num >= 0
        val = max_num / max_den
        # Handle the case where val is exactly 0 or very close
        if val == 0:
            print(0.0)
        else:
            print(f"{val:.18f}")

if __name__ == "__main__":
    solve()