import sys
import bisect

def solve():
    # Increase recursion depth just in case
    sys.setrecursionlimit(2000)
    
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    iterator = iter(data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    intervals = []
    for i in range(M):
        L = int(next(iterator))
        R = int(next(iterator))
        intervals.append((L, R, i))

    # Sort intervals by L, then by R descending
    sorted_intervals = sorted(intervals, key=lambda x: (x[0], -x[1]))
    
    # Precompute max_r_up_to[i] = max(R of sorted_intervals[0..i])
    max_r_up_to = [0] * M
    current_max = -1
    for i in range(M):
        if sorted_intervals[i][1] > current_max:
            current_max = sorted_intervals[i][1]
        max_r_up_to[i] = current_max
        
    L_values = [x[0] for x in sorted_intervals]
    
    def get_max_r_for_L_le(target):
        idx = bisect.bisect_right(L_values, target) - 1
        if idx < 0:
            return -1
        return max_r_up_to[idx]
        
    def min_cover_with_reconstruction(start, end, exclude_set):
        if start > end:
            return 0, []
        
        count = 0
        current_end = start - 1
        used_indices = []
        
        while current_end < end:
            target = current_end + 1
            idx_end = bisect.bisect_right(L_values, target) - 1
            if idx_end < 0:
                return -1, []
            
            # Find the best non-excluded interval in sorted_intervals[0..idx_end]
            best_r = -1
            best_interval = None
            
            # We scan from idx_end downwards to find the max R among non-excluded
            # To optimize, we can check max_r_up_to[idx_end] first.
            # If the interval providing max_r_up_to[idx_end] is excluded, we need to find the next best.
            
            # Simple scan is O(M) in worst case, leading to O(M^2) overall.
            # Given M=200,000, we need to be careful.
            # However, the number of steps in the greedy loop is usually small.
            # The scan depth is bounded by the number of excluded intervals + 1 in practice.
            
            for i in range(idx_end, -1, -1):
                if sorted_intervals[i][2] not in exclude_set:
                    if sorted_intervals[i][1] > best_r:
                        best_r = sorted_intervals[i][1]
                        best_interval = sorted_intervals[i]
                    # Since sorted by L then -R, the first one we find with max R is good?
                    # No, we need to check all to find max R.
                    # But we can break if we find one that covers the rest? No.
            
            if best_r <= current_end:
                return -1, []
            
            count += 1
            current_end = best_interval[1]
            used_indices.append(best_interval[2])
            
        return count, used_indices

    # Check Case 1: Cover [1, N] with all intervals (I_2 empty)
    cost1, indices1 = min_cover_with_reconstruction(1, N, set())
    
    # Check Case 2: Empty intersection pair (I_2 size 2, I_1 empty)
    # Check if any two intervals have empty intersection
    sorted_by_L = sorted(intervals, key=lambda x: x[0])
    min_R_so_far = sorted_by_L[0][1]
    has_empty_pair = False
    empty_pair_indices = None
    
    for i in range(1, M):
        if min_R_so_far < sorted_by_L[i][0]:
            has_empty_pair = True
            # Find the specific pair
            # sorted_by_L[i-1] has R = min_R_so_far (or less), and sorted_by_L[i] has L > min_R_so_far
            # We need to find the actual indices
            # Let's just find any pair
            for j in range(M):
                for k in range(j+1, M):
                    if intervals[j][1] < intervals[k][0] or intervals[k][1] < intervals[j][0]:
                        empty_pair_indices = (j, k)
                        break
                else:
                    continue
                break
            break
        if sorted_by_L[i][1] < min_R_so_far:
            min_R_so_far = sorted_by_L[i][1]
            
    cost2 = 2 if has_empty_pair else float('inf')
    
    # Check Case 3: For each k, cover [L_k, R_k] with others (I_2 size 1)
    cost3 = float('inf')
    indices3 = []
    excluded_k3 = -1
    
    # Optimization: If cost1 is 1 or 2, we might not need to check Case 3 extensively.
    # But let's check all k for correctness.
    
    for k in range(M):
        exclude = {k}
        L_k, R_k, _ = intervals[k]
        c, idxs = min_cover_with_reconstruction(L_k, R_k, exclude)
        if c != -1:
            total_cost = 1 + c
            if total_cost < cost3:
                cost3 = total_cost
                indices3 = idxs
                excluded_k3 = k
                
    # Determine the best solution
    best_cost = cost1
    best_indices = indices1
    best_type = 1 # 1 for I_1 cover, 2 for I_2 empty intersection, 3 for I_2 size 1
    best_excluded = -1
    
    if cost2 < best_cost:
        best_cost = cost2
        best_indices = empty_pair_indices
        best_type = 2
        best_excluded = -1
        
    if cost3 < best_cost:
        best_cost = cost3
        best_indices = indices3
        best_type = 3
        best_excluded = excluded_k3
        
    if best_cost == float('inf'):
        print(-1)
    else:
        ops = [0] * M
        if best_type == 1:
            # I_1 = best_indices, I_2 = empty
            for idx in best_indices:
                ops[idx] = 1
        elif best_type == 2:
            # I_2 = best_indices, I_1 = empty
            for idx in best_indices:
                ops[idx] = 2
        elif best_type == 3:
            # I_2 = {best_excluded}, I_1 = best_indices
            ops[best_excluded] = 2
            for idx in best_indices:
                ops[idx] = 1
                
        print(best_cost)
        print(" ".join(map(str, ops)))

solve()