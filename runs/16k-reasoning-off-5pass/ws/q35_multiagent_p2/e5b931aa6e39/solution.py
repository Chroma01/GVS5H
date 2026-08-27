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
    # N = (y+d)^3 - y^3 = 3y^2*d + 3y*d^2 + d^3 = d(3y^2 + 3yd + d^2)
    # So N = d * S, where S = 3y^2 + 3yd + d^2.
    # This implies d must be a divisor of N.
    # Also, S = N/d.
    # 3y^2 + 3dy + d^2 - N/d = 0.
    # Solving for y:
    # y = (-3d + sqrt(9d^2 - 12(d^2 - N/d))) / 6
    # y = (-3d + sqrt(12N/d - 3d^2)) / 6
    
    # For y to be a positive integer:
    # 1. d must divide N.
    # 2. Delta = 12N/d - 3d^2 must be a perfect square, say k^2.
    # 3. (-3d + k) must be divisible by 6.
    # 4. y = (-3d + k) / 6 must be > 0.
    
    # Condition 4 implies:
    # -3d + k > 0 => k > 3d => k^2 > 9d^2
    # 12N/d - 3d^2 > 9d^2 => 12N/d > 12d^2 => N/d > d^2 => N > d^3.
    # So we only need to check d such that d^3 < N.
    # Max d is roughly N^(1/3). For N=10^18, d up to 10^6.
    
    limit = int(round(N ** (1/3))) + 2
    
    for d in range(1, limit + 1):
        if d * d * d >= N:
            break
            
        if N % d != 0:
            continue
            
        S = N // d
        Delta = 12 * S - 3 * d * d
        
        if Delta <= 0:
            continue
            
        k = math.isqrt(Delta)
        if k * k != Delta:
            continue
            
        num = -3 * d + k
        if num <= 0:
            continue
            
        if num % 6 != 0:
            continue
            
        y = num // 6
        if y <= 0:
            continue
            
        x = y + d
        print(f"{x} {y}")
        return

    print("-1")

if __name__ == "__main__":
    solve()