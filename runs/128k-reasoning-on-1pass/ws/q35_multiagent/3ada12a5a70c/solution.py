from typing import List

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        def get_perimeter(p):
            x, y = p
            if y == 0:
                return x
            elif x == side:
                return side + y
            elif y == side:
                return 2 * side + (side - x)
            else:
                return 3 * side + (side - y)
                
        d = sorted([get_perimeter(p) for p in points])
        n = len(d)
        C = 4 * side
        d_ext = d + [x + C for x in d]
        
        def check(D):
            if D == 0: return True
            # Two pointers to find the next valid point for each index
            nxt = [0] * (2 * n)
            j = 0
            for i in range(2 * n):
                while j < 2 * n and d_ext[j] - d_ext[i] < D:
                    j += 1
                nxt[i] = j
                
            # Binary lifting (sparse table) to jump k-1 steps in O(log k)
            LOG = (k - 1).bit_length()
            up = [[0] * LOG for _ in range(2 * n)]
            for i in range(2 * n):
                up[i][0] = nxt[i]
                
            for p in range(1, LOG):
                for i in range(2 * n):
                    if up[i][p-1] < 2 * n:
                        up[i][p] = up[up[i][p-1]][p-1]
                    else:
                        up[i][p] = 2 * n
                        
            # Check if any starting point allows selecting k points with min distance D
            for i in range(n):
                curr = i
                for p in range(LOG):
                    if (k - 1) >> p & 1:
                        curr = up[curr][p]
                        if curr >= 2 * n:
                            break
                # Verify wrap-around gap
                if curr < 2 * n and C - (d_ext[curr] - d_ext[i]) >= D:
                    return True
            return False

        low, high = 0, C // k
        while low < high:
            mid = (low + high + 1) // 2
            if check(mid):
                low = mid
            else:
                high = mid - 1
        return low