import sys
from bisect import bisect_right

def solve():
    # Read all input at once
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
        B = [int(next(iterator)) for _ in range(N)]
        K = int(next(iterator))
        queries = []
        for _ in range(K):
            X = int(next(iterator))
            Y = int(next(iterator))
            queries.append((X, Y))
    except StopIteration:
        return

    # Precompute prefix sums for the original arrays? 
    # No, we need to handle subsets.
    # However, we can optimize by noting that for each query, we only need A[:X] and B[:Y].
    # We will sort these subarrays for each query.
    
    # To speed up, we can pre-slice? No, slicing creates copies.
    # But we can avoid re-sorting if we cache? No, X and Y vary.
    
    # Let's implement the O(X log X + Y log Y) per query solution.
    # For each query (X, Y):
    # 1. Take A_sub = A[:X], B_sub = B[:Y]
    # 2. Sort A_sub and B_sub
    # 3. Compute prefix sums for sorted B_sub
    # 4. Iterate through sorted A_sub, using binary search or two pointers on B_sub
    
    # Optimization: Use two pointers for the linear scan part.
    
    results = []
    
    for X, Y in queries:
        # Extract subarrays
        A_sub = A[:X]
        B_sub = B[:Y]
        
        # Sort them
        A_sub.sort()
        B_sub.sort()
        
        # Precompute prefix sums for B_sub
        # PB[i] = sum(B_sub[0]...B_sub[i-1])
        PB = [0] * (Y + 1)
        current_sum = 0
        for i in range(Y):
            current_sum += B_sub[i]
            PB[i+1] = current_sum
            
        total_sum = 0
        sum_B = PB[Y]
        
        # Two pointers / Binary Search approach
        # For each a in A_sub, find how many b in B_sub are <= a
        # Since A_sub is sorted, the split point in B_sub moves to the right.
        
        j = 0
        # We can iterate and maintain j
        for a in A_sub:
            # Move j forward while B_sub[j] <= a
            while j < Y and B_sub[j] <= a:
                j += 1
            
            # Now B_sub[0...j-1] are <= a
            # Count of elements <= a is j
            # Sum of elements <= a is PB[j]
            
            count_le = j
            sum_le = PB[j]
            
            # Contribution from elements <= a:
            # sum(a - b for b in B_sub[:j]) = j * a - sum_le
            part1 = count_le * a - sum_le
            
            # Contribution from elements > a:
            # sum(b - a for b in B_sub[j:]) = (sum_B - sum_le) - (Y - count_le) * a
            part2 = (sum_B - sum_le) - (Y - count_le) * a
            
            total_sum += part1 + part2
            
        results.append(str(total_sum))
        
    sys.stdout.write('\n'.join(results) + '\n')

if __name__ == '__main__':
    solve()