import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    P = list(map(int, data[1:1 + n]))

    # Fenwick tree over slots 1..n; tree prefix sum = number of EMPTY slots.
    # Initially all slots empty: arr[i] = 1, so tree[i] = i & -i (O(n) build).
    tree = [0] * (n + 1)
    for i in range(1, n + 1):
        tree[i] = i & -i

    # Highest power of two <= n (starting bitmask for binary lifting).
    log = 1
    while log * 2 <= n:
        log *= 2

    def find_kth(k):
        # Smallest index idx such that prefix_sum(idx) >= k (1-indexed).
        idx = 0
        bitmask = log
        while bitmask:
            nxt = idx + bitmask
            if nxt <= n and tree[nxt] < k:
                idx = nxt
                k -= tree[nxt]
            bitmask >>= 1
        return idx + 1

    ans = [0] * n
    # Process insertions in reverse. When placing value i, all values > i are
    # already in their final slots. The elements that will precede i are exactly
    # the P_i - 1 smaller values, which will occupy the first P_i - 1 empty
    # slots; hence i goes into the P_i-th empty slot from the left.
    for i in range(n, 0, -1):
        pos = find_kth(P[i - 1])   # P_i-th empty slot
        ans[pos - 1] = i
        # mark slot occupied: empty count decreases by 1
        j = pos
        while j <= n:
            tree[j] -= 1
            j += j & -j

    sys.stdout.write(' '.join(map(str, ans)) + '\n')

main()