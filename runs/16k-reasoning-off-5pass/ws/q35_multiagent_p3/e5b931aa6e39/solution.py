import sys
import math

def solve():
    # Read N from standard input
    try:
        line = sys.stdin.read().strip()
        if not line:
            return
        N = int(line)
    except ValueError:
        return

    # We need to find positive integers x, y such that x^3 - y^3 = N.
    # Factorize: (x-y)(x^2 + xy + y^2) = N.
    # Let d = x - y. Then x = y + d.
    # Substitute x into the second factor:
    # s = x^2 + xy + y^2 = (y+d)^2 + (y+d)y + y^2
    # s = y^2 + 2dy + d^2 + y^2 + dy + y^2
    # s = 3y^2 + 3dy + d^2
    # So, N = d * (3y^2 + 3dy + d^2)
    # Since y >= 1, we have:
    # N = 3y^2d + 3yd^2 + d^3 >= 3d + 3d^2 + d^3 > d^3
    # Therefore, d^3 < N, which implies d < N^(1/3).
    # This gives us an efficient bound for iterating d.

    # Calculate integer cube root upper bound for d
    # We iterate d from 1 up to floor(N^(1/3))
    # Using integer arithmetic to avoid floating point issues
    
    # Estimate upper bound for d
    # d_max = int(N**(1/3)) + 2 to be safe
    if N < 1:
        print("-1")
        return

    # Calculate integer cube root
    # For N=10^18, d_max is 10^6, which is small.
    d_max = int(round(N ** (1/3))) + 2
    
    found = False
    
    for d in range(1, d_max + 1):
        # Check if d divides N
        if N % d != 0:
            continue
            
        s = N // d
        
        # We have s = 3y^2 + 3dy + d^2
        # Rearranging: 3y^2 + 3dy + (d^2 - s) = 0
        # Quadratic formula for y:
        # y = [-3d + sqrt(9d^2 - 12(d^2 - s))] / 6
        # y = [-3d + sqrt(12s - 3d^2)] / 6
        
        discriminant = 12 * s - 3 * d * d
        
        if discriminant < 0:
            continue
            
        # Check if discriminant is a perfect square
        k = math.isqrt(discriminant)
        if k * k != discriminant:
            continue
            
        # Check if numerator is divisible by 6 and positive
        numerator = -3 * d + k
        
        if numerator > 0 and numerator % 6 == 0:
            y = numerator // 6
            x = y + d
            
            # Verify the solution
            if x**3 - y**3 == N:
                print(f"{x} {y}")
                found = True
                break
                
    if not found:
        print("-1")

if __name__ == "__main__":
    solve()