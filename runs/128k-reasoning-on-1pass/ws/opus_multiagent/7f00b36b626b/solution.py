from typing import List


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        T = threshold
        present = bytearray(T + 1)
        big = 0
        small = 0
        for v in nums:
            if v > T:
                big += 1
            elif not present[v]:
                present[v] = 1
                small += 1

        if small == 0:
            return big
        if small == 1:
            return 1 + big

        pa = list(range(T + 1))
        sz = [1] * (T + 1)
        comp = small
        pres = present

        for d in range(1, T + 1):
            # smallest present multiple of d
            s = 0
            for x in range(d, T + 1, d):
                if pres[x]:
                    s = x
                    break
            if s == 0:
                continue
            # union s with every present multiple x of d such that s*x/d <= T
            lim = T * d // s
            if lim > T:
                lim = T
            if lim <= s:
                continue
            # root of s
            rs = s
            while pa[rs] != rs:
                pa[rs] = pa[pa[rs]]
                rs = pa[rs]
            for x in range(s + d, lim + 1, d):
                if pres[x]:
                    rx = pa[x]
                    if rx == rs:
                        continue
                    while pa[rx] != rx:
                        pa[rx] = pa[pa[rx]]
                        rx = pa[rx]
                    if rx != rs:
                        if sz[rx] > sz[rs]:
                            rx, rs = rs, rx
                        pa[rx] = rs
                        sz[rs] += sz[rx]
                        comp -= 1
                        if comp == 1:
                            break
            if comp == 1:
                break

        return comp + big