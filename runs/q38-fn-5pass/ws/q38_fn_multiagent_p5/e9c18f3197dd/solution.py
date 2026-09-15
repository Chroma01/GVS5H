from typing import List
from math import gcd
from itertools import product

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        k = len(target)
        if k == 0:
            return 0

        size = 1 << k

        # lcm[mask] = lcm of target indices contained in mask
        lcms = [1] * size
        for mask in range(1, size):
            lsb = mask & -mask
            i = lsb.bit_length() - 1
            prev = mask ^ lsb
            if prev:
                a, b = lcms[prev], target[i]
                lcms[mask] = a // gcd(a, b) * b
            else:
                lcms[mask] = target[i]

        # For every non-empty subset, keep the 4 cheapest (cost, nums_index).
        top = [[] for _ in range(size)]
        for idx, x in enumerate(nums):
            for mask in range(1, size):
                cost = (-x) % lcms[mask]
                lst = top[mask]

                if len(lst) < 4:
                    lst.append((cost, idx))
                    j = len(lst) - 1
                    while j > 0 and lst[j - 1][0] > cost:
                        lst[j], lst[j - 1] = lst[j - 1], lst[j]
                        j -= 1
                elif cost < lst[-1][0]:
                    lst[-1] = (cost, idx)
                    j = 3
                    while j > 0 and lst[j - 1][0] > cost:
                        lst[j], lst[j - 1] = lst[j - 1], lst[j]
                        j -= 1

        # Generate all set partitions of target indices.
        partitions = []
        groups = []

        def gen(i: int) -> None:
            if i == k:
                partitions.append(tuple(groups))
                return

            bit = 1 << i

            # Put index i into an existing group.
            for j in range(len(groups)):
                groups[j] |= bit
                gen(i + 1)
                groups[j] ^= bit

            # Start a new group.
            groups.append(bit)
            gen(i + 1)
            groups.pop()

        gen(0)

        ans = 10 ** 30

        for part in partitions:
            m = len(part)

            # For a partition with m groups, top m candidates per group suffice.
            cand = [top[mask][:m] for mask in part]

            # Try all assignments of groups to candidate nums indices.
            for combo in product(*cand):
                if len({idx for _, idx in combo}) == m:
                    total = sum(cost for cost, _ in combo)
                    if total < ans:
                        ans = total

            if ans == 0:
                break

        return ans