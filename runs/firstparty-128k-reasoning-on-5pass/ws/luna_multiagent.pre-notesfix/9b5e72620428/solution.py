import sys
from collections import Counter, defaultdict


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    A = data[1:1 + n]
    B = data[1 + n:1 + 2 * n]

    fixed_a = [x for x in A if x != -1]
    fixed_b = [x for x in B if x != -1]

    p = len(fixed_a)
    m = len(fixed_b)

    # At most N - m fixed A-values can be placed in positions
    # whose B-value was originally unknown.
    k = max(0, p + m - n)

    if k == 0:
        print("Yes")
        return

    count_a = Counter(fixed_a)
    count_b = Counter(fixed_b)

    maximum_fixed = max(max(fixed_a, default=0), max(fixed_b, default=0))

    # For each possible common sum S, accumulate the maximum number
    # of exact matches between fixed A-values and fixed B-values.
    match_count = defaultdict(int)

    for a, ca in count_a.items():
        for b, cb in count_b.items():
            match_count[a + b] += min(ca, cb)

    for s, matches in match_count.items():
        if s >= maximum_fixed and matches >= k:
            print("Yes")
            return

    print("No")


if __name__ == "__main__":
    solve()