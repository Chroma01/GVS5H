from itertools import groupby


class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        runs = [len(list(g)) for _, g in groupby(s)]

        # cost for k == 1: string must fully alternate
        mism_a = 0  # vs "0101..."
        mism_b = 0  # vs "1010..."
        for i, ch in enumerate(s):
            if ch != ('0' if i % 2 == 0 else '1'):
                mism_a += 1
            if ch != ('1' if i % 2 == 0 else '0'):
                mism_b += 1
        cost1 = min(mism_a, mism_b)

        if cost1 <= numOps:
            return 1

        for k in range(2, n + 1):
            total = 0
            kk = k + 1
            for L in runs:
                total += L // kk
                if total > numOps:
                    break
            if total <= numOps:
                return k
        return n


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ("000001", 1, 2),
        ("0000", 2, 1),
        ("0101", 0, 1),
        ("0110", 1, 2),
        ("0000", 0, 4),
        ("1", 0, 1),
        ("01", 1, 1),
    ]
    for s, ops, exp in tests:
        got = sol.minLength(s, ops)
        print(s, ops, got, exp, "OK" if got == exp else "FAIL")