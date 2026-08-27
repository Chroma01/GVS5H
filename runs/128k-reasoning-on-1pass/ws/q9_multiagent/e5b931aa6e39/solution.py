import sys

# Function to compute integer square root
def isqrt(n):
    if n < 0:
        raise ValueError
    if n == 0:
        return 0
    x = 1 << (n.bit_length() // 2)
    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x
        x = y

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])

    # Iterate over possible values of d = x - y
    # Since y >= 1, x = y + d >= 1 + d
    # x^3 - y^3 = (y+d)^3 - y^3 = 3y^2d + 3yd^2 + d^3 = N
    # Since y >= 1, N >= 3d + 3d^2 + d^3 > d^3
    # So d^3 < N is a necessary condition.
    # We iterate d starting from 1.
    
    d = 1
    while True:
        d3 = d * d * d
        if d3 >= N:
            break
        
        # We need to solve 3dy^2 + 3d^2y + (d^3 - N) = 0 for y
        # Discriminant Delta = (3d^2)^2 - 4(3d)(d^3 - N)
        #                   = 9d^4 - 12d(d^3 - N)
        #                   = 12dN - 3d^4
        
        # Calculate Delta
        # d4 = d3 * d
        # delta = 12 * d * N - 3 * d4
        
        # Optimization: compute d4
        d4 = d3 * d
        delta = 12 * d * N - 3 * d4
        
        # Check if Delta is a perfect square
        k = isqrt(delta)
        if k * k == delta:
            # Check if y is a positive integer
            # y = (-3d^2 + k) / (6d)
            # We need (k - 3d^2) to be divisible by 6d and result > 0
            
            numerator = k - 3 * d * d
            if numerator > 0 and numerator % (6 * d) == 0:
                y = numerator // (6 * d)
                x = y + d
                print(f"{x} {y}")
                return

        d += 1

    print("-1")

if __name__ == '__main__':
    solve()