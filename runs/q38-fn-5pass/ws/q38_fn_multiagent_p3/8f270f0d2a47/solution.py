from functools import lru_cache

class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count_up_to(n: int) -> int:
            if n <= 0:
                return 0

            digits = [int(ch) for ch in str(n)]
            L = len(digits)
            max_sum = 9 * L

            def req_for(x: int):
                v2 = v3 = v5 = v7 = 0

                while x % 2 == 0:
                    v2 += 1
                    x //= 2
                while x % 3 == 0:
                    v3 += 1
                    x //= 3
                while x % 5 == 0:
                    v5 += 1
                    x //= 5
                while x % 7 == 0:
                    v7 += 1
                    x //= 7

                if x != 1:
                    return None
                return (v2, v3, v5, v7)

            reqs = [None] * (max_sum + 1)
            cap2 = cap3 = cap5 = cap7 = 0

            for s in range(1, max_sum + 1):
                req = req_for(s)
                reqs[s] = req
                if req is not None:
                    cap2 = max(cap2, req[0])
                    cap3 = max(cap3, req[1])
                    cap5 = max(cap5, req[2])
                    cap7 = max(cap7, req[3])

            add = [(0, 0, 0, 0)] * 10
            for d in range(1, 10):
                x = d
                a2 = a3 = a5 = a7 = 0

                while x % 2 == 0:
                    a2 += 1
                    x //= 2
                while x % 3 == 0:
                    a3 += 1
                    x //= 3
                while x % 5 == 0:
                    a5 += 1
                    x //= 5
                while x % 7 == 0:
                    a7 += 1
                    x //= 7

                add[d] = (a2, a3, a5, a7)

            pow10 = [1] * (L + 1)
            for i in range(1, L + 1):
                pow10[i] = pow10[i - 1] * 10

            suffix = [0] * (L + 1)
            for i in range(L - 1, -1, -1):
                suffix[i] = suffix[i + 1] + digits[i] * pow10[L - i - 1]

            @lru_cache(maxsize=None)
            def dfs(
                pos: int,
                tight: bool,
                started: bool,
                s: int,
                e2: int,
                e3: int,
                e5: int,
                e7: int,
                zero: bool
            ) -> int:
                # Once a real zero digit appears, the digit product is 0.
                # Since the digit sum is positive, every completion is beautiful.
                if zero:
                    if not started:
                        return 0
                    if tight:
                        return suffix[pos] + 1
                    return pow10[L - pos]

                if pos == L:
                    if not started or s == 0:
                        return 0

                    req = reqs[s]
                    if req is None:
                        return 0

                    return 1 if (
                        e2 >= req[0] and
                        e3 >= req[1] and
                        e5 >= req[2] and
                        e7 >= req[3]
                    ) else 0

                limit = digits[pos] if tight else 9
                total = 0

                for d in range(limit + 1):
                    ntight = tight and (d == limit)

                    if not started:
                        if d == 0:
                            total += dfs(
                                pos + 1,
                                ntight,
                                False,
                                0, 0, 0, 0, 0,
                                False
                            )
                        else:
                            a2, a3, a5, a7 = add[d]
                            total += dfs(
                                pos + 1,
                                ntight,
                                True,
                                d,
                                a2, a3, a5, a7,
                                False
                            )
                    else:
                        if d == 0:
                            total += dfs(
                                pos + 1,
                                ntight,
                                True,
                                0, 0, 0, 0, 0,
                                True
                            )
                        else:
                            ns = s + d

                            ne2 = e2 + add[d][0]
                            ne3 = e3 + add[d][1]
                            ne5 = e5 + add[d][2]
                            ne7 = e7 + add[d][3]

                            if ne2 > cap2:
                                ne2 = cap2
                            if ne3 > cap3:
                                ne3 = cap3
                            if ne5 > cap5:
                                ne5 = cap5
                            if ne7 > cap7:
                                ne7 = cap7

                            total += dfs(
                                pos + 1,
                                ntight,
                                True,
                                ns,
                                ne2, ne3, ne5, ne7,
                                False
                            )

                return total

            return dfs(0, True, False, 0, 0, 0, 0, 0, False)

        return count_up_to(r) - count_up_to(l - 1)


if __name__ == "__main__":
    sol = Solution()
    tests = [
        (10, 20, 2),
        (1, 15, 10),
        (1, 1, 1),
        (10, 10, 1),
        (1, 100, 25),
    ]

    for l, r, expected in tests:
        got = sol.beautifulNumbers(l, r)
        if got != expected:
            print(f"SAMPLE TESTS FAIL l={l} r={r} expected={expected} got={got}")
            break
    else:
        print("SAMPLE TESTS PASS")