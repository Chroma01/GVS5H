from typing import List

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0

        n, m = len(grid), len(grid[0])
        W = m + 2
        size = (n + 2) * W

        # Padded flat grid. Border cells are never scanned; their DP values stay 0.
        flat = [0] * size
        for r in range(n):
            start = (r + 1) * W + 1
            flat[start:start + m] = grid[r]

        # Directions in clockwise order:
        # 0: down-right, 1: down-left, 2: up-left, 3: up-right
        delta = (W + 1, W - 1, -W - 1, -W + 1)

        # Forward scan orders for incoming straight runs:
        # the previous cell in the direction is already processed.
        forward_rows = (
            range(1, n + 1),
            range(1, n + 1),
            range(n, 0, -1),
            range(n, 0, -1),
        )
        forward_cols = (
            range(1, m + 1),
            range(m, 0, -1),
            range(m, 0, -1),
            range(1, m + 1),
        )

        # Reverse scan orders for outgoing straight runs:
        # the next cell along the direction is already processed.
        reverse_rows = (
            range(n, 0, -1),
            range(n, 0, -1),
            range(1, n + 1),
            range(1, n + 1),
        )
        reverse_cols = (
            range(m, 0, -1),
            range(1, m + 1),
            range(1, m + 1),
            range(m, 0, -1),
        )

        ans = 0

        for d_out in range(4):
            # Incoming direction is counterclockwise from d_out,
            # so turning clockwise from d_in reaches d_out.
            d_in = (d_out - 1) % 4
            dout_delta = delta[d_out]

            # out0[idx]: max extra cells starting at idx in direction d_out
            #            when the next required value is 0.
            # out2[idx]: max extra cells starting at idx in direction d_out
            #            when the next required value is 2.
            out0 = [0] * size
            out2 = [0] * size

            for r in reverse_rows[d_out]:
                base = r * W
                for c in reverse_cols[d_out]:
                    idx = base + c
                    val = flat[idx]
                    if val == 0:
                        out0[idx] = 1 + out2[idx + dout_delta]
                    elif val == 2:
                        out2[idx] = 1 + out0[idx + dout_delta]

            # in_odd[idx]: longest valid straight prefix ending at idx
            #              in direction d_in with odd length.
            # in_even[idx]: longest valid straight prefix ending at idx
            #               in direction d_in with even length.
            in_odd = [0] * size
            in_even = [0] * size
            din_delta = delta[d_in]

            for r in forward_rows[d_in]:
                base = r * W
                for c in forward_cols[d_in]:
                    idx = base + c
                    val = flat[idx]

                    if val == 1:
                        in_odd[idx] = 1
                        cand = 1 + out2[idx + dout_delta]
                        if cand > ans:
                            ans = cand

                    elif val == 2:
                        prev_len = in_odd[idx - din_delta]
                        if prev_len:
                            le = prev_len + 1
                            in_even[idx] = le
                            cand = le + out0[idx + dout_delta]
                            if cand > ans:
                                ans = cand

                    elif val == 0:
                        prev_len = in_even[idx - din_delta]
                        if prev_len:
                            lo = prev_len + 1
                            in_odd[idx] = lo
                            cand = lo + out2[idx + dout_delta]
                            if cand > ans:
                                ans = cand

        return ans


if __name__ == "__main__":
    tests = [
        (
            [
                [2, 2, 1, 2, 2],
                [2, 0, 2, 2, 0],
                [2, 0, 1, 1, 0],
                [1, 0, 2, 2, 2],
                [2, 0, 0, 2, 2],
            ],
            5,
        ),
        (
            [
                [2, 2, 2, 2, 2],
                [2, 0, 2, 2, 0],
                [2, 0, 1, 1, 0],
                [1, 0, 2, 2, 2],
                [2, 0, 0, 2, 2],
            ],
            4,
        ),
        (
            [
                [1, 2, 2, 2, 2],
                [2, 2, 2, 2, 0],
                [2, 0, 0, 0, 0],
                [0, 0, 2, 2, 2],
                [2, 0, 0, 2, 0],
            ],
            5,
        ),
        ([[1]], 1),
    ]

    sol = Solution()
    for i, (grid, expected) in enumerate(tests, 1):
        print(f"Sample {i}: {'PASS' if sol.lenOfVDiagonal(grid) == expected else 'FAIL'}")