import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    P = list(map(int, data[1:1 + n]))

    # Fenwick tree over N slots, each initially empty (value 1).
    # O(N) build: tree[i] = i & -i holds the count of ones in (i - lowbit(i), i].
    tree = [0] * (n + 1)
    for i in range(1, n + 1):
        tree[i] = i & (-i)

    ans = [0] * (n + 1)
    top = 1 << (n.bit_length() - 1)  # highest power of two <= n

    # Process insertions in reverse. When only 1..i existed, i was placed at
    # rank P_i; in the final array its position is the P_i-th still-empty slot.
    for idx in range(n - 1, -1, -1):
        k = P[idx]
        pos = 0
        bit = top
        # Binary lifting: smallest index with prefix sum >= k (the k-th empty slot).
        while bit:
            nxt = pos + bit
            if nxt <= n and tree[nxt] < k:
                pos = nxt
                k -= tree[nxt]
            bit >>= 1
        slot = pos + 1
        ans[slot] = idx + 1
        # Remove this slot (set its value from 1 to 0).
        while slot <= n:
            tree[slot] -= 1
            slot += slot & (-slot)

    sys.stdout.write(' '.join(map(str, ans[1:])))

main()