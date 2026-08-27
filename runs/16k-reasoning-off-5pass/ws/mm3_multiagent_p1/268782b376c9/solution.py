from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        
        def min_moves(need):
            # Suffix max to get non-increasing f
            f = [0] * n
            cur = 0
            for i in range(n - 1, -1, -1):
                if need[i] > cur:
                    cur = need[i]
                f[i] = cur
            if f[0] == 0:
                return 0
            
            # Try the walk ending at cell e. Use recurrence:
            # c_0 = 2*f[0] - 1 - [e==0]
            # c_i = 2*f[i] - c_{i-1} - [e==i]  for 0 < i < n-1
            # Boundary at n-1: f[n-1] = a_{n-2} + [e==n-1]
            #   where a_{n-2} = (c_{n-2} + d_{n-2}) / 2
            #   and d_{n-2} = 1 - [e <= n-2]
            # Cost = 1 + sum(c_i for i in 0..n-2)
            
            # Only try e at positions where f changes or e=0 or e=n-1
            candidates = {0, n-1}
            for i in range(n-1):
                if f[i] > f[i+1]:
                    candidates.add(i+1)
            
            best = None
            for e in candidates:
                c0 = 2*f[0] - 1 - (1 if e == 0 else 0)
                if c0 < 0:
                    continue
                c = [c0]
                ok = True
                for i in range(1, n-1):
                    ci = 2*f[i] - c[-1] - (1 if e == i else 0)
                    if ci < 0:
                        ok = False
                        break
                    c.append(ci)
                if not ok:
                    continue
                # Check boundary at n-1
                d_last = 1 - (1 if e <= n-2 else 0)  # = 1 if e==n-1, else 0
                num = c[-1] + d_last
                if num < 0 or num % 2 != 0:
                    continue
                a_last = num // 2
                if a_last + (1 if e == n-1 else 0) != f[n-1]:
                    continue
                total = 1 + sum(c)
                if best is None or total < best:
                    best = total
            return best if best is not None else float('inf')
        
        def check(T):
            if T == 0:
                return True
            need = [(T + points[i] - 1) // points[i] for i in range(n)]
            return min_moves(need) <= m
        
        lo, hi = 0, max(points) * m
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if check(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo