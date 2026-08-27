import sys
import math

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    P = [int(next(it)) for _ in range(N)]
    P.sort()
    rem = M
    total = 0
    for p in P:
        if rem == 0:
            break
        # If even one unit costs more than remaining budget, we cannot buy from this product.
        if p > rem:
            # Since P is sorted, all later P are >= p, so we can break early.
            break
        # Maximum number of units we can buy from this product:
        # x^2 * p <= rem  =>  x <= sqrt(rem // p)
        max_units = math.isqrt(rem // p)
        total += max_units
        rem -= max_units * max_units * p
    print(total)

if __name__ == "__main__":
    solve()