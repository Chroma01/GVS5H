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

    # We are looking for positive integers x, y such that x^3 - y^3 = N.
    # Let k = x - y. Since x > y, k >= 1.
    # Substituting x = y + k into the equation:
    # (y+k)^3 - y^3 = N
    # 3ky^2 + 3k^2y + k^3 = N
    # This is a quadratic in y: 3k*y^2 + 3k^2*y + (k^3 - N) = 0
    # Solving for y using the quadratic formula:
    # y = (-3k^2 + sqrt((3k^2)^2 - 4*3k*(k^3 - N))) / (2*3k)
    # y = (-3k^2 + sqrt(9k^4 - 12k^4 + 12kN)) / (6k)
    # y = (-3k^2 + sqrt(12kN - 3k^4)) / (6k)
    
    # Constraints: N <= 10^18.
    # Since y >= 1, the smallest value for the LHS is when y=1:
    # 3k + 3k^2 + k^3 <= N
    # This implies k^3 < N, so k < N^(1/3).
    # For N = 10^18, k < 10^6. We can iterate k from 1 to 10^6.
    
    # Calculate upper bound for k. 
    # k^3 < N => k < N^(1/3). We add a small buffer to be safe.
    limit = int(n**(1/3)) + 2
    
    for k in range(1, limit + 1):
        # Calculate discriminant D = 12*k*N - 3*k^4
        # We use integer arithmetic to avoid precision issues.
        
        term1 = 12 * k * n
        term2 = 3 * (k ** 4)
        delta = term1 - term2
        
        # If delta becomes negative, larger k will also yield negative delta (since term2 grows faster)
        if delta < 0:
            break
            
        # Check if delta is a perfect square
        sqrt_delta = math.isqrt(delta)
        
        if sqrt_delta * sqrt_delta != delta:
            continue
        
        # Numerator must be positive and divisible by 6k
        numerator = -3 * (k ** 2) + sqrt_delta
        
        if numerator <= 0:
            continue
            
        if numerator % (6 * k) == 0:
            y = numerator // (6 * k)
            if y > 0:
                x = y + k
                print(f"{x} {y}")
                return

    print("-1")

if __name__ == "__main__":
    solve()