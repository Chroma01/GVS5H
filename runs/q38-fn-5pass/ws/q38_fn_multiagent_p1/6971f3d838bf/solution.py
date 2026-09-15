from typing import List
from collections import defaultdict


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        if n == 1:
            return nums[0]

        NEG = -10**30

        # Occurrence lists and baseline Kadane answer (no deletion).
        positions = defaultdict(list)
        cur = best = nums[0]
        positions[nums[0]].append(0)

        for i in range(1, n):
            v = nums[i]
            positions[v].append(i)

            if cur > 0:
                cur += v
            else:
                cur = v

            if cur > best:
                best = cur

        baseline = best

        # If every element is the same, deleting that value is invalid.
        if len(positions) == 1:
            return baseline

        # Prefix monoids for nums[0:i].
        pre_sum = [0] * (n + 1)
        pre_pref = [NEG] * (n + 1)
        pre_suff = [NEG] * (n + 1)
        pre_best = [NEG] * (n + 1)

        for i, v in enumerate(nums, 1):
            s1 = pre_sum[i - 1]
            pre_sum[i] = s1 + v

            t = s1 + v
            pp = pre_pref[i - 1]
            pre_pref[i] = pp if pp >= t else t

            t = v + pre_suff[i - 1]
            pre_suff[i] = v if v >= t else t

            pb = pre_best[i - 1]
            b = pb if pb >= v else v
            t = pre_suff[i - 1] + v
            if t > b:
                b = t
            pre_best[i] = b

        # Suffix monoids for nums[i:n].
        suf_sum = [0] * (n + 1)
        suf_pref = [NEG] * (n + 1)
        suf_suff = [NEG] * (n + 1)
        suf_best = [NEG] * (n + 1)

        for i in range(n - 1, -1, -1):
            v = nums[i]
            s2 = suf_sum[i + 1]

            suf_sum[i] = v + s2

            t = v + suf_pref[i + 1]
            suf_pref[i] = v if v >= t else t

            t = s2 + v
            ss = suf_suff[i + 1]
            suf_suff[i] = ss if ss >= t else t

            sb = suf_best[i + 1]
            b = sb if sb >= v else v
            t = v + suf_pref[i + 1]
            if t > b:
                b = t
            suf_best[i] = b

        # A segment tree is needed only for internal gaps of length >= 3.
        need_tree = False
        for pos in positions.values():
            if len(pos) >= 2:
                prev = pos[0]
                for idx in pos[1:]:
                    if idx - prev - 1 >= 3:
                        need_tree = True
                        break
                    prev = idx
                if need_tree:
                    break

        query = None

        if need_tree:
            size = 1
            while size < n:
                size <<= 1

            m = size << 1
            seg_sum = [0] * m
            seg_pref = [NEG] * m
            seg_suff = [NEG] * m
            seg_best = [NEG] * m

            base = size
            for i, v in enumerate(nums):
                idx = base + i
                seg_sum[idx] = v
                seg_pref[idx] = v
                seg_suff[idx] = v
                seg_best[idx] = v

            for i in range(size - 1, 0, -1):
                left = i << 1
                right = left | 1

                s1 = seg_sum[left]
                s2 = seg_sum[right]
                seg_sum[i] = s1 + s2

                t = s1 + seg_pref[right]
                p = seg_pref[left]
                seg_pref[i] = p if p >= t else t

                t = s2 + seg_suff[left]
                su = seg_suff[right]
                seg_suff[i] = su if su >= t else t

                b = seg_best[left] if seg_best[left] >= seg_best[right] else seg_best[right]
                t = seg_suff[left] + seg_pref[right]
                if t > b:
                    b = t
                seg_best[i] = b

            def query(
                l,
                r,
                seg_sum=seg_sum,
                seg_pref=seg_pref,
                seg_suff=seg_suff,
                seg_best=seg_best,
                size=size,
                NEG=NEG,
            ):
                l += size
                r += size

                ls = 0
                lp = NEG
                lsu = NEG
                lb = NEG

                rs = 0
                rp = NEG
                rsu = NEG
                rb = NEG

                while l < r:
                    if l & 1:
                        ns = ls + seg_sum[l]

                        t = ls + seg_pref[l]
                        np = lp if lp >= t else t

                        t = seg_sum[l] + lsu
                        nsu = seg_suff[l] if seg_suff[l] >= t else t

                        nb = lb if lb >= seg_best[l] else seg_best[l]
                        t = lsu + seg_pref[l]
                        if t > nb:
                            nb = t

                        ls, lp, lsu, lb = ns, np, nsu, nb
                        l += 1

                    if r & 1:
                        r -= 1

                        ns = seg_sum[r] + rs

                        t = seg_sum[r] + rp
                        np = seg_pref[r] if seg_pref[r] >= t else t

                        t = rs + seg_suff[r]
                        nsu = rsu if rsu >= t else t

                        nb = seg_best[r] if seg_best[r] >= rb else rb
                        t = seg_suff[r] + rp
                        if t > nb:
                            nb = t

                        rs, rp, rsu, rb = ns, np, nsu, nb

                    l >>= 1
                    r >>= 1

                ns = ls + rs

                t = ls + rp
                np = lp if lp >= t else t

                t = rs + lsu
                nsu = rsu if rsu >= t else t

                nb = lb if lb >= rb else rb
                t = lsu + rp
                if t > nb:
                    nb = t

                return ns, np, nsu, nb

        def merge_acc_node(as_, ap, asu, ab, s, pf, sf, bf):
            ns = as_ + s

            t = as_ + pf
            np = ap if ap >= t else t

            t = s + asu
            nsu = sf if sf >= t else t

            nb = ab if ab >= bf else bf
            t = asu + pf
            if t > nb:
                nb = t

            return ns, np, nsu, nb

        def get_gap(
            l,
            r,
            nums=nums,
            n=n,
            NEG=NEG,
            pre_sum=pre_sum,
            pre_pref=pre_pref,
            pre_suff=pre_suff,
            pre_best=pre_best,
            suf_sum=suf_sum,
            suf_pref=suf_pref,
            suf_suff=suf_suff,
            suf_best=suf_best,
            query=query,
        ):
            if l >= r:
                return 0, NEG, NEG, NEG

            length = r - l

            if length == 1:
                v = nums[l]
                return v, v, v, v

            if length == 2:
                a = nums[l]
                b = nums[l + 1]
                s = a + b

                p = a if a >= s else s
                su = b if b >= s else s

                best2 = a if a >= b else b
                if s > best2:
                    best2 = s

                return s, p, su, best2

            if l == 0:
                return pre_sum[r], pre_pref[r], pre_suff[r], pre_best[r]

            if r == n:
                return suf_sum[l], suf_pref[l], suf_suff[l], suf_best[l]

            return query(l, r)

        ans = baseline

        for pos in positions.values():
            # Deleting a value that appears everywhere would empty the array.
            if len(pos) == n:
                continue

            as_ = 0
            ap = NEG
            asu = NEG
            ab = NEG

            prev = 0

            for idx in pos:
                if prev < idx:
                    s, pf, sf, bf = get_gap(prev, idx)
                    as_, ap, asu, ab = merge_acc_node(
                        as_, ap, asu, ab, s, pf, sf, bf
                    )
                prev = idx + 1

            if prev < n:
                s, pf, sf, bf = get_gap(prev, n)
                as_, ap, asu, ab = merge_acc_node(
                    as_, ap, asu, ab, s, pf, sf, bf
                )

            if ab > ans:
                ans = ab

        return ans


