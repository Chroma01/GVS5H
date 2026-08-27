import sys
import math

def solve():
    N = int(sys.stdin.readline().strip())
    y = 1
    # Maximum possible y is roughly N^(1/3). Use a safe upper bound.
    max_y = int(round(N ** (1/3))) + 3
    if max_y < 1:
        max_y = 1
    for y in range(1, max_y + 1):
        y3 = y * y * y
        if y3 >= N:
            # If y^3 >= N, the minimal difference (y+1)^3 - y^3 = 3y^2 + 3y + 1
            # may still be > N, but we can still check.
            pass
        target = N + y3
        # Initial guess using float
        x_guess = int(target ** (1/3))
        # Correct the guess to be the exact integer cube root
        x = x_guess
        # Adjust up
        while (x + 1) ** 3 <= target:
            x += 1
        # Adjust down
        while x ** 3 > target:
            x -= 1
        if x ** 3 == target and x > y:
            print(x, y)
            return
    # If no solution found
    print(-1)

if __name__ == "__main__":
    solve()