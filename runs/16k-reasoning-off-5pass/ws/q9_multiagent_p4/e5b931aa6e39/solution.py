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

    # We are looking for positive integers x, y such that x^3 - y^3 = n.
    # Let k = x - y. Since x > y (as n > 0), k >= 1.
    # Substituting x = y + k into the equation:
    # (y + k)^3 - y^3 = n
    # 3ky^2 + 3k^2y + k^3 = n
    # 3ky^2 + 3k^2y + (k^3 - n) = 0
    # This is a quadratic equation in y: Ay^2 + By + C = 0
    # where A = 3k, B = 3k^2, C = k^3 - n.
    
    # The discriminant D = B^2 - 4AC
    # D = (3k^2)^2 - 4(3k)(k^3 - n)
    # D = 9k^4 - 12k^4 + 12kn
    # D = 12kn - 3k^4
    
    # For y to be a positive integer:
    # 1. D must be non-negative.
    # 2. D must be a perfect square.
    # 3. The root (-B + sqrt(D)) must be divisible by 2A and positive.
    #    y = (-3k^2 + sqrt(D)) / (6k)
    
    # Constraints: n <= 10^18.
    # D >= 0 => 12kn >= 3k^4 => 4n >= k^3 => k <= (4n)^(1/3).
    # For n = 10^18, k <= (4 * 10^18)^(1/3) approx 1.58 * 10^6.
    # Iterating k up to ~1.6 million is well within time limits for Python.
    
    k = 1
    while True:
        # Calculate discriminant D = 12*k*n - 3*k^4
        # Using integer arithmetic to avoid precision issues
        term1 = 12 * k * n
        term2 = 3 * (k ** 4)
        d = term1 - term2
        
        if d < 0:
            # If D < 0, then 4n < k^3. Since k increases, k^3 grows faster than 4n,
            # so D will remain negative for all subsequent k. We can stop.
            break
        
        # Check if d is a perfect square
        root = math.isqrt(d)
        if root * root != d:
            k += 1
            continue
        
        # Solve for y: y = (-3k^2 + root) / (6k)
        numerator = -3 * (k ** 2) + root
        denominator = 6 * k
        
        # y must be a positive integer
        if numerator <= 0:
            k += 1
            continue
            
        if numerator % denominator == 0:
            y = numerator // denominator
            x = y + k
            
            # Verify the solution to ensure correctness
            # Note: x^3 - y^3 can be large, but Python handles large integers automatically.
            if x**3 - y**3 == n:
                print(f"{x} {y}")
                return
        
        k += 1

    print("-1")

if __name__ == "__main__":
    solve()