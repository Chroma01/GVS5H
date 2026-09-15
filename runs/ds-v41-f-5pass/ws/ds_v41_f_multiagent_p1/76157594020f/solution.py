class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)

        def feasible(L: int) -> bool:
            # L == 1: final string must be fully alternating; cost is the
            # Hamming distance to the two possible alternating patterns.
            if L == 1:
                cost0 = 0  # target starts with '0': 0101...
                cost1 = 0  # target starts with '1': 1010...
                for i, ch in enumerate(s):
                    if i % 2 == 0:
                        if ch != '0':
                            cost0 += 1
                        else:
                            cost1 += 1
                    else:
                        if ch != '1':
                            cost0 += 1
                        else:
                            cost1 += 1
                return min(cost0, cost1) <= numOps

            # L >= 2: runs are independent; a run of length m needs
            # m // (L + 1) interior flips so that no piece exceeds L.
            total = 0
            i = 0
            while i < n:
                j = i
                while j < n and s[j] == s[i]:
                    j += 1
                run = j - i
                total += run // (L + 1)
                if total > numOps:
                    return False
                i = j
            return total <= numOps

        # Feasibility is monotone in L -> binary search for the smallest.
        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo