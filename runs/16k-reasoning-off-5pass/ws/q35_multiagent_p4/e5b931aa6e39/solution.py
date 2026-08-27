import sys
import math

def is_perfect_square(n):
    if n < 0:
        return False
    if n == 0:
        return True
    root = math.isqrt(n)
    return root * root == n

def solve():
    try:
        line = sys.stdin.read().strip()
        if not line:
            return
        N = int(line)
    except ValueError:
        return

    # We want x^3 - y^3 = N with x, y >= 1 integers.
    # Let d = x - y, so x = y + d, with d >= 1.
    # N = (x-y)(x^2 + xy + y^2) = d * ( (y+d)^2 + (y+d)y + y^2 )
    # N = d * (3y^2 + 3dy + d^2)
    # So, N/d = 3y^2 + 3dy + d^2
    # Let S = N/d. Then 3y^2 + 3dy + (d^2 - S) = 0.
    # This is a quadratic in y: 3y^2 + 3dy + (d^2 - S) = 0.
    # Discriminant D = (3d)^2 - 4*3*(d^2 - S) = 9d^2 - 12d^2 + 12S = 12S - 3d^2.
    # For y to be an integer, D must be a perfect square, say k^2.
    # Then y = (-3d + k) / 6. We need k > 3d (for y > 0) and (-3d + k) % 6 == 0.
    
    # Also, since S = 3y^2 + 3dy + d^2 >= 3(1)^2 + 3d(1) + d^2 = d^2 + 3d + 3,
    # we have N/d >= d^2 + 3d + 3 => N >= d^3 + 3d^2 + 3d.
    # For large N, d is roughly N^(1/3). We iterate d from 1 up to floor(N^(1/3)) + 1.
    
    limit = int(round(N ** (1/3))) + 2
    
    for d in range(1, limit + 1):
        if N % d != 0:
            continue
        
        S = N // d
        # D = 12*S - 3*d^2
        D = 12 * S - 3 * d * d
        
        if D < 0:
            continue
            
        if not is_perfect_square(D):
            continue
            
        k = math.isqrt(D)
        # y = (-3d + k) / 6
        numerator = -3 * d + k
        
        if numerator <= 0:
            continue
            
        if numerator % 6 != 0:
            continue
            
        y = numerator // 6
        x = y + d
        
        # Verify the solution
        if x**3 - y**3 == N:
            print(f"{x} {y}")
            return

    print("-1")

if __name__ == "__main__":
    solve()