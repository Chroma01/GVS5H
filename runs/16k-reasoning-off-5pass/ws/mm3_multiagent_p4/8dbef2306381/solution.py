import sys
from math import gcd
from collections import deque

def solve():
    import sys
    from math import gcd
    from collections import deque
    
    input_data = sys.stdin.read().split()
    it = iter(input_data)
    N = int(next(it))
    M = int(next(it))
    A = int(next(it))
    B = int(next(it))
    bad_intervals = []
    for _ in range(M):
        L = int(next(it))
        R = int(next(it))
        bad_intervals.append((L, R))
    
    # Precompute representable differences
    LIMIT = 5000
    rep = [False] * (LIMIT + 1)
    rep[0] = True
    q = deque([0])
    while q:
        d = q.popleft()
        if d > LIMIT:
            continue
        for step in range(A, B+1):
            nd = d + step
            if nd <= LIMIT and not rep[nd]:
                rep[nd] = True
                q.append(nd)
    
    # Find Frobenius number F
    F = 0
    for d in range(1, LIMIT+1):
        if not rep[d]:
            F = d
    
    g = gcd(A, B)
    
    def is_representable(d):
        if d < 0:
            return False
        if d == 0:
            return True
        if d <= LIMIT:
            return rep[d]
        if g == 1:
            return True
        else:
            return (d % g == 0)
    
    def exists_representable(a, b):
        if a > b:
            return False
        if b - a <= 2000:
            for d in range(a, b+1):
                if is_representable(d):
                    return True
            return False
        if g == 1:
            if b > F:
                return True
            for d in range(a, min(b, F)+1):
                if is_representable(d):
                    return True
            return False
        else:
            first = a + ((g - a % g) % g)
            if first > b:
                return False
            if is_representable(first):
                return True
            if b > F:
                cand = max(F+1, first)
                if cand % g != 0:
                    cand += (g - cand % g) % g
                if cand <= b:
                    return True
            return False
    
    def largest_representable(a, b):
        if a > b:
            return None
        if b - a <= 2000:
            for d in range(b, a-1, -1):
                if is_representable(d):
                    return d
            return None
        if g == 1:
            if b > F:
                return b
            for d in range(b, max(a, 0), -1):
                if is_representable(d):
                    return d
            return None
        else:
            d = b - (b % g)
            while d >= a:
                if is_representable(d):
                    return d
                d -= g
            return None
    
    # Build safe zones
    zones = []
    if M == 0:
        zones.append((1, N))
    else:
        if bad_intervals[0][0] > 1:
            zones.append((1, bad_intervals[0][0] - 1))
        for i in range(M-1):
            L_curr_bad = bad_intervals[i][1]
            R_next_bad = bad_intervals[i+1][0]
            if L_curr_bad + 1 <= R_next_bad - 1:
                zones.append((L_curr_bad + 1, R_next_bad - 1))
        if bad_intervals[-1][1] < N:
            zones.append((bad_intervals[-1][1] + 1, N))
    
    p = 1
    for i in range(len(zones)):
        L_curr, R_curr = zones[i]
        if p < L_curr or p > R_curr:
            print("No")
            return
        
        if i == len(zones) - 1:
            if is_representable(N - p):
                print("Yes")
            else:
                print("No")
            return
        else:
            L_next, R_next = zones[i+1]
            # Check direct jump
            if p >= L_next - B and p <= R_next - A:
                p = min(R_next, p + B)
                continue
            x_low = max(L_curr, L_next - B)
            x_high = min(R_curr, R_next - A)
            if x_low > x_high:
                print("No")
                return
            a = x_low - p
            b = x_high - p
            a = max(a, 1)
            if not exists_representable(a, b):
                print("No")
                return
            d_max = largest_representable(a, b)
            if d_max is None:
                print("No")
                return
            x = p + d_max
            p = min(R_next, x + B)

if __name__ == "__main__":
    solve()