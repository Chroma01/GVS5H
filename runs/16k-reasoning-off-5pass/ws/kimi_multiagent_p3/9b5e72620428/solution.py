import sys
from collections import Counter
import numpy as np

def main():
    input = sys.stdin.readline
    N_line = input()
    if not N_line:
        return
    N = int(N_line)
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))

    fixed_A = [x for x in A if x != -1]
    fixed_B = [x for x in B if x != -1]
    
    k = len(fixed_A)
    m = len(fixed_B)
    
    T = k + m - N
    
    if T <= 0:
        print("Yes")
        return
        
    max_fixed = 0
    if k > 0:
        max_fixed = max(max_fixed, max(fixed_A))
    if m > 0:
        max_fixed = max(max_fixed, max(fixed_B))
        
    cnt_A = Counter(fixed_A)
    cnt_B = Counter(fixed_B)
    
    items_A = list(cnt_A.items())
    items_B = list(cnt_B.items())
    
    vals_A = np.array([x[0] for x in items_A], dtype=np.int64)
    counts_A = np.array([x[1] for x in items_A], dtype=np.int64)
    
    vals_B = np.array([x[0] for x in items_B], dtype=np.int64)
    counts_B = np.array([x[1] for x in items_B], dtype=np.int64)
    
    sums = vals_A[:, None] + vals_B[None, :]
    weights = np.minimum(counts_A[:, None], counts_B[None, :])
    
    flat_sums = sums.ravel()
    flat_weights = weights.ravel()
    
    sort_idx = np.argsort(flat_sums)
    sorted_sums = flat_sums[sort_idx]
    sorted_weights = flat_weights[sort_idx]
    
    possible = False
    n_sums = len(sorted_sums)
    i = 0
    while i < n_sums:
        j = i
        current_match = 0
        s = sorted_sums[i]
        while j < n_sums and sorted_sums[j] == s:
            current_match += sorted_weights[j]
            j += 1
        if s >= max_fixed and current_match >= T:
            possible = True
            break
        i = j
        
    print("Yes" if possible else "No")

if __name__ == "__main__":
    main()