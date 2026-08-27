import sys
from collections import Counter

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    A = data[1:1 + n]
    B = data[1 + n:1 + 2 * n]

    fixed_a = [x for x in A if x != -1]
    fixed_b = [x for x in B if x != -1]

    count_a = Counter(fixed_a)
    count_b = Counter(fixed_b)

    unknown_a = n - len(fixed_a)
    known_b = len(fixed_b)

    # All known-B positions can be supplied by freely chosen A values.
    # The remaining fixed A values then fit in unknown-B positions.
    if known_b <= unknown_a:
        print("Yes")
        return

    needed_matches = known_b - unknown_a
    minimum_sum = max(max(fixed_a, default=0), max(fixed_b, default=0))

    matched_by_sum = {}

    for a, ca in count_a.items():
        for b, cb in count_b.items():
            s = a + b
            if s < minimum_sum:
                continue

            add = ca if ca < cb else cb
            total = matched_by_sum.get(s, 0) + add

            if total >= needed_matches:
                print("Yes")
                return

            matched_by_sum[s] = total

    print("No")

if __name__ == "__main__":
    solve()