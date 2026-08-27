import sys
from collections import Counter

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    B = [int(next(it)) for _ in range(N)]
    
    fixedA = [x for x in A if x != -1]
    fixedB = [x for x in B if x != -1]
    cntA1 = A.count(-1)
    cntB1 = B.count(-1)
    k = len(fixedA)
    m = len(fixedB)
    
    # If all B are -1 or all A are -1, always possible
    if m == 0 or k == 0:
        print("Yes")
        return
    
    # If we can cover all fixed B with wildcards and all fixed A with wildcards
    if m <= cntA1 and k <= cntB1:
        print("Yes")
        return
    
    # Otherwise, we need at least one fixed-fixed match
    maxA = max(fixedA)
    maxB = max(fixedB)
    
    # L = minimum number of fixed-fixed pairs required
    L = max(m - cntA1, k - cntB1)
    # L >= 1 here because either m > cntA1 or k > cntB1
    
    counterA = Counter(fixedA)
    counterB = Counter(fixedB)
    
    t = {}  # sum -> max matching size
    for a, ca in counterA.items():
        for b, cb in counterB.items():
            s = a + b
            # contribution to max matching for sum s
            t[s] = t.get(s, 0) + min(ca, cb)
    
    found = False
    for s, size in t.items():
        if size >= L and s >= maxA and s >= maxB:
            found = True
            break
    
    print("Yes" if found else "No")

if __name__ == "__main__":
    solve()