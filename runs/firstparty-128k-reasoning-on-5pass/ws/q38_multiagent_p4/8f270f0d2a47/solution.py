from functools import lru_cache

CAP2, CAP3, CAP5, CAP7 = 6, 4, 2, 2
MAX_SUM = 81

B3 = CAP2 + 1
B5 = B3 * (CAP3 + 1)
B7 = B5 * (CAP5 + 1)
MAX_CODE = B7 * (CAP7 + 1)


def _encode(e2, e3, e5, e7):
    return e2 + B3 * e3 + B5 * e5 + B7 * e7


_EXP = [None] * MAX_CODE
for code in range(MAX_CODE):
    e2 = code % B3
    e3 = (code // B3) % (CAP3 + 1)
    e5 = (code // B5) % (CAP5 + 1)
    e7 = code // B7
    _EXP[code] = (e2, e3, e5, e7)


_DIGIT_ADD = [
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


_NEXT = [[0] * 10 for _ in range(MAX_CODE)]
for code in range(MAX_CODE):
    e2, e3, e5, e7 = _EXP[code]
    for d in range(1, 10):
        a2, a3, a5, a7 = _DIGIT_ADD[d]
        _NEXT[code][d] = _encode(
            min(CAP2, e2 + a2),
            min(CAP3, e3 + a3),
            min(CAP5, e5 + a5),
            min(CAP7, e7 + a7),
        )


_REQ = [None] * (MAX_SUM + 1)
for s in range(1, MAX_SUM + 1):
    x = s
    e2 = e3 = e5 = e7 = 0
    while x % 2 == 0:
        e2 += 1
        x //= 2
    while x % 3 == 0:
        e3 += 1
        x //= 3
    while x % 5 == 0:
        e5 += 1
        x //= 5
    while x % 7 == 0:
        e7 += 1
        x //= 7
    if x == 1:
        _REQ[s] = (e2, e3, e5, e7)


_GOOD = [bytearray(MAX_CODE) for _ in range(MAX_SUM + 1)]
for s in range(1, MAX_SUM + 1):
    req = _REQ[s]
    if req is None:
        continue
    r2, r3, r5, r7 = req
    for code in range(MAX_CODE):
        e2, e3, e5, e7 = _EXP[code]
        if e2 >= r2 and e3 >= r3 and e5 >= r5 and e7 >= r7:
            _GOOD[s][code] = 1


class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        return self._count_up_to(r) - self._count_up_to(l - 1)

    def _count_up_to(self, n: int) -> int:
        if n <= 0:
            return 0

        digits = [ord(c) - 48 for c in str(n)]
        m = len(digits)

        suffix = [0] * (m + 1)
        for i in range(m - 1, -1, -1):
            suffix[i] = suffix[i + 1] * 10 + digits[i]

        pow10 = [1] * (m + 1)
        for i in range(1, m + 1):
            pow10[i] = pow10[i - 1] * 10

        next_code = _NEXT
        good = _GOOD

        @lru_cache(maxsize=None)
        def dp(pos: int, tight: bool, s: int, code: int) -> int:
            if pos == m:
                if s == 0:
                    return 0
                return good[s][code]

            limit = digits[pos] if tight else 9
            total = 0

            if s == 0:
                # Still in leading-zero region.
                total += dp(pos + 1, tight and limit == 0, 0, 0)
                for d in range(1, limit + 1):
                    total += dp(pos + 1, tight and d == limit, d, next_code[0][d])
            else:
                # A real zero makes the digit product 0, so every completion is beautiful.
                if tight and limit == 0:
                    total += suffix[pos + 1] + 1
                else:
                    total += pow10[m - pos - 1]

                for d in range(1, limit + 1):
                    total += dp(pos + 1, tight and d == limit, s + d, next_code[code][d])

            return total

        ans = dp(0, True, 0, 0)
        dp.cache_clear()
        return ans