from typing import List

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        # Map points to (perimeter_coord, side_index, x, y)
        # Sides: 0: Bottom (y=0), 1: Right (x=side), 2: Top (y=side), 3: Left (x=0)
        # Perimeter order: Bottom (0 to side), Right (0 to side), Top (side to 0), Left (side to 0)
        # Mapping:
        # Bottom: (x, 0) -> P = x
        # Right: (side, y) -> P = side + y
        # Top: (x, side) -> P = 2*side + (side - x)
        # Left: (0, y) -> P = 3*side + (side - y)
        
        mapped_points = []
        for x, y in points:
            if y == 0:
                p = x
                s_idx = 0
            elif x == side:
                p = side + y
                s_idx = 1
            elif y == side:
                p = 2 * side + (side - x)
                s_idx = 2
            else: # x == 0
                p = 3 * side + (side - y)
                s_idx = 3
            mapped_points.append((p, s_idx, x, y))
        
        # Sort by perimeter coordinate
        mapped_points.sort(key=lambda x: x[0])
        n = len(mapped_points)
        
        # Precompute side boundaries for the sorted list
        side_start_indices = [-1] * 4
        side_end_indices = [-1] * 4
        
        current_s = -1
        for i, (p, s, x, y) in enumerate(mapped_points):
            if s != current_s:
                current_s = s
                side_start_indices[s] = i
        
        for i in range(n - 1, -1, -1):
            p, s, x, y = mapped_points[i]
            if side_end_indices[s] == -1:
                side_end_indices[s] = i
        
        # Helper to calculate Manhattan distance
        def manhattan(p1, p2):
            return abs(p1[2] - p2[2]) + abs(p1[3] - p2[3])
        
        # Helper to find the first valid point index in [L, R] with distance >= d
        # Handles the V-shape distance function on the opposite side
        def find_first_valid_in_range(L, R, start_idx, d):
            curr = mapped_points[start_idx]
            target_coord = curr[2] # x coordinate
            
            # Find the point in [L, R] that minimizes the distance to start_idx
            # This is the point with x coordinate closest to target_coord
            
            side_in_range = mapped_points[L][1]
            min_dist_idx = -1
            min_dist = float('inf')
            
            # Candidates to check for minimum distance
            candidates = []
            
            # If the side is Right (1) or Left (3), x is constant.
            # If the side is Bottom (0) or Top (2), x varies.
            if side_in_range == 1 or side_in_range == 3:
                # x is constant, so all points have the same distance
                candidates.append(L)
                candidates.append(R)
            else:
                # x varies. Find the point with x closest to target_coord.
                # Side 0 (Bottom): x increases.
                # Side 2 (Top): x decreases.
                
                if side_in_range == 0:
                    # Increasing x. Find first index with x >= target_coord
                    lo, hi = L, R
                    best_idx = -1
                    while lo <= hi:
                        mid = (lo + hi) // 2
                        if mapped_points[mid][2] >= target_coord:
                            best_idx = mid
                            hi = mid - 1
                        else:
                            lo = mid + 1
                    
                    if best_idx != -1:
                        candidates.append(best_idx)
                    if best_idx - 1 >= L:
                        candidates.append(best_idx - 1)
                else: # Side 2 (Top)
                    # Decreasing x. Find first index with x <= target_coord
                    lo, hi = L, R
                    best_idx = -1
                    while lo <= hi:
                        mid = (lo + hi) // 2
                        if mapped_points[mid][2] <= target_coord:
                            best_idx = mid
                            lo = mid + 1
                        else:
                            hi = mid - 1
                    
                    if best_idx != -1:
                        candidates.append(best_idx)
                    if best_idx - 1 >= L:
                        candidates.append(best_idx - 1)
                
                # Also check endpoints to be safe
                candidates.append(L)
                candidates.append(R)
            
            # Find the index with minimum distance among candidates
            for idx in candidates:
                dist = manhattan(curr, mapped_points[idx])
                if dist < min_dist:
                    min_dist = dist
                    min_dist_idx = idx
            
            # If the minimum distance in the range is >= d, then all points are valid.
            # The first valid point is L.
            if min_dist >= d:
                return L
            
            # If min_dist < d, then there is a "gap" around min_dist_idx.
            # The valid points are a prefix [L, k] and a suffix [m, R].
            # We need to find the first valid point.
            # Check the prefix [L, min_dist_idx]: distance decreases as we approach min_dist_idx.
            # So if dist(L) >= d, then L is the first valid point.
            if manhattan(curr, mapped_points[L]) >= d:
                return L
            
            # Check the suffix [min_dist_idx, R]: distance increases as we move away from min_dist_idx.
            # We binary search for the first point with dist >= d.
            lo, hi = min_dist_idx, R
            ans = -1
            while lo <= hi:
                mid = (lo + hi) // 2
                if manhattan(curr, mapped_points[mid]) >= d:
                    ans = mid
                    hi = mid - 1
                else:
                    lo = mid + 1
            return ans if ans != -1 else -1
        
        # Helper to find the next valid point starting from start_idx
        def find_next_valid(start_idx, d):
            curr = mapped_points[start_idx]
            curr_s = curr[1]
            
            # We search in the range [start_idx + 1, start_idx + n - 1]
            # We iterate through the 4 sides in order (curr_s, next, next, next)
            sides_order = [curr_s, (curr_s + 1) % 4, (curr_s + 2) % 4, (curr_s + 3) % 4]
            
            best_j = -1
            
            for s in sides_order:
                L_side = side_start_indices[s]
                R_side = side_end_indices[s]
                
                # Determine the valid range [L, R] within [L_side, R_side] that is after start_idx
                # The search range is [start_idx + 1, start_idx + n - 1]
                L = max(L_side, start_idx + 1)
                R = min(R_side, start_idx + n - 1)
                
                if L <= R:
                    res = find_first_valid_in_range(L, R, start_idx, d)
                    if res != -1:
                        if best_j == -1 or res < best_j:
                            best_j = res
            
            return best_j
        
        # Check function: can we select k points with min distance >= d?
        def check(d):
            # Try each point as the first point
            for i in range(n):
                count = 1
                last_idx = i
                valid = True
                for _ in range(k - 1):
                    next_idx = find_next_valid(last_idx, d)
                    if next_idx == -1:
                        valid = False
                        break
                    last_idx = next_idx
                    count += 1
                if valid:
                    return True
            return False
        
        # Binary search for the answer
        low = 1
        high = 2 * side
        ans = 1
        
        while low <= high:
            mid = (low + high) // 2
            if check(mid):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        
        return ans