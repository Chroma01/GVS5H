import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    try:
        T = int(next(iterator))
    except StopIteration:
        return

    results = []
    
    for _ in range(T):
        try:
            N = int(next(iterator))
            A = []
            for _ in range(N):
                A.append(int(next(iterator)))
        except StopIteration:
            break
            
        # Count runs in the original array
        runs = 1
        for i in range(1, N):
            if A[i] != A[i-1]:
                runs += 1
        
        # Count frequencies
        from collections import Counter
        counts = Counter(A)
        distinct = len(counts)
        
        # Calculate inversions to sort the array
        # We only care about inversions between different values.
        # Specifically, to group all identical values together, we want to sort the array.
        # The cost is the number of swaps (inversions) + number of runs in sorted array (which is distinct).
        
        # To count inversions efficiently:
        # We can use a Fenwick tree or merge sort.
        # Since values are up to N, we can use a Fenwick tree.
        
        # Coordinate compression is not needed as values are 1..N.
        
        # However, N is up to 2*10^5, so O(N log N) is required.
        
        # Let's implement a Fenwick tree for inversion counting.
        
        bit = [0] * (N + 1)
        
        def update(i, delta):
            while i <= N:
                bit[i] += delta
                i += i & (-i)
                
        def query(i):
            s = 0
            while i > 0:
                s += bit[i]
                i -= i & (-i)
            return s
            
        inversions = 0
        # Process from right to left to count smaller elements to the right
        # Or left to right to count larger elements to the left.
        # Let's count pairs (i, j) with i < j and A[i] > A[j].
        
        # Clear bit
        bit = [0] * (N + 1)
        
        for x in A:
            # Count elements greater than x that have appeared so far?
            # No, we want to count elements to the right that are smaller.
            # Let's do it left to right: for each x, count how many elements to the left are greater than x.
            # Total elements to left = i.
            # Elements <= x to left = query(x).
            # Elements > x to left = i - query(x).
            # But we want inversions, which are pairs (i, j) with i < j and A[i] > A[j].
            # So for current element A[j]=x, we want to count i < j such that A[i] > x.
            # This is exactly j - query(x) if we have processed j elements? No, we are at j-th element (0-indexed).
            # Let's use 1-based indexing for BIT.
            
            # Number of elements seen so far
            seen = query(N) # This is just the loop index + 1 if we update after query
            
            # Actually, let's just use the standard method:
            # For each element, count how many elements to its right are smaller.
            # This is equivalent to counting pairs (i, j) with i < j and A[i] > A[j].
            
            # Let's do it by processing from right to left.
            # For each x, count how many elements to the right are smaller than x.
            # This is query(x-1).
            pass

        # Let's restart the inversion count logic cleanly
        bit = [0] * (N + 1)
        inversions = 0
        
        # Process from right to left
        for i in range(N - 1, -1, -1):
            x = A[i]
            # Count elements to the right that are smaller than x
            # These are elements already in the BIT that are < x
            smaller = query(x - 1)
            inversions += smaller
            update(x, 1)
            
        ans = inversions + distinct
        results.append(str(ans))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()