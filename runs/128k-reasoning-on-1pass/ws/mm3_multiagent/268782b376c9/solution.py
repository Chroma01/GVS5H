from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        NEG = -10**30  # -infinity for max‑plus semiring

        class SegTree:
            __slots__ = ('size', 'tree')
            def __init__(self, w: List[int]):
                sz = 1 << (len(w) - 1).bit_length()
                self.size = sz
                # identity matrix for max‑plus: [[0, -inf], [-inf, 0]]
                ID = (0, NEG, NEG, 0)
                self.tree = [ID] * (2 * sz)
                # set leaves for actual vertices
                for i, wi in enumerate(w):
                    self.tree[sz + i] = (0, wi, 0, NEG)
                # build internal nodes
                for i in range(sz - 1, 0, -1):
                    self.tree[i] = self._combine(self.tree[2*i], self.tree[2*i+1])

            @staticmethod
            def _combine(A, B):
                a00, a01, a10, a11 = A
                b00, b01, b10, b11 = B
                # max‑plus matrix multiplication
                c00 = a00 + b00
                if a01 + b10 > c00:
                    c00 = a01 + b10
                c01 = a00 + b01
                if a01 + b11 > c01:
                    c01 = a01 + b11
                c10 = a10 + b00
                if a11 + b10 > c10:
                    c10 = a11 + b10
                c11 = a10 + b01
                if a11 + b11 > c11:
                    c11 = a11 + b11
                return (c00, c01, c10, c11)

            def update(self, idx: int, w: int):
                i = self.size + idx
                self.tree[i] = (0, w, 0, NEG)
                i //= 2
                while i:
                    self.tree[i] = self._combine(self.tree[2*i], self.tree[2*i+1])
                    i //= 2

            def query(self) -> int:
                root = self.tree[1]
                # first row corresponds to previous state = 0
                return root[0] if root[0] > root[1] else root[1]

        def can(X: int) -> bool:
            # minimal required visits for each cell
            need = [(X + points[i] - 1) // points[i] for i in range(n)]

            # initialise weights w[i] for final index p = 0
            w = [0] * n
            w0 = need[0] - 1
            if w0 < 0:
                w0 = 0
            w[0] = w0
            for i in range(1, n):
                w[i] = need[i]  # i > p, so no subtraction yet

            seg = SegTree(w)

            for p in range(n):
                S = seg.query()                # max‑weight independent set
                L = 1 + p + 2 * S
                if L <= m:
                    return True

                if p + 1 < n:
                    # when p increases, weight of vertex p+1 is reduced by one
                    new_w = need[p + 1] - 1
                    if new_w < 0:
                        new_w = 0
                    seg.update(p + 1, new_w)

            return False

        # binary search on the answer
        lo, hi = 0, m * max(points)   # feasible lower bound, upper bound
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if can(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo