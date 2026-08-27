import sys
import math

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    d = 1
    while d ** 3 <= N:
        if N % d == 0:
            val = 4 * N - d ** 3
            if val > 0:
                D = 3 * d * val
                s = math.isqrt(D)
                if s * s == D:
                    num = 3 * d * d + s
                    den = 6 * d
                    if num % den == 0:
                        x = num // den
                        y = x - d
                        if y > 0:
                            sys.stdout.write(f"{x} {y}\n")
                            return
        d += 1
    sys.stdout.write("-1\n")

if __name__ == "__main__":
    solve()