from typing import List

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        # Sort points along the perimeter of the square.
        # Order: Bottom (y=0, x: 0->side), Right (x=side, y: 0->side), 
        #        Top (y=side, x: side->0), Left (x=0, y: side->0)
        def get_perimeter_index(x, y):
            if y == 0:
                return x
            elif x == side:
                return side + y
            elif y == side:
                return 2 * side + (side - x)
            elif x == 0:
                return 3 * side + (side - y)
            return -1 # Should not happen based on constraints
        
        sorted_points = sorted(points, key=lambda p: get_perimeter_index(p[0], p[1]))
        n = len(sorted_points)
        
        # Helper to calculate Manhattan distance
        def manhattan(p1, p2):
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
        
        # Binary search for the maximum minimum distance
        low = 0
        high = 2 * side # Max possible distance
        ans = 0
        
        while low <= high:
            mid = (low + high) // 2
            if mid == 0:
                low = 1
                continue
                
            # Check if it's possible to select k points with min distance >= mid
            # This is equivalent to finding Maximum Independent Set on an interval graph
            # where intervals are [L_i, R_i] such that dist(i, j) < mid
            
            def check(D):
                if D == 0: return True
                intervals = []
                
                # We need to find for each point i, the range [L_i, R_i] of indices 
                # (in the sorted perimeter list) such that dist(i, j) < D.
                # Since the points are on a circle (perimeter), this range is contiguous.
                # We handle the circularity by considering indices modulo n.
                
                # To efficiently find L_i and R_i, we can use two pointers.
                # However, since the "conflict" region moves monotonically as we iterate i,
                # we can maintain pointers. But given N=15000, a simple O(N) scan per point 
                # with early breaking or optimized two-pointers is needed.
                # A robust O(N) approach for circular intervals:
                
                # Let's compute intervals. For each i, we want the smallest L and largest R
                # such that for all j in [L, R], dist(i, j) < D.
                # Note: The condition dist(i, j) < D defines a contiguous arc.
                
                # We will compute L_i and R_i for each i.
                # To handle the circular nature easily, we can duplicate the points array 
                # virtually or just use modulo arithmetic.
                
                # Optimization: The conflict interval for i is roughly centered around i.
                # As i increases, the interval [L_i, R_i] shifts to the right.
                
                # Let's find R_i first (rightmost index with dist < D).
                # And L_i (leftmost index with dist < D).
                
                # We can use two pointers for R and L.
                # Initialize R and L.
                
                R = 0
                L = 0
                
                # We iterate i from 0 to n-1.
                # We need to find the range [L, R] in the circular array.
                # Let's map indices to 0..2n-1 to avoid modulo confusion during search,
                # then map back.
                
                # Actually, simpler logic:
                # For a fixed i, the set of j with dist(i, j) < D is an arc.
                # Let's find the arc boundaries.
                
                # We can pre-calculate the "next" and "prev" points that satisfy the condition?
                # No, just two pointers is fine.
                
                # Reset pointers for each check? No, we can maintain them.
                # But since the condition is dist(i, j) < D, and i moves, the window moves.
                
                # Let's implement a clean O(N) two-pointer approach.
                # We want to find for each i:
                #   R[i]: the largest index (in 0..2n-1 range) such that dist(i, R[i]) < D.
                #   L[i]: the smallest index (in 0..2n-1 range) such that dist(i, L[i]) < D.
                # The actual interval in 0..n-1 is [L[i] % n, R[i] % n] but we must be careful with wrap-around.
                # Actually, if the interval wraps around, it will be represented as [start, n-1] U [0, end].
                # But for the greedy MIS on circular interval graph, we can break the circle at an arbitrary point
                # and duplicate the array.
                
                # Let's duplicate the points array to handle wrap-around.
                # points_2n = sorted_points + sorted_points
                # Now we have 2n points. We only care about selecting k points from the original n.
                # But the greedy algorithm on the duplicated array might select points from the second half.
                # We need to ensure we select distinct points from the original set.
                
                # Alternative: Just compute the interval [L, R] for each i in the circular sense.
                # If the interval does not wrap, it's [L, R]. If it wraps, it's [L, n-1] and [0, R].
                # But the standard greedy for circular interval graph is slightly more complex.
                # However, since k is small and N is up to 15000, maybe O(N log N) is acceptable.
                # Let's stick to the interval graph logic.
                
                # To simplify:
                # 1. Compute for each i, the interval of indices j (0 <= j < n) such that dist(i, j) < D.
                #    This interval is always contiguous on the circle.
                # 2. Convert this to a linear interval graph problem by breaking the circle.
                #    We can try breaking the circle at every point? No, that's O(N^2).
                #    Standard trick: Duplicate the array to 2n. Solve for MIS on 2n intervals.
                #    But we must ensure we don't pick the same point twice (i and i+n).
                #    Actually, if we select k points from 2n such that no two are within distance < D,
                #    and we enforce that we pick at most one from {i, i+n}, it works.
                #    But simpler: Just use the property that the conflict graph is an interval graph.
                #    We can solve MIS on circular interval graph by trying to break the circle at the point
                #    that is NOT selected? No.
                
                # Let's use the property that we only need to find IF there exists a subset of size k.
                # We can use the greedy strategy on the linearized array (0 to 2n-1) but with a constraint.
                # Actually, the simplest correct approach for "Max Independent Set on Circular Interval Graph"
                # is to try breaking the circle at each of the N points? No, that's O(N^2).
                # But wait, we can just break the circle at an arbitrary point, say index 0.
                # If the optimal solution does not include index 0, then the linear solution on 0..n-1 works.
                # If it does include index 0, then we might have issues with wrap-around.
                # However, we can try two cases:
                # Case 1: Do not select index 0. Solve on 1..n-1 (linear).
                # Case 2: Select index 0. Then we cannot select any point in its conflict interval.
                #         Then solve for the remaining k-1 points in the remaining valid range (linear).
                
                # This reduces the problem to two linear MIS problems.
                
                # Let's implement this.
                
                # Helper to get conflict interval for i in linear array [0, 2n-1]
                # But we only need to consider points in [0, n-1].
                
                # Let's refine the "break circle" strategy.
                # We want to select k points from 0..n-1.
                # Conflict(i, j) iff dist(i, j) < D.
                # This is symmetric.
                
                # Strategy:
                # 1. Try to solve assuming index 0 is NOT selected.
                #    We consider points 1..n-1. The conflict intervals are computed within this range.
                #    But conflicts can wrap around (e.g., n-1 conflicts with 1).
                #    If we exclude 0, the circle is broken at 0. The remaining points form a line 1..n-1.
                #    The conflict intervals for points in 1..n-1 will be contiguous segments within 1..n-1
                #    UNLESS the conflict interval wraps around 0. But since 0 is excluded, we just ignore 0.
                #    So for each i in 1..n-1, the conflict set is {j in 1..n-1 | dist(i, j) < D}.
                #    This is a contiguous segment in 1..n-1.
                #    So we can run linear greedy MIS on 1..n-1.
                
                # 2. Try to solve assuming index 0 IS selected.
                #    If we select 0, we cannot select any j such that dist(0, j) < D.
                #    Let the conflict interval of 0 be [L0, R0] (wrapping allowed).
                #    We remove all j in [L0, R0] from consideration.
                #    The remaining points form a linear segment (or two segments if 0 was in the middle? No, 0 is a point).
                #    Actually, removing a contiguous arc from a circle leaves a linear segment.
                #    So we get a linear range of points. We need to select k-1 points from this range.
                #    Run linear greedy MIS.
                
                # This covers all cases because any valid set either contains 0 or it doesn't.
                
                def solve_linear(points_subset, k_needed, D):
                    # points_subset is a list of indices from the original sorted_points
                    # We assume these indices form a linear chain where neighbors are adjacent in the subset?
                    # No, we just need to map them to a linear order.
                    # Since we are breaking the circle, the indices in points_subset are already sorted.
                    # We just need to compute conflict intervals within this subset.
                    
                    # Let's map indices to 0..m-1
                    m = len(points_subset)
                    if m == 0: return k_needed <= 0
                    
                    # We need to find for each i in 0..m-1, the interval [L, R] in 0..m-1
                    # such that for all j in [L, R], dist(points_subset[i], points_subset[j]) < D.
                    # Since the original points are on a circle, and we broke it, the conflict intervals
                    # might wrap around the "break" point?
                    # No, we constructed points_subset such that the break point (index 0 or the removed arc) is excluded.
                    # So the conflict intervals should be contiguous within points_subset.
                    
                    # Let's verify:
                    # Case 1: points_subset = 1..n-1. The break is at 0.
                    #    Conflict between n-1 and 1? dist(n-1, 1) might be < D.
                    #    If so, the interval for n-1 would include 1.
                    #    But 1 is the start of the subset. So the interval is [1, n-1].
                    #    This is contiguous in the subset.
                    # Case 2: points_subset = remaining after removing [L0, R0].
                    #    This is a single contiguous segment of indices.
                    #    So yes, we can treat it as a linear problem.
                    
                    # Implementation:
                    # Sort points_subset by their original index (already sorted).
                    # For each i, find L and R in the subset such that dist < D.
                    # Use two pointers.
                    
                    subset_indices = points_subset
                    m = len(subset_indices)
                    intervals = []
                    
                    # Two pointers for L and R
                    # We need to search in the subset_indices.
                    # Since dist is not monotonic with respect to index in the subset (because of geometry),
                    # we cannot simply assume monotonicity.
                    # HOWEVER, on the perimeter, the distance function dist(i, j) is convex-like (decreases then increases).
                    # So the set {j | dist(i, j) < D} is indeed a contiguous interval on the perimeter.
                    # Since our subset_indices is a contiguous segment of the perimeter, the intersection
                    # is also a contiguous segment.
                    
                    # So we can use two pointers.
                    
                    # We need to handle the "wrap" within the subset?
                    # No, because we broke the circle. The subset is a linear segment of the perimeter.
                    # So for any i, the conflict interval is a sub-segment of subset_indices.
                    
                    # Let's find L and R for each i.
                    # L[i]: first index in subset_indices such that dist(i, L[i]) < D.
                    # R[i]: last index in subset_indices such that dist(i, R[i]) < D.
                    
                    # We can compute these using two pointers.
                    # Initialize L=0, R=0.
                    # For each i:
                    #   While L <= i and dist(i, subset_indices[L]) >= D: L += 1
                    #   While R < m and dist(i, subset_indices[R]) < D: R += 1
                    #   Interval is [L, R-1].
                    
                    # Wait, the condition "dist(i, j) < D" is symmetric.
                    # As i increases, L and R should generally increase.
                    
                    L_ptr = 0
                    R_ptr = 0
                    
                    for i in range(m):
                        xi, yi = sorted_points[subset_indices[i]]
                        
                        # Adjust L_ptr
                        while L_ptr <= i:
                            xj, yj = sorted_points[subset_indices[L_ptr]]
                            if abs(xi - xj) + abs(yi - yj) >= D:
                                L_ptr += 1
                            else:
                                break
                        if L_ptr > i:
                            # This means no point in subset_indices[0..i] conflicts with i?
                            # But i itself conflicts with i (dist=0 < D).
                            # So L_ptr should be at most i.
                            # The loop above stops when dist < D.
                            # If dist(i, i) >= D, then D <= 0, which is handled.
                            # So L_ptr will be <= i.
                            pass
                        
                        # Adjust R_ptr
                        # We need to find the largest R such that dist(i, R) < D.
                        # We can start from the previous R_ptr?
                        # Since i increases, the conflict interval shifts right.
                        # But we must ensure R_ptr >= L_ptr.
                        if R_ptr < L_ptr:
                            R_ptr = L_ptr
                        
                        while R_ptr < m:
                            xj, yj = sorted_points[subset_indices[R_ptr]]
                            if abs(xi - xj) + abs(yi - yj) < D:
                                R_ptr += 1
                            else:
                                break
                        # R_ptr is now one past the last valid index.
                        # Interval is [L_ptr, R_ptr - 1]
                        intervals.append((L_ptr, R_ptr - 1))
                    
                    # Now run greedy MIS on these intervals
                    # Sort by right endpoint
                    intervals.sort(key=lambda x: x[1])
                    
                    count = 0
                    last_end = -1
                    
                    for l, r in intervals:
                        if l > last_end:
                            count += 1
                            last_end = r
                            if count >= k_needed:
                                return True
                    return False
                
                # Case 1: Do not select index 0.
                # Points: 1 to n-1.
                # If n < 2, this case is invalid (but k >= 4, so n >= 4).
                if n >= 2:
                    if solve_linear(list(range(1, n)), k, D):
                        return True
                
                # Case 2: Select index 0.
                # Find conflict interval of 0.
                # We need to find the range [L0, R0] in the circular array such that dist(0, j) < D.
                # Then remove these points and solve for k-1 in the remaining linear segment.
                
                # Find L0 and R0 for index 0.
                # We search in 0..2n-1.
                L0 = 0
                R0 = 0
                
                # Find L0: first index with dist(0, L0) >= D
                # Actually we want the range of indices with dist < D.
                # Let's find the first index with dist >= D going forward (L0_start)
                # and the last index with dist < D going forward (R0_end).
                
                # Search forward from 0
                curr = 0
                while curr < 2 * n:
                    idx = curr % n
                    xj, yj = sorted_points[idx]
                    if abs(sorted_points[0][0] - xj) + abs(sorted_points[0][1] - yj) < D:
                        curr += 1
                    else:
                        break
                R0_end = curr - 1 # Last index with dist < D
                
                # Search backward from 0 (or forward from n)
                # We want the first index (going backward) with dist >= D.
                # Let's search forward from n-1 (which is -1 mod n)
                curr = n - 1
                while curr >= 0:
                    xj, yj = sorted_points[curr]
                    if abs(sorted_points[0][0] - xj) + abs(sorted_points[0][1] - yj) < D:
                        curr -= 1
                    else:
                        break
                L0_start = curr + 1 # First index (going backward) with dist >= D
                
                # The conflict interval is [L0_start, R0_end] (circular).
                # If L0_start <= R0_end, the interval is [L0_start, R0_end].
                # If L0_start > R0_end, the interval wraps: [L0_start, n-1] U [0, R0_end].
                
                # We need to remove these points and solve for k-1 in the remaining.
                # The remaining points form a linear segment.
                # If the interval is [L0_start, R0_end] (no wrap), remaining is [0, L0_start-1] and [R0_end+1, n-1].
                #    This is two segments. We can try both.
                # If the interval wraps, remaining is [R0_end+1, L0_start-1] (a single segment).
                
                # Let's collect the remaining segments.
                segments = []
                if L0_start <= R0_end:
                    # No wrap
                    if L0_start > 0:
                        segments.append(list(range(0, L0_start)))
                    if R0_end < n - 1:
                        segments.append(list(range(R0_end + 1, n)))
                else:
                    # Wrap
                    # Remaining is [R0_end + 1, L0_start - 1]
                    if R0_end + 1 <= L0_start - 1:
                        segments.append(list(range(R0_end + 1, L0_start)))
                
                # Try each segment
                for seg in segments:
                    if solve_linear(seg, k - 1, D):
                        return True
                
                return False

            if check(mid):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        
        return ans