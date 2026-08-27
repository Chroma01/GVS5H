import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    # Constraints: A_i <= 10^7, so max sum is 2*10^7
    MAX_VAL = 10000000
    MAX_SUM = 20000000
    
    # Frequency array for A. 
    # Using a list is faster than a dict for dense access.
    # We also maintain a set of distinct elements to speed up the inner loop iteration.
    cnt = [0] * (MAX_VAL + 1)
    distinct_A = set()
    
    for x in A:
        cnt[x] += 1
        distinct_A.add(x)
    
    # Convert to sorted list for predictable iteration
    distinct_A = sorted(list(distinct_A))
    
    ans = 0
    
    # Iterate over all odd integers v (potential values of f(S))
    # f(S) = v implies S = v * 2^k for some k >= 0
    # We iterate v from 1 to MAX_VAL (odd only)
    # The maximum possible sum is 2*10^7, so v can go up to 10^7.
    for v in range(1, MAX_VAL + 1, 2):
        # For a fixed v, we need to sum v * P[S] for all S = v * 2^k <= MAX_SUM
        # P[S] is the number of pairs (i, j) with i <= j such that A_i + A_j = S
        
        S = v
        while S <= MAX_SUM:
            # Calculate P[S]
            # P[S] = sum_{x} cnt[x] * cnt[S-x] (handling i <= j)
            # To optimize, we iterate only over distinct elements present in A
            # and check if the complement exists in the frequency array.
            
            count_S = 0
            
            # We iterate x in distinct_A. Since x + y = S, we need x < S.
            # Also we need y = S - x to be in the range [1, MAX_VAL] (which is implied if x < S and S <= MAX_SUM)
            # and y must be present in A.
            
            # Optimization: Since distinct_A is sorted, we can break early if x >= S
            for x in distinct_A:
                if x >= S:
                    break
                
                y = S - x
                # Check if y exists in A
                # Since cnt is a list, we can check cnt[y] directly if y is within bounds
                # y is guaranteed to be < MAX_SUM because x >= 1 and S <= MAX_SUM
                if y <= MAX_VAL: # y must be a valid element in A
                    if cnt[y] > 0:
                        c1 = cnt[x]
                        c2 = cnt[y]
                        if x == y:
                            # Pairs (i, i) where A_i = x. Number of ways is C(cnt[x], 2)
                            count_S += c1 * (c1 - 1) // 2
                        else:
                            # Pairs (i, j) with A_i = x, A_j = y. Since x != y, order doesn't matter for the set {i, j}
                            # But we are summing over i <= j.
                            # If we iterate distinct elements, we count each pair {x, y} once.
                            # The number of pairs is cnt[x] * cnt[y].
                            count_S += c1 * c2
            
            # Add contribution of v for this S
            ans += v * count_S
            
            # Move to next multiple S = S * 2
            # Check for overflow before multiplying
            if S > MAX_SUM // 2:
                break
            S *= 2
            
    print(ans)

if __name__ == '__main__':
    solve()