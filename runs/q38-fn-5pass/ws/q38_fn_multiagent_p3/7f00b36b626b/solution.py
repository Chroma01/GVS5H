from typing import List

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        small = set()
        large = 0

        for x in nums:
            if x <= threshold:
                small.add(x)
            else:
                large += 1

        if not small:
            return large

        # If 1 is present, every small value is connected to it.
        # If there is only one distinct small value, it forms one component.
        if 1 in small or len(small) == 1:
            return large + 1

        T = threshold
        T1 = T + 1
        half = T // 2

        parent = list(range(T1))
        size = [1] * T1

        def find(a: int) -> int:
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        # For each present value x <= threshold, union it with all multiples
        # of x up to threshold. Two values are connected iff they share a
        # common multiple <= threshold, equivalent to lcm <= threshold.
        for x in small:
            if x > half:
                continue

            rx = find(x)
            for m in range(x + x, T1, x):
                rm = find(m)
                if rx != rm:
                    if size[rx] < size[rm]:
                        rx, rm = rm, rx
                    parent[rm] = rx
                    size[rx] += size[rm]

        return large + len({find(x) for x in small})