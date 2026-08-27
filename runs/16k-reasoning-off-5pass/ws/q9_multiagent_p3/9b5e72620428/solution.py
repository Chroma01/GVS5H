import sys
from collections import Counter

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
        B = []
        for _ in range(N):
            B.append(int(next(iterator)))
    except StopIteration:
        return

    # Identify known values and fixed pairs
    known_A = []
    known_B = []
    fixed_sums = []
    
    for i in range(N):
        if A[i] != -1 and B[i] != -1:
            fixed_sums.append(A[i] + B[i])
        if A[i] != -1:
            known_A.append(A[i])
        if B[i] != -1:
            known_B.append(B[i])
            
    # Check consistency of fixed pairs
    if fixed_sums:
        base_S = fixed_sums[0]
        for s in fixed_sums:
            if s != base_S:
                print("No")
                return
    else:
        base_S = 0
        
    cntA = len(known_A)
    cntB = len(known_B)
    overlap = cntA + cntB - N
    
    # If overlap <= 0, we have enough slack to fill everything without strict pairing constraints
    # (other than S >= max values)
    if overlap <= 0:
        print("Yes")
        return

    # If overlap > 0, we need to find a sum S such that:
    # 1. S >= base_S
    # 2. S >= max(known_A)
    # 3. S >= max(known_B)
    # 4. The number of pairs (a, b) with a in known_A, b in known_B such that a+b=S is >= overlap
    
    if known_A:
        max_val_A = max(known_A)
    else:
        max_val_A = 0
        
    if known_B:
        max_val_B = max(known_B)
    else:
        max_val_B = 0
        
    lower_bound = max(base_S, max_val_A, max_val_B)
    
    # Count frequencies of sums a + b
    # Since N <= 2000, O(N^2) is acceptable (4*10^6 operations)
    sum_counts = Counter()
    
    for a in known_A:
        for b in known_B:
            s = a + b
            sum_counts[s] += 1
            
    # Check if any valid sum satisfies the condition
    possible = False
    for s, count in sum_counts.items():
        if s >= lower_bound and count >= overlap:
            possible = True
            break
            
    if possible:
        print("Yes")
    else:
        print("No")

if __name__ == '__main__':
    solve()