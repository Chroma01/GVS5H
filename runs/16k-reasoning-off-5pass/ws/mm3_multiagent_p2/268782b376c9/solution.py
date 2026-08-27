class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        if m < n:
            return 0
        
        lo, hi = 0, min(points) * m
        
        def feasible(X):
            if X == 0:
                return True
            need = [(X + p - 1) // p for p in points]
            
            # pref[p] = max_{1 <= i <= p} (need[i] - 1), pref[0] = 0
            pref = [0] * n
            for i in range(1, n):
                pref[i] = max(pref[i-1], need[i] - 1)
            
            # suf[p] = max_{p < i < n} need[i], suf[n-1] = 0
            suf = [0] * n
            for i in range(n-2, -1, -1):
                suf[i] = max(suf[i+1], need[i+1])
            
            base = need[0] - 2
            
            for p in range(n):
                D = max(base, pref[p], suf[p])
                if D < 0:
                    D = 0
                k = (D + 1) // 2
                T = 1 + 2 * n * k + p
                if T <= m:
                    return True
            return False
        
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo