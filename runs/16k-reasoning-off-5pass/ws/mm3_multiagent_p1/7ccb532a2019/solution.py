class Solution:
    def makeStringGood(self, s: str) -> int:
        from collections import Counter
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - 97] += 1
        n = len(s)
        ans = n  # cost to delete everything

        # Try all possible number of distinct letters k and target frequency f
        for k in range(1, 27):
            if k > n:
                break
            for f in range(1, n + 1):
                # Weight for each letter: |cnt[i] - f| - cnt[i]
                weights = [abs(c - f) - c for c in cnt]
                weights.sort()
                # Sum of k smallest weights
                curr = sum(weights[:k])
                total = n + curr
                if total < ans:
                    ans = total
        return ans