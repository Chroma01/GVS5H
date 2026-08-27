import sys
from math import gcd
from collections import defaultdict

def solve():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    A = [int(x) for x in data[2:2+N]]
    
    MAX_VAL = 1000000
    
    # For each value v, store the list of indices where A[i] == v
    value_to_indices = defaultdict(list)
    for i in range(N):
        value_to_indices[A[i]].append(i)
    
    # For each candidate g, count how many elements in A are multiples of g
    # Also, we need to know which indices have A[i] as a multiple of g
    # To avoid storing all indices for all g (which could be memory heavy),
    # we'll use a different approach:
    
    # Step 1: Compute count[g] = number of elements in A that are multiples of g
    count = [0] * (MAX_VAL + 1)
    freq = [0] * (MAX_VAL + 1)
    for a in A:
        freq[a] += 1
    
    for g in range(1, MAX_VAL + 1):
        c = 0
        for multiple in range(g, MAX_VAL + 1, g):
            c += freq[multiple]
        count[g] = c
    
    # Step 2: For each g from MAX_VAL down to 1, if count[g] >= K,
    # then all indices i where A[i] is a multiple of g and ans[i] is not set,
    # set ans[i] = g.
    
    # To efficiently find indices i where A[i] is a multiple of g,
    # we can precompute for each g the list of indices.
    # But this might be memory intensive. Let's think differently.
    
    # Alternative: For each g with count[g] >= K, we need to find all i such that
    # A[i] is a multiple of g. We can iterate through all multiples of g and
    # for each multiple v, get all indices where A[i] == v.
    
    ans = [0] * N
    
    # Process g from large to small
    for g in range(MAX_VAL, 0, -1):
        if count[g] < K:
            continue
        
        # For each multiple of g, get indices where A[i] == multiple
        for multiple in range(g, MAX_VAL + 1, g):
            if freq[multiple] == 0:
                continue
            for idx in value_to_indices[multiple]:
                if ans[idx] == 0:
                    ans[idx] = g
    
    # Output results
    for a in ans:
        print(a)

solve()