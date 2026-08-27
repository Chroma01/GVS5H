import sys
from collections import Counter, defaultdict

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

    # Extract known values (non -1)
    K_A = [x for x in A if x != -1]
    K_B = [x for x in B if x != -1]
    
    len_K_A = len(K_A)
    len_K_B = len(K_B)
    
    # Number of fillable slots
    N_A = N - len_K_A
    N_B = N - len_K_B
    
    # We need to cover at least R elements of K_A using fixed slots from K_B
    # The remaining can be covered by flexible slots (from N_B)
    R = len_K_A - N_B
    
    # If we have enough flexible slots to cover all K_A, it's always possible
    if R <= 0:
        print("Yes")
        return

    # Calculate minimum required S
    # S must be >= max(K_B) to ensure S - b >= 0 for all b in K_B
    # S must be >= max(K_A) to ensure flexible slots can produce values in K_A
    max_K_B = max(K_B) if K_B else 0
    max_K_A = max(K_A) if K_A else 0
    min_S = max(max_K_B, max_K_A)
    
    cntA = Counter(K_A)
    cntB = Counter(K_B)
    
    # We need to find S >= min_S such that:
    # sum(min(cntA[y], cntB[S-y])) >= R
    # We iterate over all pairs (y, b) to generate candidate S values.
    # To do this in O(N^2), we group y by S = y + b.
    
    candidates = defaultdict(list)
    
    for y in K_A:
        for b in K_B:
            s = y + b
            if s >= min_S:
                candidates[s].append(y)
    
    # Check each candidate S
    for s, ys in candidates.items():
        # Calculate matches for this S
        # We need to sum min(cntA[y], cntB[s-y]) for all unique y in ys
        # ys contains duplicates, so we use a set to get unique y's
        unique_ys = set(ys)
        
        current_matches = 0
        for y in unique_ys:
            b_needed = s - y
            if b_needed in cntB:
                # We can match at most min(count of y in A, count of b_needed in B)
                current_matches += min(cntA[y], cntB[b_needed])
                if current_matches >= R:
                    print("Yes")
                    return
                    
    print("No")

if __name__ == '__main__':
    solve()