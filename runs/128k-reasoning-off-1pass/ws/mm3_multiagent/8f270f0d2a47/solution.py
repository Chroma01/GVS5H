from collections import defaultdict

# Precompute suffix counts for no-zero digit sequences (digits 1-9)
_suffix_counts = [defaultdict(int) for _ in range(10)]
_suffix_counts[0][(1, 0)] = 1
for k in range(1, 10):
    cur = defaultdict(int)
    prev = _suffix_counts[k - 1]
    for (p, s), cnt in prev.items():
        for d in range(1, 10):
            cur[(p * d, s + d)] += cnt
    _suffix_counts[k] = cur

# Group suffix counts by sum for efficient iteration in the DP
_suffix_by_sum = [defaultdict(list) for _ in range(10)]
for k in range(10):
    for (p, s), cnt in _suffix_counts[k].items():
        _suffix_by_sum[k][s].append((p, cnt))

# Precompute the number of beautiful no-zero numbers for each exact length
_beautiful_by_length = [0] * 10
for k in range(1, 10):
    total = 0
    for (p, s), cnt in _suffix_counts[k].items():
        if p % s == 0:
            total += cnt
    _beautiful_by_length[k] = total


def _count_beautiful_no_zero(N):
    """Count beautiful numbers with no zero digit in [1, N]."""
    if N <= 0:
        return 0
    s = str(N)
    d = len(s)
    ans = 0
    # Add all beautiful no-zero numbers with fewer digits than N
    for k in range(1, d):
        ans += _beautiful_by_length[k]

    P = 1
    S = 0
    for i in range(d):
        digit = int(s[i])
        # Less-than branches: choose digit x < digit for this position
        for x in range(1, digit):
            remaining = d - 1 - i
            M_base = S + x
            # Iterate over suffix entries grouped by sum for efficiency
            for su, lst in _suffix_by_sum[remaining].items():
                M = M_base + su
                if M == 0:
                    continue
                Px_mod = (P * x) % M
                for p, cnt in lst:
                    if (Px_mod * (p % M)) % M == 0:
                        ans += cnt
        # Tight branch: choose digit = digit
        if digit == 0:
            break
        P *= digit
        S += digit
        if i == d - 1:
            # Check the full number
            if P % S == 0:
                ans += 1
    return ans


def _count_no_zero(N):
    """Count positive integers in [1, N] with no zero digit."""
    if N <= 0:
        return 0
    s = str(N)
    d = len(s)
    ans = 0
    # Add all no-zero numbers with fewer digits
    for k in range(1, d):
        ans += 9 ** k

    tight = True
    for i in range(d):
        digit = int(s[i])
        if tight:
            # Less-than branches: digits 1 to digit-1
            ans += (digit - 1) * 9 ** (d - 1 - i)
            if digit == 0:
                tight = False
                break
        else:
            # Not tight: remaining positions can be any digit 1-9
            ans += 9 ** (d - i)
            break
    if tight:
        ans += 1
    return ans


def _beautiful_count(N):
    """Count beautiful numbers in [1, N]."""
    if N <= 0:
        return 0
    # Numbers with at least one zero digit are all beautiful
    zero_count = N - _count_no_zero(N)
    # Add no-zero numbers that are beautiful
    return zero_count + _count_beautiful_no_zero(N)


class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        return _beautiful_count(r) - _beautiful_count(l - 1)