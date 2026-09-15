from functools import lru_cache


@lru_cache(maxsize=None)
def _free_count(rem: int, started: bool, digit_sum: int, digit_product: int) -> int:
    """
    Count beautiful completions when the remaining `rem` digits are unrestricted.
    """
    if rem == 0:
        return 1 if started and digit_sum > 0 and digit_product % digit_sum == 0 else 0

    # Once a real zero digit has appeared, every suffix keeps product 0.
    # Since the number has started, its digit sum is positive, so all suffixes work.
    if started and digit_product == 0:
        return 10 ** rem

    total = 0
    for d in range(10):
        if not started:
            if d == 0:
                total += _free_count(rem - 1, False, 0, 1)
            else:
                total += _free_count(rem - 1, True, d, d)
        else:
            new_sum = digit_sum + d
            if d == 0 or digit_product == 0:
                new_product = 0
            else:
                new_product = digit_product * d
            total += _free_count(rem - 1, True, new_sum, new_product)

    return total


def _count_up_to(n: int) -> int:
    """
    Count beautiful positive integers in [1, n].
    """
    if n <= 0:
        return 0

    digits = tuple(map(int, str(n)))
    m = len(digits)

    def tight_dfs(pos: int, started: bool, digit_sum: int, digit_product: int) -> int:
        if pos == m:
            return 1 if started and digit_sum > 0 and digit_product % digit_sum == 0 else 0

        limit = digits[pos]
        total = 0

        for d in range(limit + 1):
            if not started:
                if d == 0:
                    next_started = False
                    next_sum = 0
                    next_product = 1
                else:
                    next_started = True
                    next_sum = d
                    next_product = d
            else:
                next_started = True
                next_sum = digit_sum + d
                if d == 0 or digit_product == 0:
                    next_product = 0
                else:
                    next_product = digit_product * d

            if d < limit:
                total += _free_count(m - pos - 1, next_started, next_sum, next_product)
            else:
                total += tight_dfs(pos + 1, next_started, next_sum, next_product)

        return total

    return tight_dfs(0, False, 0, 1)


class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        return _count_up_to(r) - _count_up_to(l - 1)