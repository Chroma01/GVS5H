import sys

# Module-level memo: non-tight DP states depend only on (remaining free digits,
# started flag, running digit sum, running digit product), never on the bound N.
# Caching it globally makes repeated calls (many test cases) essentially free.
_MEMO = {}


class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        memo = _MEMO

        def dfs(rem: int, started: bool, s: int, p: int) -> int:
            """Number of ways to fill `rem` completely free digits (0..9 each)
            so that the whole number is beautiful, given the prefix already has
            digit-sum s and digit-product p (`started` False => prefix is all
            leading zeros, i.e. no significant digit yet)."""
            if rem == 0:
                # 'started' False here means the number is 0 -> not counted.
                return 1 if (started and p % s == 0) else 0
            if started and p == 0:
                # product already 0 -> 0 % (positive sum) == 0 for every suffix
                return 10 ** rem
            key = (rem, started, s, p)
            v = memo.get(key)
            if v is not None:
                return v
            if not started:
                # a 0 here is still a leading zero
                total = dfs(rem - 1, False, 0, 1)
                for d in range(1, 10):
                    total += dfs(rem - 1, True, d, d)
            else:
                total = dfs(rem - 1, True, s, 0)  # digit 0 -> product becomes 0
                for d in range(1, 10):
                    total += dfs(rem - 1, True, s + d, p * d)
            memo[key] = total
            return total

        def count(N: int) -> int:
            """Beautiful numbers in [1, N]."""
            if N <= 0:
                return 0
            ds = list(map(int, str(N)))
            n = len(ds)
            total = 0
            s = 0
            p = 1
            started = False
            for i in range(n):
                dig = ds[i]
                rem = n - i - 1
                for d in range(dig):
                    if not started and d == 0:
                        total += dfs(rem, False, 0, 1)
                    else:
                        total += dfs(rem, True, s + d, p * d)
                # follow the tight branch with digit == dig
                if started or dig != 0:
                    started = True
                    s += dig
                    p *= dig
            # N itself (N >= 1 so `started` is True here)
            if started and p % s == 0:
                total += 1
            return total

        return count(r) - count(l - 1)