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

    # We want to find positive integers x, y such that x^3 - y^3 = N.
    # Factorize: (x-y)(x^2 + xy + y^2) = N.
    # Let d = x - y, S = x^2 + xy + y^2. Then d * S = N.
    # Since x, y >= 1 and x > y, d >= 1.
    # Also, S = (y+d)^2 + (y+d)y + y^2 = 3y^2 + 3dy + d^2.
    # Since y >= 1, S = 3y^2 + 3dy + d^2 >= 3 + 3d + d^2 > d^2.
    # Therefore, N = d * S > d * d^2 = d^3.
    # So d < N^(1/3). We can iterate d from 1 up to int(N**(1/3)) + 1.
    
    limit = int(round(N ** (1/3))) + 2
    
    for d in range(1, limit + 1):
        if N % d != 0:
            continue
        
        S = N // d
        
        # We need to solve 3y^2 + 3dy + (d^2 - S) = 0 for positive integer y.
        # Quadratic formula: y = (-3d +/- sqrt(D)) / 6
        # D = (3d)^2 - 4*3*(d^2 - S) = 9d^2 - 12d^2 + 12S = 12S - 3d^2
        
        D = 12 * S - 3 * d * d
        
        if D < 0:
            continue
            
        if not is_perfect_square(D):
            continue
            
        k = math.isqrt(D)
        
        # We need y = (-3d + k) / 6 to be a positive integer.
        # Note: -3d - k would be negative since k >= 0 and d >= 1, so we only check +k.
        
        numerator = -3 * d + k
        
        if numerator <= 0:
            continue
            
        if numerator % 6 == 0:
            y = numerator // 6
            x = y + d
            # Verify solution just in case
            if x**3 - y**3 == N:
                print(f"{x} {y}")
                return

    print("-1")

if __name__ == "__main__":
    solve()