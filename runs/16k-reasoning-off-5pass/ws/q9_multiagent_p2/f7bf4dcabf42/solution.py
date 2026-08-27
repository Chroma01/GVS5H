import sys
from collections import defaultdict

# Increase recursion depth just in case, though we use iterative DP
sys.setrecursionlimit(2000)

def solve():
    # Read input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    M = int(input_data[1])
    S = input_data[2]
    
    MOD = 998244353
    
    # Precompute powers of 26 for the final step
    steps = min(N, M)
    remaining_steps = M - steps
    
    # Precompute multiplier
    multiplier = pow(26, remaining_steps, MOD)
    
    # Identify unique characters in S to optimize transitions
    S_int = [ord(c) - ord('a') for c in S]
    unique_chars_in_S = set(S_int)
    chars_not_in_S = 26 - len(unique_chars_in_S)
    
    # Precompute the list of unique chars in S for iteration
    unique_chars_list = list(unique_chars_in_S)
    
    # dp[state_tuple] = count
    # Initial state: empty vector, count 1
    dp = defaultdict(int)
    dp[()] = 1
    
    # Cache for S_int access
    # We will access S_int directly
    
    for i in range(steps):
        new_dp = defaultdict(int)
        
        # Optimization: 
        # We iterate over the current states.
        # For each state, we compute transitions for:
        # 1. Characters NOT in S (uniform transition: prefix max)
        # 2. Characters IN S (specific transition)
        
        # To speed up, we can separate the "not in S" calculation.
        # The "not in S" transition is: new_vec[p] = max(vec[0]...vec[p])
        # This results in a specific state for ALL states.
        # We can compute this state for each state and add count * chars_not_in_S.
        
        # Let's collect the "not in S" states first to avoid recomputing the logic structure?
        # No, the state depends on the specific values of vec.
        # But the logic is the same.
        
        # We will iterate over dp.items()
        # To minimize overhead, we convert dp to a list of items
        items = list(dp.items())
        
        # Pre-calculate the unique chars list to avoid global lookup
        # And S_int
        
        for vec, count in items:
            # vec is a tuple of length i
            
            # Case 1: Characters NOT in S
            # Transition: new_vec[p] = max(vec[0]...vec[p]) for p in 0..i-1
            # And new_vec[i] = max(vec[0]...vec[i-1])
            
            # Compute running max
            current_max = -1
            base_vec_list = []
            for v in vec:
                if v > current_max:
                    current_max = v
                base_vec_list.append(current_max)
            # The new state is base_vec_list + (base_vec_list[-1],)
            # Note: base_vec_list has length i. The last element is the max of all.
            # The new state has length i+1.
            base_state = tuple(base_vec_list) + (base_vec_list[-1],)
            
            if chars_not_in_S > 0:
                new_dp[base_state] = (new_dp[base_state] + count * chars_not_in_S) % MOD
            
            # Case 2: Characters IN S
            # For each unique char c in S, we compute the transition.
            # Transition: new_vec[p] = max_{0<=q<=p} (vec[q] + (1 if S[q]==c else 0))
            
            # We can optimize this by precomputing the 'boost' values for each char c
            # boost[q] = 1 if S[q] == c else 0
            # Then new_vec[p] = max(boosted_vals[0]...boosted_vals[p])
            
            # Since unique_chars_list is small (<= 26), we can iterate.
            # To speed up, we can precompute the indices for each character in S
            # But since N is small, checking S_int[q] == c is fast enough.
            
            for c in unique_chars_list:
                # Compute boosted_vals
                # vec is a tuple, S_int is a list
                # We can use a list comprehension
                # boosted_vals = [v + (1 if S_int[q] == c else 0) for q, v in enumerate(vec)]
                # This is O(i).
                
                # To make it faster, we can avoid the list comprehension overhead by unrolling or using local vars?
                # Given N <= 10, list comprehension is very fast.
                
                # Let's try to optimize the inner loop further.
                # We can compute the prefix max on the fly.
                
                # We need to construct the new state tuple.
                # new_vec_list = []
                # curr = -1
                # for q, v in enumerate(vec):
                #     val = v + (1 if S_int[q] == c else 0)
                #     if val > curr: curr = val
                #     new_vec_list.append(curr)
                # new_vec_list.append(curr)
                
                # This is O(i).
                
                # Let's implement this loop.
                
                # Optimization: 
                # We can precompute the 'boost' mask for each char c?
                # boost_mask = [1 if S_int[q] == c else 0 for q in range(N)]
                # But we only need up to i.
                
                # Let's use a local variable for S_int to avoid global lookup
                # And iterate.
                
                # To reduce tuple creation overhead, we can build a list and then tuple.
                
                new_vec_list = []
                curr = -1
                
                # We can iterate q from 0 to i-1
                for q, v in enumerate(vec):
                    # Check if S[q] == c
                    # S_int is a list, access is fast
                    if S_int[q] == c:
                        val = v + 1
                    else:
                        val = v
                    
                    if val > curr:
                        curr = val
                    new_vec_list.append(curr)
                
                # Append the last max for the new position i
                new_vec_list.append(curr)
                
                new_state = tuple(new_vec_list)
                new_dp[new_state] = (new_dp[new_state] + count) % MOD
        
        dp = new_dp

    # Collect answers
    ans = [0] * (N + 1)
    
    for vec, count in dp.items():
        # vec is a tuple of length steps
        # The LCS length is the last element of vec
        lcs_len = vec[-1]
        if lcs_len <= N:
            ans[lcs_len] = (ans[lcs_len] + count * multiplier) % MOD
            
    print(*(ans))

if __name__ == '__main__':
    solve()