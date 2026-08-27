import sys
from collections import Counter

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    B = list(map(int, data[1+n:1+2*n]))
    
    a_fixed = [x for x in A if x != -1]
    b_fixed = [x for x in B if x != -1]
    cnt_a_wild = n - len(a_fixed)
    cnt_b_wild = n - len(b_fixed)
    
    max_a = max(a_fixed) if a_fixed else 0
    max_b = max(b_fixed) if b_fixed else 0
    lower_bound = max(max_a, max_b, 0)
    
    required = max(0, len(a_fixed) - cnt_b_wild, len(b_fixed) - cnt_a_wild)
    
    if required == 0:
        print("Yes")
        return
    
    if not a_fixed or not b_fixed:
        print("No")
        return
    
    cnt_a = Counter(a_fixed)
    cnt_b = Counter(b_fixed)
    
    match_count = {}
    for a, ca in cnt_a.items():
        for b, cb in cnt_b.items():
            s = a + b
            if s >= lower_bound:
                match_count[s] = match_count.get(s, 0) + min(ca, cb)
    
    for s, m in match_count.items():
        if m >= required:
            print("Yes")
            return
    
    print("No")

solve()