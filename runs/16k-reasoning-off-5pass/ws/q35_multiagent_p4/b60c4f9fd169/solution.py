import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    K = int(input_data[0])
    S = input_data[1]
    T = input_data[2]
    
    n = len(S)
    m = len(T)
    
    # If the length difference is greater than K, it's impossible
    if abs(n - m) > K:
        print("No")
        return
    
    # We'll use two arrays: prev and curr
    # prev[j] stores the edit distance for S[0:i-1] and T[0:j]
    # curr[j] stores the edit distance for S[0:i] and T[0:j]
    
    # Initialize prev for i=0 (empty S)
    # prev[j] = j for j in 0..m, but we cap at K+1
    # However, we only need to store values for j in [0, min(m, K)] initially
    # But since we access j in [i-K, i+K], let's just create arrays of size m+1
    # and only compute valid ranges.
    
    # To save space and time, we can use a list of size m+1
    # Initialize prev
    prev = [0] * (m + 1)
    for j in range(m + 1):
        prev[j] = j if j <= K else K + 1
    
    for i in range(1, n + 1):
        curr = [0] * (m + 1)
        
        # Determine the range of j to compute
        # j must be in [max(0, i-K), min(m, i+K)]
        j_start = max(0, i - K)
        j_end = min(m, i + K)
        
        # Handle j=0 separately: curr[0] = i (delete all characters from S so far)
        if i <= K:
            curr[0] = i
        else:
            curr[0] = K + 1
        
        for j in range(j_start, j_end + 1):
            if j == 0:
                continue # Already handled
            
            # Cost for replacement/match
            cost = 0 if S[i-1] == T[j-1] else 1
            
            # Options:
            # 1. Delete from S: prev[j] + 1
            # 2. Insert into S: curr[j-1] + 1
            # 3. Replace/Match: prev[j-1] + cost
            
            val_delete = prev[j] + 1
            val_insert = curr[j-1] + 1
            val_replace = prev[j-1] + cost
            
            curr[j] = min(val_delete, val_insert, val_replace)
            
            # Cap at K+1
            if curr[j] > K:
                curr[j] = K + 1
        
        prev = curr
    
    if prev[m] <= K:
        print("Yes")
    else:
        print("No")

solve()