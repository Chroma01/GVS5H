import sys

# Increase recursion depth just in case, though not strictly needed for this iterative solution
sys.setrecursionlimit(200005)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        T_str = next(iterator)
        T = int(T_str)
    except StopIteration:
        return

    results = []
    
    for _ in range(T):
        try:
            N_str = next(iterator)
            N = int(N_str)
            A = []
            for _ in range(N):
                A.append(int(next(iterator)))
        except StopIteration:
            break
            
        # Logic Implementation
        # The problem asks for the minimum operations to empty the array.
        # The optimal strategy is to delete values in the order of their first appearance.
        # For a value v to be deleted, all its instances must be moved to the front.
        # The cost to move all instances of v to the front (given that values appearing before v 
        # in the sorted order are already removed) is equal to the number of instances of 
        # "future" values (values appearing after v in the sorted order) that are located 
        # before the last occurrence of v in the original array.
        # Total Operations = Sum of Swaps + Number of Distinct Values.
        
        # Step 1: Identify distinct values and their first appearance indices.
        first_occurrence = {}
        for idx, val in enumerate(A):
            if val not in first_occurrence:
                first_occurrence[val] = idx
        
        # Step 2: Sort distinct values by first appearance.
        distinct_values = sorted(first_occurrence.keys(), key=lambda x: first_occurrence[x])
        num_distinct = len(distinct_values)
        
        # Step 3: Precompute last occurrence for each value.
        last_occurrence = {}
        for idx, val in enumerate(A):
            last_occurrence[val] = idx
            
        # Step 4: Efficiently count swaps using a Fenwick Tree (BIT).
        # We need to count, for each v in distinct_values, the number of elements u 
        # such that u appears after v in the sorted list AND u appears before last(v) in A.
        # We initialize a BIT with 1s at all positions (representing all elements).
        # As we iterate through distinct_values, we query the BIT for the sum in range [0, last(v)].
        # This sum gives the count of elements that are neither v nor any previously processed value.
        # After the query, we update the BIT by setting all positions of v to 0 (removing them).
        
        # BIT Implementation
        bit = [0] * (N + 1)
        
        # Initialize BIT with 1s in O(N)
        # For a BIT where all elements are 1, bit[i] = i & (-i)
        for i in range(1, N + 1):
            bit[i] = i & (-i)
            
        def update(idx, val):
            # idx is 0-based, convert to 1-based
            i = idx + 1
            while i <= N:
                bit[i] += val
                i += i & (-i)
                
        def query(idx):
            # idx is 0-based
            i = idx + 1
            s = 0
            while i > 0:
                s += bit[i]
                i -= i & (-i)
            return s
            
        # Group indices by value to efficiently update the BIT
        positions = {}
        for idx, val in enumerate(A):
            if val not in positions:
                positions[val] = []
            positions[val].append(idx)
            
        total_swaps = 0
        
        for v in distinct_values:
            last_idx = last_occurrence[v]
            # Count future values in 0..last_idx
            count_future = query(last_idx)
            total_swaps += count_future
            
            # Remove current value from BIT
            for pos in positions[v]:
                update(pos, -1)
                
        results.append(str(total_swaps + num_distinct))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()