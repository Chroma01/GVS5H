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
    # Let k = x - y. Since x > y, k >= 1.
    # Then x = y + k.
    # Substituting into the equation:
    # (y + k)^3 - y^3 = n
    # 3*y^2*k + 3*y*k^2 + k^3 = n
    # This is a quadratic equation in y: (3k)y^2 + (3k^2)y + (k^3 - n) = 0
    # Using the quadratic formula for y:
    # y = (-3k^2 + sqrt(D)) / (6k)
    # where D = (3k^2)^2 - 4*(3k)*(k^3 - n)
    #       = 9k^4 - 12k^4 + 12kn
    #       = 12kn - 3k^4
    #       = 3k(4n - k^3)
    
    # Constraints:
    # 1 <= n <= 10^18
    # Since y >= 1, we have 3k*y^2 < n => k < n/3.
    # Also, since y >= 1, n = 3ky^2 + 3yk^2 + k^3 >= 3k + 3k^2 + k^3.
    # Thus k^3 < n, so k < n^(1/3).
    # For n = 10^18, k <= 10^6. Iterating k from 1 to 10^6 is efficient.

    # Calculate upper bound for k. 
    # k^3 < n implies k < n^(1/3). We add a small buffer to be safe.
    limit = int(n**(1/3)) + 2
    
    for k in range(1, limit + 1):
        # Calculate discriminant D = 3*k*(4*n - k^3)
        # We must ensure 4*n - k^3 > 0 for D to be positive.
        # Since k < n^(1/3), k^3 < n, so 4n - k^3 > 3n > 0.
        
        term1 = 4 * n - k**3
        if term1 <= 0:
            break
            
        d = 3 * k * term1
        
        # Check if d is a perfect square
        s = math.isqrt(d)
        if s * s != d:
            continue
        
        # Calculate numerator: -3k^2 + s
        # We need y to be a positive integer.
        # y = (-3k^2 + s) / (6k)
        
        numerator = -3 * k * k + s
        denominator = 6 * k
        
        if numerator <= 0:
            continue
            
        if numerator % denominator == 0:
            y = numerator // denominator
            if y > 0:
                x = y + k
                # Verify the solution to be absolutely sure
                if x**3 - y**3 == n:
                    print(f"{x} {y}")
                    return

    print("-1")

if __name__ == '__main__':
    solve()