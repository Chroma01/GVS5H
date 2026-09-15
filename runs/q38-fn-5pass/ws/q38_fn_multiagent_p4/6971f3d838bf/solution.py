from typing import List
import random
from itertools import product


def _merge(a, b):
    """Merge two segment summaries. None represents the empty sequence."""
    if a is None:
        return b
    if b is None:
        return a

    sa, pa, ua, ba = a
    sb, pb, ub, bb = b

    s = sa + sb

    t = sa + pb
    p = pa if pa >= t else t

    t = sb + ua
    u = ub if ub >= t else t

    best = ba if ba >= bb else bb
    t = ua + pb
    if t > best:
        best = t

    return (s, p, u, best)


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        if not nums:
            return 0

        n = len(nums)

        # Original maximum subarray sum, and group negative values by positions.
        ans = cur = nums[0]
        pos = {}

        for i in range(n):
            v = nums[i]

            if i:
                if cur < 0:
                    cur = v
                else:
                    cur += v
                if cur > ans:
                    ans = cur

            if v < 0:
                lst = pos.get(v)
                if lst is None:
                    pos[v] = [i]
                else:
                    lst.append(i)

        # If there is no negative value, deleting non-negative values cannot help.
        # If n == 1, deleting the only value is invalid.
        if not pos or n == 1:
            return ans

        # If all elements are the same negative value, deletion is invalid.
        if len(pos) == 1:
            only = next(iter(pos.values()))
            if len(only) == n:
                return ans

        mg = _merge

        # Prefix summaries: pref[i] summarizes nums[0:i].
        pref = [None] * (n + 1)
        for i in range(n):
            v = nums[i]
            pref[i + 1] = mg(pref[i], (v, v, v, v))

        # Suffix summaries: suff[i] summarizes nums[i:n].
        suff = [None] * (n + 1)
        for i in range(n - 1, -1, -1):
            v = nums[i]
            suff[i] = mg((v, v, v, v), suff[i + 1])

        # A segment tree is needed only for internal blocks between occurrences.
        need_tree = False
        for lst in pos.values():
            m = len(lst)
            if m > 1:
                prev = lst[0] + 1
                for j in range(1, m):
                    p = lst[j]
                    if prev < p:
                        need_tree = True
                        break
                    prev = p + 1
                if need_tree:
                    break

        query = None
        if need_tree:
            size = 1
            while size < n:
                size <<= 1

            tree = [None] * (size << 1)
            base = size

            for i in range(n):
                v = nums[i]
                tree[base + i] = (v, v, v, v)

            for i in range(base - 1, 0, -1):
                tree[i] = mg(tree[i << 1], tree[(i << 1) | 1])

            def query(l, r, tree=tree, base=base, mg=mg):
                if l >= r:
                    return None

                l += base
                r += base
                left = None
                right = None

                while l < r:
                    if l & 1:
                        left = mg(left, tree[l])
                        l += 1
                    if r & 1:
                        r -= 1
                        right = mg(tree[r], right)
                    l >>= 1
                    r >>= 1

                return mg(left, right)

        # For each negative value, concatenate all blocks that remain after deletion.
        for lst in pos.values():
            m = len(lst)

            # Removing this value would empty the array.
            if m == n:
                continue

            # Single occurrence: only prefix and suffix blocks.
            if m == 1:
                p = lst[0]
                acc = pref[p] if p > 0 else None
                if p + 1 < n:
                    acc = mg(acc, suff[p + 1])

                if acc is not None and acc[3] > ans:
                    ans = acc[3]
                continue

            acc = None

            first = lst[0]
            if first > 0:
                acc = pref[first]

            prev = first + 1
            for j in range(1, m):
                p = lst[j]
                if prev < p:
                    acc = mg(acc, query(prev, p))
                prev = p + 1

            if prev < n:
                acc = mg(acc, suff[prev])

            if acc is not None and acc[3] > ans:
                ans = acc[3]

        return ans


def _max_subarray_brute(arr):
    """Independent O(n^2) maximum subarray sum for the checker."""
    best = arr[0]
    n = len(arr)
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += arr[j]
            if s > best:
                best = s
    return best


def _brute(nums):
    ans = _max_subarray_brute(nums)
    seen = set()

    for x in nums:
        if x in seen:
            continue
        seen.add(x)

        arr = [v for v in nums if v != x]
        if not arr:
            continue

        val = _max_subarray_brute(arr)
        if val > ans:
            ans = val

    return ans


if __name__ == "__main__":
    sol = Solution()

    sample_cases = [
        ([-3, 2, -2, -1, 3, -2, 3], 7),
        ([1, 2, 3, 4], 10),
    ]

    sample_ok = True
    for nums, expected in sample_cases:
        got = sol.maxSubarraySum(nums)
        if got != expected:
            sample_ok = False
            print("Sample fail:", nums, got, expected)

    print("Sample verdict:", "pass" if sample_ok else "fail")

    random.seed(123456)
    random_ok = True
    random_fail = None

    for _ in range(1000):
        n = random.randint(1, 8)
        nums = [random.randint(-5, 5) for _ in range(n)]

        got = sol.maxSubarraySum(nums)
        expected = _brute(nums)

        if got != expected:
            random_ok = False
            random_fail = (nums, got, expected)
            break

    if random_fail is not None:
        print("Random fail:", random_fail)

    print("Random verdict:", "pass" if random_ok else "fail")

    exhaustive_ok = None
    exhaustive_fail = None

    if random_ok:
        exhaustive_ok = True

        for n in range(1, 5):
            for tup in product(range(-2, 3), repeat=n):
                nums = list(tup)

                got = sol.maxSubarraySum(nums)
                expected = _brute(nums)

                if got != expected:
                    exhaustive_ok = False
                    exhaustive_fail = (nums, got, expected)
                    break

            if not exhaustive_ok:
                break

        if exhaustive_fail is not None:
            print("Exhaustive fail:", exhaustive_fail)

    if exhaustive_ok is not None:
        print("Exhaustive verdict:", "pass" if exhaustive_ok else "fail")