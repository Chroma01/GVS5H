from typing import List
from array import array
from collections import deque


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        a = nums

        # prefix sums of the original array
        pref = [0] * (n + 1)
        acc = 0
        for i in range(n):
            acc += a[i]
            pref[i + 1] = acc

        # nxt[i] = first j > i with a[j] > a[i], else n  (strictly greater)
        nxt = [n] * n
        st = []
        for i in range(n - 1, -1, -1):
            ai = a[i]
            while st and a[st[-1]] <= ai:
                st.pop()
            if st:
                nxt[i] = st[-1]
            st.append(i)

        # Binary lifting over the running-max record chain.
        # up[j][i]  = position after 2^j record jumps from i (sentinel n)
        # add[j][i] = sum of full contribution blocks for those 2^j records.
        LOG = max(1, n.bit_length())

        up0 = array('q', [n]) * (n + 1)
        add0 = array('q', [0]) * (n + 1)
        for i in range(n):
            q = nxt[i]
            up0[i] = q
            add0[i] = a[i] * (q - i)

        up = [up0]
        add = [add0]
        for _ in range(1, LOG):
            pu = up[-1]
            pa = add[-1]
            cu = array('q', [n]) * (n + 1)
            ca = array('q', [0]) * (n + 1)
            for i in range(n):
                mid = pu[i]
                cu[i] = pu[mid]
                ca[i] = pa[i] + pa[mid]
            up.append(cu)
            add.append(ca)

        # S(L, R) = sum of running prefix maxima of a[L..R]
        def S(L: int, R: int) -> int:
            p = L
            s = 0
            for j in range(LOG - 1, -1, -1):
                q = up[j][p]
                if q <= R:
                    s += add[j][p]
                    p = q
            return s + a[p] * (R - p + 1)

        dq = deque()          # indices, values strictly decreasing (front = window max)
        left = 0
        ans = 0
        cost = 0
        for right in range(n):
            ar = a[right]
            while dq and a[dq[-1]] <= ar:
                dq.pop()
            dq.append(right)

            # Appending only changes the new element's contribution:
            # cost(l,r) = cost(l,r-1) + (max(a[l..r]) - a[r])
            if left == right:
                cost = 0
            else:
                cost += a[dq[0]] - ar

            while cost > k:
                left += 1
                if dq[0] < left:
                    dq.popleft()
                cost = S(left, right) - (pref[right + 1] - pref[left])

            ans += right - left + 1

        return ans