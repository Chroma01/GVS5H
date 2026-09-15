from typing import List
from collections import deque


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)

        # If removing any one word leaves fewer than k words, every answer is 0.
        if n - 1 < k:
            return [0] * n

        # For k == 1, the LCP of one string is its full length.
        # The answer is the maximum length among the remaining words.
        if k == 1:
            max1 = 0
            max2 = 0
            cnt1 = 0

            for w in words:
                length = len(w)
                if length > max1:
                    max2 = max1
                    max1 = length
                    cnt1 = 1
                elif length == max1:
                    cnt1 += 1
                elif length > max2:
                    max2 = length

            ans = []
            for w in words:
                length = len(w)
                if length == max1 and cnt1 == 1:
                    ans.append(max2)
                else:
                    ans.append(max1)
            return ans

        # Sort occurrence indices lexicographically.
        order = sorted(range(n), key=words.__getitem__)

        # Adjacent LCP array in sorted order.
        lcp = [0] * (n - 1)
        prev = words[order[0]]

        for pos in range(1, n):
            cur = words[order[pos]]
            limit = len(prev)
            if len(cur) < limit:
                limit = len(cur)

            j = 0
            while j < limit and prev[j] == cur[j]:
                j += 1

            lcp[pos - 1] = j
            prev = cur

        # Values of all original k-windows.
        # A k-window LCP is the minimum of k-1 adjacent LCP values.
        win = self._sliding_min(lcp, k - 1)
        m = len(win)

        # Prefix maxima of k-window values.
        pref = [0] * m
        best = 0
        for i, val in enumerate(win):
            if val > best:
                best = val
            pref[i] = best

        # Suffix maxima of k-window values.
        suff = [0] * m
        best = 0
        for i in range(m - 1, -1, -1):
            val = win[i]
            if val > best:
                best = val
            suff[i] = best

        # Global baseline: maximum LCP over all original (k + 1)-windows.
        # This value is safe for every removal.
        baseline = self._max_sliding_min(lcp, k)

        ans = [0] * n

        for pos, orig in enumerate(order):
            res = baseline

            # k-windows completely before pos: start <= pos - k.
            left = pos - k
            if left >= 0:
                val = pref[left]
                if val > res:
                    res = val

            # k-windows completely after pos: start >= pos + 1.
            right = pos + 1
            if right < m:
                val = suff[right]
                if val > res:
                    res = val

            ans[orig] = res

        return ans

    def _sliding_min(self, arr: List[int], window: int) -> List[int]:
        n = len(arr)

        if window <= 1:
            return arr

        if window > n:
            return []

        dq = deque()
        res = []

        for i, x in enumerate(arr):
            while dq and arr[dq[-1]] >= x:
                dq.pop()

            dq.append(i)

            if dq[0] <= i - window:
                dq.popleft()

            if i >= window - 1:
                res.append(arr[dq[0]])

        return res

    def _max_sliding_min(self, arr: List[int], window: int) -> int:
        n = len(arr)

        if n == 0:
            return 0

        if window <= 1:
            return max(arr)

        if window > n:
            return 0

        dq = deque()
        best = 0

        for i, x in enumerate(arr):
            while dq and arr[dq[-1]] >= x:
                dq.pop()

            dq.append(i)

            if dq[0] <= i - window:
                dq.popleft()

            if i >= window - 1:
                val = arr[dq[0]]
                if val > best:
                    best = val

        return best