def brute_force(nums: List[int]) -> int:
    if not nums:
        return 0

    def max_sub(arr: List[int]) -> int:
        if not arr:
            return -10**30
        cur = best = arr[0]
        for v in arr[1:]:
            if cur > 0:
                cur += v
            else:
                cur = v
            if cur > best:
                best = cur
        return best

    ans = max_sub(nums)
    n = len(nums)
    for x in set(nums):
        if nums.count(x) == n:
            continue
        arr = [v for v in nums if v != x]
        if arr:
            val = max_sub(arr)
            if val > ans:
                ans = val
    return ans


def run_tests() -> None:
    tests = [
        ([-3, 2, -2, -1, 3, -2, 3], 7),
        ([1, 2, 3, 4], 10),
        ([5], 5),
        ([-7], -7),
        ([-2, -3, -1], -1),
        ([-5, -5, -2, -5], -2),
        ([2, 2, 2], 6),
        ([-1, -1], -1),
        ([1, 2, 1], 4),
        ([1, 1, -100, 1, 1], 4),
        ([0, 0, 0], 0),
        ([1, 1, 1, 2], 5),
        ([10, -1, 2, 3, 4, -1, 10], 29),
        ([5, -1, -2, -3, 5, -1, 5], 10),
    ]

    sol = Solution()
    failures = []

    for nums, expected in tests:
        got = sol.maxSubarraySum(nums)
        if got != expected:
            failures.append((nums, expected, got))

    import random

    random.seed(12345)
    for _ in range(200):
        n = random.randint(1, 8)
        arr = [random.randint(-5, 5) for _ in range(n)]
        expected = brute_force(arr)
        got = sol.maxSubarraySum(arr)
        if got != expected:
            failures.append((arr, expected, got))
            break

    if failures:
        print("FAIL")
        for nums, expected, got in failures:
            print(f"input={nums} expected={expected} got={got}")
    else:
        print("PASS")


if __name__ == "__main__":
    run_tests()