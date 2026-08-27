from functools import lru_cache

MAX_SUM = 81
CAP2, CAP3, CAP5, CAP7 = 6, 4, 2, 2
DIGIT_FACTORS = [
    (0, 0, 0, 0),  # 0
    (0, 0, 0, 0),  # 1
    (1, 0, 0, 0),  # 2
    (0, 1, 0, 0),  # 3
    (2, 0, 0, 0),  # 4
    (0, 0, 1, 0),  # 5
    (1, 1, 0, 0),  # 6
    (0, 0, 0, 1),  # 7
    (3, 0, 0, 0),  # 8
    (0, 2, 0, 0),  # 9
]


def _build_good():
    good = [
        [
            [
                [
                    [False] * (CAP7 + 1)
                    for _ in range(CAP5 + 1)
                ]
                for _ in range(CAP3 + 1)
            ]
            for _ in range(CAP2 + 1)
        ]
        for _ in range(MAX_SUM + 1)
    ]
    for s in range(1, MAX_SUM + 1):
        for e2 in range(CAP2 + 1):
            p2 = 1 << e2
            for e3 in range(CAP3 + 1):
                p = p2 * (3 ** e3)
                for e5 in range(CAP5 + 1):
                    p5 = p * (5 ** e5)
                    for e7 in range(CAP7 + 1):
                        good[s][e2][e3][e5][e7] = (p5 * (7 ** e7)) % s == 0
    return good


GOOD = _build_good()


class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        good = GOOD
        factors = DIGIT_FACTORS
        cap2, cap3, cap5, cap7 = CAP2, CAP3, CAP5, CAP7

        def count_upto(n: int) -> int:
            if n <= 0:
                return 0

            digits = list(map(int, str(n)))
            m = len(digits)

            suffix = [0] * (m + 1)
            for i in range(m - 1, -1, -1):
                suffix[i] = suffix[i + 1] * 10 + digits[i]

            pow10 = [1] * (m + 1)
            for i in range(1, m + 1):
                pow10[i] = pow10[i - 1] * 10

            @lru_cache(maxsize=None)
            def dfs(pos: int, tight: bool, started: bool, s: int,
                    e2: int, e3: int, e5: int, e7: int) -> int:
                if pos == m:
                    if not started:
                        return 0
                    return 1 if good[s][e2][e3][e5][e7] else 0

                limit = digits[pos] if tight else 9
                rem = m - pos - 1
                total = 0

                for d in range(limit + 1):
                    ntight = tight and (d == limit)

                    if not started:
                        if d == 0:
                            total += dfs(pos + 1, ntight, False, s, e2, e3, e5, e7)
                        else:
                            f2, f3, f5, f7 = factors[d]
                            ne2 = e2 + f2
                            if ne2 > cap2:
                                ne2 = cap2
                            ne3 = e3 + f3
                            if ne3 > cap3:
                                ne3 = cap3
                            ne5 = e5 + f5
                            if ne5 > cap5:
                                ne5 = cap5
                            ne7 = e7 + f7
                            if ne7 > cap7:
                                ne7 = cap7
                            total += dfs(pos + 1, ntight, True, s + d, ne2, ne3, ne5, ne7)
                    else:
                        if d == 0:
                            if tight and digits[pos] == 0:
                                total += suffix[pos + 1] + 1
                            else:
                                total += pow10[rem]
                        else:
                            f2, f3, f5, f7 = factors[d]
                            ne2 = e2 + f2
                            if ne2 > cap2:
                                ne2 = cap2
                            ne3 = e3 + f3
                            if ne3 > cap3:
                                ne3 = cap3
                            ne5 = e5 + f5
                            if ne5 > cap5:
                                ne5 = cap5
                            ne7 = e7 + f7
                            if ne7 > cap7:
                                ne7 = cap7
                            total += dfs(pos + 1, ntight, True, s + d, ne2, ne3, ne5, ne7)

                return total

            return dfs(0, True, False, 0, 0, 0, 0, 0)

        return count_upto(r) - count_upto(l - 1)


if __name__ == "__main__":
    sol = Solution()
    assert sol.beautifulNumbers(10, 20) == 2
    assert sol.beautifulNumbers(1, 15) == 10

    def brute_count(left: int, right: int) -> int:
        cnt = 0
        for x in range(left, right + 1):
            s = 0
            p = 1
            y = x
            while y:
                d = y % 10
                s += d
                p *= d
                y //= 10
            if p % s == 0:
                cnt += 1
        return cnt

    for left in range(1, 200, 31):
        right = min(left + 40, 200)
        assert sol.beautifulNumbers(left, right) == brute_count(left, right)