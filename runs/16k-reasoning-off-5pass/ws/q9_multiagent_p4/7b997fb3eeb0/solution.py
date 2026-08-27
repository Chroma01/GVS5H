import sys
import bisect

# Increase recursion depth just in case, though we use iterative find
sys.setrecursionlimit(300000)

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
        
        Q = int(next(iterator))
        queries = []
        for i in range(Q):
            l = int(next(iterator))
            r = int(next(iterator))
            queries.append((l, r, i))
            
    except StopIteration:
        return

    # Precompute best_match[i]: the smallest index j < i such that A[j] <= A[i] / 2.
    # Since A is sorted, we can use binary search.
    best_match = [-1] * N
    for i in range(N):
        target = A[i] // 2
        # We need the smallest index j < i such that A[j] <= target.
        # bisect_left returns the first index where A[idx] > target.
        # So the element at idx-1 is the largest element <= target.
        # If idx == 0, no element <= target exists in A[0:i].
        idx = bisect.bisect_left(A, target, 0, i)
        if idx < i:
            best_match[i] = idx
        else:
            best_match[i] = -1

    # Sort queries by their right endpoint R to process offline
    queries.sort(key=lambda x: x[1])
    
    # DSU array to maintain the set of available indices.
    # dsu[i] stores the next available index <= i.
    # Initially, every index is available, so dsu[i] = i.
    # If an index i is removed, dsu[i] will point to the next available index to its left.
    # We use -1 to indicate no available index exists (i.e., below index 0).
    dsu = list(range(N))
    
    # Iterative find with path compression
    def find(i):
        path = []
        curr = i
        while curr != -1 and dsu[curr] != curr:
            path.append(curr)
            curr = dsu[curr]
        # curr is now -1 or the root (an available index)
        for node in path:
            dsu[node] = curr
        return curr

    ans = [0] * Q
    
    # Process queries
    for l, r, q_idx in queries:
        # Convert to 0-based indexing
        l0, r0 = l - 1, r - 1
        curr = r0
        count = 0
        
        # Greedy simulation:
        # Start from the largest available index <= curr.
        # If it can be paired with a valid top (smallest available <= A[curr]/2), do it.
        # Otherwise, discard the largest available index.
        while curr >= l0:
            # Find the largest available index <= curr
            idx = find(curr)
            
            # If the largest available index is less than L, we can't form any more pairs
            if idx < l0:
                break
            
            # idx is the candidate for the base (bottom) of the kagamimochi
            p = best_match[idx]
            
            if p != -1:
                # Check if the candidate top 'p' is available and within the range [L, R]
                # p is always < idx, so we just need to check if p >= l0 and p is available.
                # p is available if find(p) == p.
                if p >= l0 and find(p) == p:
                    # Pair (p, idx)
                    count += 1
                    
                    # Remove idx from available set
                    if idx == 0:
                        dsu[0] = -1
                    else:
                        dsu[idx] = find(idx - 1)
                    
                    # Remove p from available set
                    if p == 0:
                        dsu[0] = -1
                    else:
                        dsu[p] = find(p - 1)
                    
                    # The next candidate base will be the largest available index < idx
                    # which is now stored in dsu[idx]
                    curr = dsu[idx]
                else:
                    # Cannot pair idx because p is either out of range or not available.
                    # Discard idx.
                    if idx == 0:
                        dsu[0] = -1
                    else:
                        dsu[idx] = find(idx - 1)
                    curr = dsu[idx]
            else:
                # No valid top exists for idx (all smaller elements are too large)
                # Discard idx.
                if idx == 0:
                    dsu[0] = -1
                else:
                    dsu[idx] = find(idx - 1)
                curr = dsu[idx]
        
        ans[q_idx] = count

    # Print answers in the original order
    for a in ans:
        print(a)

if __name__ == '__main__':
    solve()