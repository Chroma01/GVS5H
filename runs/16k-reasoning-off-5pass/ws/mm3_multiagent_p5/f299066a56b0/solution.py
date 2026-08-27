import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    a = list(map(int, data[1:1+n]))
    # a is already sorted non-decreasing per problem statement
    i = 0  # pointer for top (smaller) mochi
    j = 0  # pointer for bottom (larger) mochi
    k = 0  # count of kagamimochi
    while i < n and j < n:
        # we want the smallest i such that a[i] * 2 > a[j]
        # while the condition holds, we could pair, but we keep the smallest
        # feasible top unused until we need it.
        if i == j:
            # top and bottom cannot be the same mochi
            j += 1
            continue
        if a[i] * 2 <= a[j]:
            # valid pair, use it
            k += 1
            i += 1
            j += 1
        else:
            # a[i] is too large to be a top for this bottom;
            # try a larger bottom
            j += 1
    print(k)

if __name__ == "__main__":
    solve()