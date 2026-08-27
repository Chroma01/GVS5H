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

    # We want to find positive integers x, y such that x^3 - y^3 = n.
    # Let k = x - y. Since x > y >= 1, k >= 1.
    # Then x = y + k.
    # Substituting into the equation:
    # (y+k)^3 - y^3 = n
    # 3y^2k + 3yk^2 + k^3 = n
    # 3ky^2 + 3k^2y + (k^3 - n) = 0
    # This is a quadratic equation in y: Ay^2 + By + C = 0
    # where A = 3k, B = 3k^2, C = k^3 - n.
    # The discriminant D = B^2 - 4AC = (3k^2)^2 - 4(3k)(k^3 - n)
    # D = 9k^4 - 12k^4 + 12kn = 12kn - 3k^4 = 3k(4n - k^3).
    # For y to be a real number, D >= 0 => 4n >= k^3 => k <= (4n)^(1/3).
    # For y to be an integer, D must be a perfect square, and the numerator
    # (-B + sqrt(D)) must be divisible by 2A.
    # y = (-3k^2 + sqrt(D)) / (6k).

    # Max value for k is approx (4 * 10^18)^(1/3) approx 1.58 * 10^6.
    # We iterate k from 1 upwards.

    # Calculate limit for k safely. 
    # k^3 <= 4n => k <= (4n)^(1/3).
    # Using integer arithmetic to avoid precision issues with large floats.
    # We can estimate limit_k.
    limit_k = int((4 * n) ** (1/3)) + 2
    
    for k in range(1, limit_k + 1):
        # Calculate discriminant D = 3k(4n - k^3)
        term = 4 * n - k**3
        if term < 0:
            break
        
        d = 3 * k * term
        
        # Check if d is a perfect square
        s = math.isqrt(d)
        if s * s != d:
            continue
        
        # Calculate numerator for y: -3k^2 + s
        # We need (-3k^2 + s) to be divisible by 6k and result > 0
        numerator = -3 * k * k + s
        
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