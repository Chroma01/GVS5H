import sys

def solve():
    # Increase recursion depth just in case, though not needed here
    sys.setrecursionlimit(2000)
    
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    N = int(data[0])
    M = int(data[1])
    
    A = []
    for i in range(N):
        A.append(int(data[2 + i]))
        
    # Step 1: Compute initial inversion count for k=0 using Fenwick Tree
    # Values are in [0, M-1]. We can use a BIT of size M.
    
    class FenwickTree:
        def __init__(self, size):
            self.tree = [0] * (size + 1)
            
        def update(self, i, delta):
            while i < len(self.tree):
                self.tree[i] += delta
                i += i & (-i)
                
        def query(self, i):
            s = 0
            while i > 0:
                s += self.tree[i]
                i -= i & (-i)
            return s
            
    bit = FenwickTree(M)
    inv_count = 0
    
    # Process from left to right
    # For each element A[i], the number of elements already processed that are greater than A[i]
    # is: (total elements processed so far) - (elements <= A[i] processed so far)
    # Since we are 0-indexed in values, we map value v to index v+1 in BIT.
    
    for x in A:
        # Count elements greater than x already in BIT
        # Total elements so far is i (0-indexed loop variable, but let's track count)
        # Actually, let's just use a counter
        pass
        
    # Let's rewrite the loop properly
    inv_count = 0
    for i, x in enumerate(A):
        # Number of elements seen so far that are > x
        # Total seen so far = i
        # Number of elements <= x = bit.query(x + 1)
        count_le = bit.query(x + 1)
        count_gt = i - count_le
        inv_count += count_gt
        bit.update(x + 1, 1)
        
    # Step 2: Group indices by value
    # indices_by_val[v] = list of indices i where A[i] == v
    indices_by_val = [[] for _ in range(M)]
    for i, x in enumerate(A):
        indices_by_val[x].append(i)
        
    # Step 3: Iterate k from 0 to M-1
    # For each k, print inv_count
    # Then update inv_count for k+1
    
    results = []
    
    for k in range(M):
        results.append(str(inv_count))
        
        if k < M - 1:
            # The elements that wrap from M-1 to 0 in the current B array
            # are those with A[i] == M - 1 - k
            val = M - 1 - k
            W = indices_by_val[val]
            c = len(W)
            
            if c > 0:
                # Compute P_after: number of pairs (i, j) such that i < j, A[i] != val, A[j] == val
                # For each j in W, count number of non-wrapping elements before j.
                # Non-wrapping elements before j = j - (number of elements in W at indices <= j)
                # Since W is sorted, we can iterate through W and maintain a count of how many W elements we've seen.
                
                p_after = 0
                w_count_so_far = 0
                for idx in W:
                    # Number of wrapping elements at indices <= idx is w_count_so_far + 1 (including current)
                    # But we want number of wrapping elements at indices < idx? No, <= idx.
                    # Actually, the formula is:
                    # Non-wrapping before idx = idx - (number of wrapping elements at indices <= idx)
                    # Wait, if we are at idx, and it is a wrapping element, then the number of wrapping elements
                    # at indices <= idx is w_count_so_far + 1.
                    # So non-wrapping before idx = idx - (w_count_so_far + 1)
                    
                    non_wrapping_before = idx - (w_count_so_far + 1)
                    p_after += non_wrapping_before
                    w_count_so_far += 1
                
                # Delta = 2 * P_after - c * (N - c)
                delta = 2 * p_after - c * (N - c)
                inv_count += delta
                
    print('\n'.join(results))

solve()