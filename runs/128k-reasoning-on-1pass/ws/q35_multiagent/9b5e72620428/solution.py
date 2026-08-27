import sys
from collections import Counter, defaultdict

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
        B = [int(next(iterator)) for _ in range(N)]
    except StopIteration:
        return
        
    K_A = [x for x in A if x != -1]
    K_B = [x for x in B if x != -1]
    
    U_A = len(A) - len(K_A)
    U_B = len(B) - len(K_B)
    
    req = len(K_A) + len(K_B) - N
    
    if req <= 0:
        print("Yes")
        return
        
    if req > len(K_A) * len(K_B):
        print("No")
        return
        
    min_S = 0
    if K_A:
        min_S = max(min_S, max(K_A))
    if K_B:
        min_S = max(min_S, max(K_B))
        
    if req == 1:
        print("Yes")
        return
        
    cnt_A = Counter(K_A)
    cnt_B = Counter(K_B)
    
    sum_count = defaultdict(int)
    
    items_A = list(cnt_A.items())
    items_B = list(cnt_B.items())
    
    for a, count_a in items_A:
        for b, count_b in items_B:
            s = a + b
            if s >= min_S:
                sum_count[s] += count_a * count_b
                
    for s, count in sum_count.items():
        if count >= req:
            print("Yes")
            return
            
    print("No")

if __name__ == '__main__':
    solve()