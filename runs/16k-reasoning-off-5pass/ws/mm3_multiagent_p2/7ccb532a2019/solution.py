class Solution:
    def makeStringGood(self, s: str) -> int:
        n = len(s)
        counts = [0] * 26
        for c in s:
            counts[ord(c) - ord('a')] += 1
        sorted_counts = sorted(counts, reverse=True)
        ans = n  # cost of deleting all characters
        for k in range(1, n + 1):
            excess = 0
            deficit = 0
            unkept = n
            # incrementally evaluate keeping d = 1, 2, ..., 26 distinct chars
            for d in range(26):
                c = sorted_counts[d]
                unkept -= c
                if c > k:
                    excess += c - k
                else:
                    deficit += k - c
                # cost for keeping the top d+1 characters
                cost = excess + max(unkept, deficit)
                if cost < ans:
                    ans = cost
        return ans