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
    # Substituting: (y+d)^3 - y^3 = n
    # y^3 + 3y^2d + 3yd^2 + d^3 - y^3 = n
    # 3y^2d + 3yd^2 + d^3 = n
    # d(3y^2 + 3dy + d^2) = n
    
    # Since y >= 1, we have 3y^2 + 3dy + d^2 > d^2.
    # So n = d * (something > d^2) > d^3.
    # Therefore, d^3 < n, which implies d < n^(1/3).
    # Since n <= 10^18, d < 10^6.
    
    # We iterate d from 1 upwards.
    # For a fixed d, we check if n is divisible by d.
    # If so, we solve the quadratic equation for y:
    # 3d * y^2 + 3d^2 * y + (d^3 - n) = 0
    # Let A = 3d, B = 3d^2, C = d^3 - n.
    # Discriminant D = B^2 - 4AC.
    # If D is a perfect square, say k^2, then y = (-B + k) / (2A).
    # We check if y is a positive integer.
    
    # Calculate limit for d. Since d^3 < n, d < n^(1/3).
    # We add a small buffer to handle floating point inaccuracies.
    # For n = 10^18, n^(1/3) = 10^6.
    limit = int(n**(1/3)) + 2
    
    for d in range(1, limit + 1):
        # Check divisibility
        if n % d != 0:
            continue
        
        # Equation: 3d*y^2 + 3d^2*y + (d^3 - n) = 0
        # A = 3d
        # B = 3d^2
        # C = d^3 - n
        
        a = 3 * d
        b = 3 * d * d
        c = d * d * d - n
        
        # Discriminant
        delta = b * b - 4 * a * c
        
        if delta < 0:
            continue
            
        sqrt_delta = int(math.isqrt(delta))
        if sqrt_delta * sqrt_delta != delta:
            continue
        
        # y = (-b + sqrt_delta) / (2a)
        # We need -b + sqrt_delta to be positive and divisible by 2a
        # Note: Since n > d^3, c is negative, so -4ac is positive.
        # Thus delta = b^2 + positive_term > b^2.
        # So sqrt_delta > b. Numerator is positive.
        
        numerator = -b + sqrt_delta
        denominator = 2 * a
        
        if numerator <= 0 or numerator % denominator != 0:
            continue
            
        y = numerator // denominator
        
        if y <= 0:
            continue
            
        x = y + d
        
        # Verify solution to be absolutely sure
        if x**3 - y**3 == n:
            print(f"{x} {y}")
            return

    print("-1")

if __name__ == "__main__":
    solve()