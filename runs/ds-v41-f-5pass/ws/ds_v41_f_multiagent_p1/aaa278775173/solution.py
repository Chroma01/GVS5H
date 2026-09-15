from typing import List

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        size = n * m

        # Clockwise diagonal cycle: turn is d -> (d+1)%4
        # 0: down-right (+1,+1)
        # 1: down-left  (+1,-1)
        # 2: up-left    (-1,-1)
        # 3: up-right   (-1,+1)
        DR = (1, 1, -1, -1)
        DC = (1, -1, -1, 1)

        # Sequence 1,2,0,2,0,...  nxt[v] = required following value
        #   nxt[0] = 2 (after 0 comes 2)
        #   nxt[1] = 2 (after 1 comes 2)
        #   nxt[2] = 0 (after 2 comes 0)
        nxt = (2, 2, 0)

        # Flatten grid for cache-friendly indexing
        flat = [grid[r][c] for r in range(n) for c in range(m)]

        # f[d][i] = longest alternating run STARTING at cell i going direction d
        f = [[0] * size for _ in range(4)]
        for d in range(4):
            dr = DR[d]
            dc = DC[d]
            fd = f[d]
            step = dr * m + dc
            r_range = range(n - 1, -1, -1) if dr > 0 else range(n)
            c_range = range(m - 1, -1, -1) if dc > 0 else range(m)
            for r in r_range:
                base = r * m
                for c in c_range:
                    i = base + c
                    rr = r + dr
                    cc = c + dc
                    if 0 <= rr < n and 0 <= cc < m and flat[i + step] == nxt[flat[i]]:
                        fd[i] = 1 + fd[i + step]
                    else:
                        fd[i] = 1

        # g[d][i] = longest alternating run ENDING at cell i arriving via
        # direction d that STARTS at a value-1 cell; 0 if unreachable.
        g = [[0] * size for _ in range(4)]
        for d in range(4):
            dr = DR[d]
            dc = DC[d]
            gd = g[d]
            step = dr * m + dc
            # predecessor is (r-dr, c-dc) -> opposite sweep order vs forward
            r_range = range(n) if dr > 0 else range(n - 1, -1, -1)
            c_range = range(m) if dc > 0 else range(m - 1, -1, -1)
            for r in r_range:
                base = r * m
                for c in c_range:
                    i = base + c
                    if flat[i] == 1:
                        gd[i] = 1
                    else:
                        pr = r - dr
                        pc = c - dc
                        if 0 <= pr < n and 0 <= pc < m:
                            j = i - step
                            gp = gd[j]
                            if gp > 0 and flat[i] == nxt[flat[j]]:
                                gd[i] = gp + 1
                            # otherwise stays 0

        best = 0

        # No-turn segments (also covers single value-1 cell).
        for r in range(n):
            base = r * m
            for c in range(m):
                i = base + c
                if flat[i] == 1:
                    for d in range(4):
                        v = f[d][i]
                        if v > best:
                            best = v

        # V-shape: turn clockwise at apex i.
        # incoming arm: g[d][i]  (ends at apex, starts at a 1)
        # outgoing arm: f[(d+1)%4][i] (starts at apex)
        for d in range(4):
            gd = g[d]
            fo = f[(d + 1) % 4]
            for i in range(size):
                inc = gd[i]
                if inc > 0:
                    total = inc + fo[i] - 1  # apex counted once
                    if total > best:
                        best = total

        return best