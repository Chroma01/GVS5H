import sys
from math import isqrt

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])

    # Let d = x - y. Then N = d * (3*y*y + 3*d*y + d*d).
    # Since y >= 1, the second factor is > d*d, so d*d*d < N.
    # For N <= 10^18, this means d < 10^6.
    for d in range(1, 1_000_001):
        if d * d * d >= n:
            break

        if n % d != 0:
            continue

        q = n // d

        # Solve 3*y^2 + 3*d*y + d^2 = q.
        # Discriminant: D = 12*q - 3*d^2.
        # y = (-3*d + sqrt(D)) / 6.
        disc = 12 * q - 3 * d * d
        if disc < 0:
            continue

        s = isqrt(disc)
        if s * s != disc:
            continue

        if (s - 3 * d) % 6 != 0:
            continue

        y = (s - 3 * d) // 6
        if y <= 0:
            continue

        x = y + d

        # Final exact verification.
        if d * (3 * y * y + 3 * d * y + d * d) == n:
            print(x, y)
            return

    print(-1)

if __name__ == "__main__":
    main()