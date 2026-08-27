import sys
import math

def solve():
    # Read input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    
    # We want to find positive integers x, y such that x^3 - y^3 = N.
    # Let d = x - y. Then x = y + d.
    # Substituting x in the equation:
    # (y + d)^3 - y^3 = N
    # y^3 + 3y^2d + 3yd^2 + d^3 - y^3 = N
    # 3dy^2 + 3d^2y + d^3 - N = 0
    # This is a quadratic equation in y: 3d * y^2 + 3d^2 * y + (d^3 - N) = 0.
    # Dividing by 3d (since d >= 1):
    # y^2 + dy + (d^2/3 - N/(3d)) = 0
    # The discriminant D of this quadratic is:
    # D = d^2 - 4 * 1 * (d^2/3 - N/(3d))
    # D = d^2 - 4d^2/3 + 4N/(3d)
    # D = 4N/(3d) - d^2/3
    # D = (4N - d^3) / (3d)
    # For y to be an integer, D must be a perfect square, say k^2.
    # So, (4N - d^3) / (3d) = k^2  =>  4N - d^3 = 3d * k^2  =>  4N = d^3 + 3d * k^2 = d(d^2 + 3k^2).
    # Also, the solution for y is y = (-d + k) / 2.
    # Since y must be a positive integer, we need:
    # 1. k^2 = (4N - d^3) / (3d) to be an integer and a perfect square.
    # 2. k > d (so that y > 0).
    # 3. k and d must have the same parity (so that y is an integer).
    #    However, from 4N = d(d^2 + 3k^2), it can be shown that if a solution exists,
    #    k and d will always have the same parity.
    
    # We iterate over possible values of d.
    # From D >= 0, we have 4N - d^3 >= 0 => d^3 <= 4N => d <= (4N)^(1/3).
    # For N = 10^18, d <= ~1.6 * 10^6, which is small enough to iterate.
    
    d = 1
    # Use a while loop to avoid floating point inaccuracies for the bound.
    while d * d * d < 4 * N:
        numerator = 4 * N - d * d * d
        denominator = 3 * d
        
        # Check if numerator is divisible by denominator
        if numerator % denominator == 0:
            val = numerator // denominator
            # Check if val is a perfect square
            k = math.isqrt(val)
            if k * k == val:
                # Check if k > d for y > 0
                if k > d:
                    y = (k - d) // 2
                    x = y + d
                    print(f"{x} {y}")
                    return
        
        d += 1
        
    # If no solution is found after checking all valid d
    print("-1")

if __name__ == '__main__':
    solve()