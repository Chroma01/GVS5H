import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

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
    except StopIteration:
        return

    # Group positions by value
    # positions[v] will store a list of indices (0-based) where value v appears
    positions = {}
    for idx, val in enumerate(A):
        if val not in positions:
            positions[val] = []
        positions[val].append(idx)

    # Helper function to calculate number of subarrays that do NOT contain any element from a given list of positions
    # The list of positions must be sorted (which they are by construction)
    def count_subarrays_without_any(pos_list):
        if not pos_list:
            # If the value never appears, all subarrays don't contain it
            return N * (N + 1) // 2
        
        total_subarrays = N * (N + 1) // 2
        count_without = 0
        
        # Gap before the first occurrence
        first = pos_list[0]
        count_without += (first + 1) * first // 2
        
        # Gaps between consecutive occurrences
        for i in range(1, len(pos_list)):
            prev = pos_list[i-1]
            curr = pos_list[i]
            gap_len = curr - prev - 1
            if gap_len > 0:
                count_without += gap_len * (gap_len + 1) // 2
        
        # Gap after the last occurrence
        last = pos_list[-1]
        count_without += (N - last) * (N - last + 1) // 2
        
        return count_without

    # 1. Calculate Sum of Unique Elements
    # Sum_{L,R} |Unique(L,R)| = Sum_{v} (Total Subarrays - Subarrays without v)
    sum_unique = 0
    total_subarrays = N * (N + 1) // 2
    
    for v in positions:
        pos_list = positions[v]
        subarrays_without = count_subarrays_without_any(pos_list)
        subarrays_with = total_subarrays - subarrays_without
        sum_unique += subarrays_with

    # 2. Calculate Sum of Pairs (x, x+1)
    # Sum_{L,R} |Pairs(L,R)| = Sum_{x=1}^{N-1} (Subarrays containing both x and x+1)
    # Count(x, x+1) = Total - (No x) - (No x+1) + (No x and No x+1)
    # (No x and No x+1) is calculated by merging pos_list(x) and pos_list(x+1) and finding gaps in the union
    
    sum_pairs = 0
    
    # We iterate x from 1 to N-1. Note that values in A are 1-based (1 <= A_i <= N).
    # So we check pairs (1,2), (2,3), ..., (N-1, N).
    for x in range(1, N):
        pos_x = positions.get(x, [])
        pos_x1 = positions.get(x+1, [])
        
        # Calculate (No x)
        no_x = count_subarrays_without_any(pos_x)
        
        # Calculate (No x+1)
        no_x1 = count_subarrays_without_any(pos_x1)
        
        # Calculate (No x and No x+1) -> Union of positions
        # Merge two sorted lists
        union_pos = []
        i, j = 0, 0
        len_x = len(pos_x)
        len_x1 = len(pos_x1)
        
        while i < len_x and j < len_x1:
            if pos_x[i] < pos_x1[j]:
                union_pos.append(pos_x[i])
                i += 1
            else:
                union_pos.append(pos_x1[j])
                j += 1
        while i < len_x:
            union_pos.append(pos_x[i])
            i += 1
        while j < len_x1:
            union_pos.append(pos_x1[j])
            j += 1
            
        no_both = count_subarrays_without_any(union_pos)
        
        count_both = total_subarrays - no_x - no_x1 + no_both
        sum_pairs += count_both

    # Result
    ans = sum_unique - sum_pairs
    print(ans)

if __name__ == '__main__':
    solve()