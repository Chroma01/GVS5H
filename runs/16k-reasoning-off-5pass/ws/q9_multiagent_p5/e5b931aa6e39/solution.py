import sys
import math

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    try:
        n = int(input_data[0])
    except ValueError:
        return

    # We need to find positive integers x, y such that x^3 - y^3 = n.
    # Let d = x - y. Then x = y + d.
    # (y+d)^3 - y^3 = n
    # 3y^2d + 3yd^2 + d^3 = n
    # d(3y^2 + 3yd + d^2) = n
    # Since y >= 1 and d >= 1, the term (3y^2 + 3yd + d^2) > d^2.
    # Therefore, n = d * (...) > d^3, so d < n^(1/3).
    # Given n <= 10^18, d <= 10^6.
    
    # We iterate d from 1 up to floor(n^(1/3)) + 2 to be safe.
    # For each d, we check if n is divisible by d.
    # If so, let k = n / d. We solve 3y^2 + 3dy + d^2 = k for y.
    # This is a quadratic equation: 3y^2 + (3d)y + (d^2 - k) = 0.
    # Discriminant D = (3d)^2 - 4*3*(d^2 - k) = 9d^2 - 12d^2 + 12k = 12k - 3d^2.
    # y = (-3d + sqrt(D)) / 6. (We take the positive root).
    # We check if D is a perfect square and if the resulting y is a positive integer.

    # Calculate upper bound for d. Since d^3 < n, d < n^(1/3).
    # We add a small buffer to ensure we cover the edge case where d is close to the root.
    # For n=10^18, n^(1/3) = 10^6.
    limit = int(n**(1/3)) + 2
    
    for d in range(1, limit + 1):
        if n % d != 0:
            continue
        
        k = n // d
        # Equation: 3y^2 + 3dy + d^2 - k = 0
        # Discriminant
        delta = 12 * k - 3 * d * d
        
        if delta < 0:
            continue
            
        sqrt_delta = int(math.isqrt(delta))
        if sqrt_delta * sqrt_delta != delta:
            continue
        
        # y = (-3d + sqrt_delta) / 6
        numerator = -3 * d + sqrt_delta
        if numerator <= 0:
            continue
            
        if numerator % 6 == 0:
            y = numerator // 6
            if y >= 1:
                x = y + d
                # Double check to be safe against floating point issues or logic slips
                # Use integer arithmetic for verification
                if x**3 - y**3 == n:
                    print(f"{x} {y}")
                    return

    print("-1")

if __name__ == '__main__':
    solve()