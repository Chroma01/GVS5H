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
        if rem <= 0:
            break
        # max k with k^2 * p <= rem  =>  k = floor(sqrt(rem // p))  (use integer sqrt)
        k = math.isqrt(rem // p)
        if k == 0:
            # even one unit is too expensive; but we might still try other cheaper products later
            continue
        cost = k * k * p
        if cost > rem:
            # Should not happen with isqrt, but guard against overflow/precision
            k = math.isqrt(rem // p)
            cost = k * k * p
        rem -= cost
        total += k
    print(total)

if __name__ == "__main__":
    solve()