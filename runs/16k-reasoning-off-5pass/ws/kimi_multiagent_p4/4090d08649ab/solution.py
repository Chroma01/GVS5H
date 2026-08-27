import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))

    # Part 1: sum over all subarrays of the number of distinct values.
    # Position i (1-indexed), previous occurrence p of the same value:
    # contributes (i - p) * (n - i + 1) subarrays where A_i is the first
    # occurrence of its value.
    last = [0] * (n + 2)
    distinct_sum = 0
    for i in range(1, n + 1):
        x = A[i - 1]
        p = last[x]
        distinct_sum += (i - p) * (n - i + 1)
        last[x] = i

    # Part 2: sum over v of the number of subarrays containing both v and v+1.
    # For fixed right endpoint R, # of L such that both v and v+1 appear in
    # A[L..R] equals min(last[v], last[v+1]) (0 if either unseen so far).
    # Maintain pair_min[v] = min(last[v], last[v+1]) and cur = sum of pair_min.
    # When last[x] is updated at position i, only pair_min[x-1] and pair_min[x]
    # can change. Add cur to the total at EVERY position R.
    last = [0] * (n + 2)
    pair_min = [0] * (n + 2)  # pair_min[v] meaningful for 1 <= v <= n-1
    cur = 0
    pair_sum = 0
    for i in range(1, n + 1):
        x = A[i - 1]
        last[x] = i
        # pair (x-1, x): pair_min[x-1] = min(last[x-1], i)
        if x - 1 >= 1:
            v = x - 1
            new = last[v] if last[v] < i else i
            cur += new - pair_min[v]
            pair_min[v] = new
        # pair (x, x+1): pair_min[x] = min(i, last[x+1])
        if x + 1 <= n:
            v = x
            lv = last[x + 1]
            new = lv if lv < i else i
            cur += new - pair_min[v]
            pair_min[v] = new
        pair_sum += cur

    print(distinct_sum - pair_sum)

main()