class Solution:
    def makeStringGood(self, s: str) -> int:
        n = len(s)
        from collections import Counter
        cnt = Counter(s)
        # frequencies of each letter, 26 letters
        freqs = [cnt[chr(ord('a') + i)] for i in range(26)]
        max_k = max(freqs) + n  # upper bound for k; n is safe upper bound anyway
        # iterate over k from 0 to n
        best = n  # worst case: delete all
        for k in range(0, n + 1):
            total = 0
            num_used = 0  # how many letters we decide to use with frequency k
            for c in freqs:
                if c == k:
                    continue
                # cost to make this letter unused: c deletions
                cost_to_zero = c
                # cost to make this letter used with frequency k
                if c <= k:
                    cost_to_k = k - c  # inserts
                else:
                    cost_to_k = c - k  # deletions (or use increments on other letters)
                # choose the cheaper option
                total += min(cost_to_zero, cost_to_k)
                # if we choose to use it (cost_to_k is cheaper), we will use this letter
                if cost_to_k <= cost_to_zero:
                    num_used += 1
            # extra inserts if total target length exceeds n
            total += max(0, num_used * k - n)
            if total < best:
                best = total
        return best