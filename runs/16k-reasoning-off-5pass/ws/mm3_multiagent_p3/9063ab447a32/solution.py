import sys
import math

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    P = [int(next(it)) for _ in range(N)]
    P.sort()
    
    # Upper bound: sum of max units per product if we spent all M on each individually
    # This is a safe upper bound for binary search
    max_possible = 0
    for p in P:
        max_possible += math.isqrt(M // p)
    # Add a small safety margin (N) in case of edge cases, but max_possible is already safe
    hi = max_possible + N
    lo = 0
    
    def feasible(X):
        if X == 0:
            return True
        R = X
        B = M
        for p in P:
            if R == 0:
                break
            # Maximum units we can take from this product given remaining budget
            # Use isqrt to avoid floating point issues
            max_take = math.isqrt(B // p)
            take = min(R, max_take)
            cost = take * take * p
            B -= cost
            R -= take
            if B < 0:
                return False
        return R == 0
    
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    
    print(lo)

if __name__ == "__main__":
    solve()