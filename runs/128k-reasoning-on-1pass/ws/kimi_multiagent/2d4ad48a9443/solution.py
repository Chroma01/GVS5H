from array import array
from typing import List


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)

        # nxt[i] = smallest j > i with nums[j] > nums[i] (strictly greater),
        # or n if there is none. These are exactly the "record high" jumps.
        nxt = [n] * (n + 1)
        stack = []
        for i, v in enumerate(nums):
            while stack and nums[stack[-1]] < v:
                nxt[stack.pop()] = i
            stack.append(i)

        size = n + 1
        LOG = max(1, n.bit_length())

        # Binary lifting over next-strictly-greater chains.
        # up[j][i] = index reached after 2^j chain steps starting at i.
        # sm[j][i] = sum of nums[x] * (nxt[x] - x) over those 2^j records,
        #            i.e. the full running-max contribution of that block.
        up = [array('i', nxt)]
        sm = [array('q', [nums[i] * (nxt[i] - i) for i in range(n)] + [0])]
        for _ in range(1, LOG):
            pu, ps = up[-1], sm[-1]
            up.append(array('i', [pu[pu[i]] for i in range(size)]))
            sm.append(array('q', [ps[i] + ps[pu[i]] for i in range(size)]))

        # Ordinary prefix sums of nums.
        pref = [0] * size
        run = 0
        for i, v in enumerate(nums):
            run += v
            pref[i + 1] = run

        ans = 0
        r = -1
        jrange = range(LOG - 1, -1, -1)
        for l in range(n):
            if r < l - 1:
                r = l - 1
            base = pref[l]
            # Extend r while cost(l, r+1) <= k (cost is monotone in r).
            while r + 1 < n:
                nr = r + 1
                # sum_running_max(l, nr): walk the record chain from l,
                # taking whole 2^j blocks whose end stays <= nr.
                cur = l
                tot = 0
                for j in jrange:
                    u = up[j][cur]
                    if u <= nr:
                        tot += sm[j][cur]
                        cur = u
                # Last record segment is clipped at nr+1.
                tot += nums[cur] * (nr + 1 - cur)
                # cost = sum_running_max - range_sum
                if tot - (pref[nr + 1] - base) <= k:
                    r = nr
                else:
                    break
            ans += r - l + 1
        return ans