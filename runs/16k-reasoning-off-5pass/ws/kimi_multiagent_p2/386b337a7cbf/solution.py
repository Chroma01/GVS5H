from typing import List


class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        total = sum(nums)
        # Alternating sum of any subsequence lies in [-total, total].
        if k > total or k < -total:
            return -1

        CAP = limit + 1  # absorbing "product exceeds limit" marker

        # dp_even[s]: set of achievable products for subsequences of even
        #             length whose alternating sum is s.
        # dp_odd[s]:  same for odd length.
        # The empty subsequence is intentionally NOT represented anywhere,
        # so it can never be reported as an answer.
        dp_even = {}
        dp_odd = {}

        def add(dp, s, p):
            st = dp.get(s)
            if st is None:
                dp[s] = {p}
            else:
                st.add(p)

        for v in nums:
            # Snapshot current states; transitions for this element only
            # read from the snapshot so each element is used at most once.
            new_odd = []   # transitions into the odd-length layer
            new_even = []  # transitions into the even-length layer

            # Pick v after an even-length subsequence: it lands at an even
            # (0-indexed) position -> add v.
            for s, prods in dp_even.items():
                ns = s + v
                for p in prods:
                    np = p * v
                    if np > limit:
                        np = CAP
                    new_odd.append((ns, np))

            # Pick v after an odd-length subsequence: it lands at an odd
            # position -> subtract v.
            for s, prods in dp_odd.items():
                ns = s - v
                for p in prods:
                    np = p * v
                    if np > limit:
                        np = CAP
                    new_even.append((ns, np))

            # Pick v as the first element (length 1, odd): sum = v, product = v.
            add(dp_odd, v, v if v <= limit else CAP)

            for s, p in new_odd:
                add(dp_odd, s, p)
            for s, p in new_even:
                add(dp_even, s, p)

        best = -1
        for dp in (dp_even, dp_odd):
            prods = dp.get(k)
            if prods:
                for p in prods:
                    if p <= limit and p > best:
                        best = p
        return best