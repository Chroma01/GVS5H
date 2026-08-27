import sys
import math

def solve():
    try:
        line = sys.stdin.read().strip()
        if not line:
            return
        N = int(line)
    except ValueError:
        return

    # We want to find positive integers x, y such that x^3 - y^3 = N.
    # Let d = x - y. Then x = y + d.
    # Substituting: (y+d)^3 - y^3 = N
    # y^3 + 3y^2d + 3yd^2 + d^3 - y^3 = N
    # 3y^2d + 3yd^2 + d^3 = N
    # d(3y^2 + 3yd + d^2) = N
    
    # So d must be a divisor of N.
    # Also, since y >= 1, we have 3y^2 + 3yd + d^2 >= 3 + 3d + d^2 > d^2.
    # Therefore, N = d * (3y^2 + 3yd + d^2) > d * d^2 = d^3.
    # This implies d^3 < N, so d < N^(1/3).
    # For N <= 10^18, d < 10^6. We can iterate d from 1 to int(N**(1/3)) + 2.

    limit = int(round(N ** (1/3))) + 2
    
    found = False
    ans_x = -1
    ans_y = -1

    for d in range(1, limit + 1):
        if N % d != 0:
            continue
        
        M = N // d
        # We need to solve 3y^2 + 3dy + d^2 = M for positive integer y.
        # 3y^2 + 3dy + (d^2 - M) = 0
        
        # Quadratic formula: y = [-3d +/- sqrt(9d^2 - 12(d^2 - M))] / 6
        # Discriminant D = 9d^2 - 12d^2 + 12M = 12M - 3d^2
        D = 12 * M - 3 * d * d
        
        if D < 0:
            continue
            
        sqrt_D = int(math.isqrt(D))
        if sqrt_D * sqrt_D != D:
            continue
            
        # y = (-3d + sqrt_D) / 6  (we take positive root since y > 0)
        # Check if numerator is divisible by 6 and positive
        numerator = -3 * d + sqrt_D
        if numerator <= 0:
            continue
        if numerator % 6 != 0:
            continue
            
        y = numerator // 6
        x = y + d
        
        # Verify the solution
        if x**3 - y**3 == N:
            ans_x = x
            ans_y = y
            found = True
            break
            
    if found:
        print(f"{ans_x} {ans_y}")
    else:
        print("-1")

if __name__ == '__main__':
    solve()