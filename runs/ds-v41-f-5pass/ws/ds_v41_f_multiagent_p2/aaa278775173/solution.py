from typing import List

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        sz = n * m

        # Flatten grid for speed.
        g = [0] * sz
        for i in range(n):
            row = grid[i]
            base = i * m
            for j in range(m):
                g[base + j] = row[j]

        # next value in the sequence 1,2,0,2,0,...
        # 1->2, 2->0, 0->2
        nxt = (2, 2, 0)

        # Directions: 0=DR (1,1), 1=DL (1,-1), 2=UL (-1,-1), 3=UR (-1,1)
        # R[d][idx] = longest alternating straight segment STARTING at idx going d.
        R0 = [1] * sz
        R1 = [1] * sz
        R2 = [1] * sz
        R3 = [1] * sz

        # R0 DR: successor (i+1, j+1)
        for i in range(n - 1, -1, -1):
            base = i * m
            for j in range(m - 1, -1, -1):
                idx = base + j
                if i + 1 < n and j + 1 < m:
                    q = idx + m + 1
                    if g[q] == nxt[g[idx]]:
                        R0[idx] = R0[q] + 1
        # R1 DL: successor (i+1, j-1)
        for i in range(n - 1, -1, -1):
            base = i * m
            for j in range(m):
                idx = base + j
                if i + 1 < n and j > 0:
                    q = idx + m - 1
                    if g[q] == nxt[g[idx]]:
                        R1[idx] = R1[q] + 1
        # R2 UL: successor (i-1, j-1)
        for i in range(n):
            base = i * m
            for j in range(m):
                idx = base + j
                if i > 0 and j > 0:
                    q = idx - m - 1
                    if g[q] == nxt[g[idx]]:
                        R2[idx] = R2[q] + 1
        # R3 UR: successor (i-1, j+1)
        for i in range(n):
            base = i * m
            for j in range(m - 1, -1, -1):
                idx = base + j
                if i > 0 and j + 1 < m:
                    q = idx - m + 1
                    if g[q] == nxt[g[idx]]:
                        R3[idx] = R3[q] + 1

        # Length-1 segment is any cell holding 1.
        ans = 1 if 1 in g else 0

        # f[d][idx] = longest alternating straight segment ENDING at idx whose
        # last move was in direction d (must start at a value 1).
        # At a turn vertex, combine first arm (direction d) with second arm
        # (clockwise direction (d+1)%4): total = f + R[(d+1)%4] - 1.
        # Since R >= 1, this also covers zero-turn straight segments.

        # d = 0 (DR), predecessor (i-1,j-1), clockwise -> DL (R1)
        f = [0] * sz
        Rc = R1
        for i in range(n):
            base = i * m
            for j in range(m):
                idx = base + j
                best = 0
                if i > 0 and j > 0:
                    p = idx - m - 1
                    fo = f[p]
                    if fo == 0:
                        fo = 1 if g[p] == 1 else 0
                    if fo and g[idx] == nxt[g[p]]:
                        best = fo + 1
                f[idx] = best
                if best:
                    tot = best + Rc[idx] - 1
                    if tot > ans: ans = tot

        # d = 1 (DL), predecessor (i-1,j+1), clockwise -> UL (R2)
        f = [0] * sz
        Rc = R2
        for i in range(n):
            base = i * m
            for j in range(m - 1, -1, -1):
                idx = base + j
                best = 0
                if i > 0 and j + 1 < m:
                    p = idx - m + 1
                    fo = f[p]
                    if fo == 0:
                        fo = 1 if g[p] == 1 else 0
                    if fo and g[idx] == nxt[g[p]]:
                        best = fo + 1
                f[idx] = best
                if best:
                    tot = best + Rc[idx] - 1
                    if tot > ans: ans = tot

        # d = 2 (UL), predecessor (i+1,j+1), clockwise -> UR (R3)
        f = [0] * sz
        Rc = R3
        for i in range(n - 1, -1, -1):
            base = i * m
            for j in range(m - 1, -1, -1):
                idx = base + j
                best = 0
                if i + 1 < n and j + 1 < m:
                    p = idx + m + 1
                    fo = f[p]
                    if fo == 0:
                        fo = 1 if g[p] == 1 else 0
                    if fo and g[idx] == nxt[g[p]]:
                        best = fo + 1
                f[idx] = best
                if best:
                    tot = best + Rc[idx] - 1
                    if tot > ans: ans = tot

        # d = 3 (UR), predecessor (i+1,j-1), clockwise -> DR (R0)
        f = [0] * sz
        Rc = R0
        for i in range(n - 1, -1, -1):
            base = i * m
            for j in range(m):
                idx = base + j
                best = 0
                if i + 1 < n and j > 0:
                    p = idx + m - 1
                    fo = f[p]
                    if fo == 0:
                        fo = 1 if g[p] == 1 else 0
                    if fo and g[idx] == nxt[g[p]]:
                        best = fo + 1
                f[idx] = best
                if best:
                    tot = best + Rc[idx] - 1
                    if tot > ans: ans = tot

        return ans