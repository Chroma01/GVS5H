import sys
import math

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    
    # Small N check: smallest positive difference is 2^3 - 1^3 = 7
    if N < 7:
        print(-1)
        return
    
    # Approach: iterate over d = x - y (the difference)
    # Since N = d * (3y^2 + 3dy + d^2) and 3y^2 + 3dy + d^2 > d^2,
    # we have d^3 < N, so d < N^(1/3) <= 10^6.
    
    # Compute upper bound for d
    max_d = int(round(N ** (1/3))) + 2
    # Ensure we cover all possibilities
    while (max_d + 1) ** 3 <= N:
        max_d += 1
    while max_d > 0 and max_d ** 3 > N and (max_d - 1) ** 3 > N:
        max_d -= 1
    
    for d in range(1, max_d + 1):
        if N % d != 0:
            continue
        # M = N / d = 3y^2 + 3dy + d^2
        M = N // d
        # Quadratic: 3y^2 + 3dy + (d^2 - M) = 0
        # Discriminant: D = 3(4M - d^2)
        D = 3 * (4 * M - d * d)
        if D < 0:
            continue
        s = math.isqrt(D)
        if s * s != D:
            continue
        # y = (-3d + s) / 6, need s > 3d for positive y
        if s <= 3 * d:
            continue
        num = s - 3 * d
        if num % 6 != 0:
            continue
        y = num // 6
        if y <= 0:
            continue
        x = y + d
        # Verify the solution
        if x * x * x - y * y * y == N:
            print(x, y)
            return
    
    print(-1)

if __name__ == "__main__":
    solve()