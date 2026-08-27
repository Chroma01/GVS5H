import bisect

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        # Map each point to its perimeter coordinate
        perims = []
        for x, y in points:
            if y == 0:
                # Bottom edge: (0,0) to (side,0)
                p = x
            elif x == side:
                # Right edge: (side,0) to (side,side)
                p = side + y
            elif y == side:
                # Top edge: (side,side) to (0,side)
                p = 2 * side + (side - x)
            else:  # x == 0
                # Left edge: (0,side) to (0,0)
                p = 3 * side + (side - y)
            perims.append(p)
        
        perims.sort()
        n = len(perims)
        circumference = 4 * side
        
        # Binary search on the answer
        low, high = 0, 2 * side
        
        def check(d):
            if d == 0:
                return True
            # For each starting point, try to greedily pick k points
            for i in range(n):
                count = 1
                last = perims[i]
                current_index = i
                # We'll try to pick k-1 more points
                while count < k:
                    # The next point must be at least d away and at most circumference - d away
                    # in perimeter difference (which corresponds to Manhattan distance >= d)
                    low_val = last + d
                    high_val = last + circumference - d
                    
                    # Find the first index j > current_index such that perims[j] >= low_val
                    j = bisect.bisect_left(perims, low_val, current_index + 1)
                    
                    # Check if j is within bounds and perims[j] <= high_val
                    if j < n and perims[j] <= high_val:
                        count += 1
                        last = perims[j]
                        current_index = j
                    else:
                        break
                if count >= k:
                    return True
            return False
        
        ans = 0
        while low <= high:
            mid = (low + high) // 2
            if check(mid):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        
        return ans