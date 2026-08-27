import sys
import math

def solve():
    # Read N from stdin
    try:
        line = sys.stdin.read().strip()
        if not line:
            return
        N = int(line)
    except ValueError:
        return

    # We iterate d from 1 up to N^(1/3)
    # Since x^3 - y^3 = N and x > y >= 1, we have:
    # N = (x-y)(x^2 + xy + y^2) = d * (3y^2 + 3dy + d^2)
    # Since y >= 1, 3y^2 + 3dy + d^2 > d^2, so N > d^3 => d < N^(1/3)
    
    # Calculate upper bound for d
    # Use integer cube root approximation
    if N <= 0:
        print(-1)
        return
        
    # Upper bound for d: d^3 < N, so d <= floor(N^(1/3))
    # We can use math.isqrt for square root, but for cube root we can use exponentiation
    # or binary search. Given N <= 10^18, d <= 10^6.
    # Let's just iterate up to 10^6 + 100 to be safe, or compute exact bound.
    
    # Compute integer cube root of N
    # For N=10^18, cube root is 10^6.
    # We can use pow(N, 1/3) and adjust.
    d_max = int(round(N ** (1/3))) + 2
    
    found = False
    ans_x = -1
    ans_y = -1
    
    for d in range(1, d_max + 1):
        if d * d * d > N:
            break
            
        if N % d != 0:
            continue
            
        K = N // d
        # Equation: 3y^2 + 3dy + d^2 = K
        # => 3y^2 + 3dy + (d^2 - K) = 0
        # Discriminant D = (3d)^2 - 4*3*(d^2 - K)
        #                = 9d^2 - 12d^2 + 12K
        #                = 12K - 3d^2
        
        D = 12 * K - 3 * d * d
        
        if D < 0:
            continue
            
        # Check if D is a perfect square
        sqrt_D = math.isqrt(D)
        if sqrt_D * sqrt_D != D:
            continue
            
        # Roots: y = (-3d ± sqrt_D) / 6
        # We need y > 0, so we take the positive root: (-3d + sqrt_D) / 6
        # This requires sqrt_D > 3d
        
        if sqrt_D <= 3 * d:
            continue
            
        numerator = -3 * d + sqrt_D
        
        if numerator % 6 != 0:
            continue
            
        y = numerator // 6
        
        if y <= 0:
            continue
            
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
        print(-1)

if __name__ == "__main__":
    solve()