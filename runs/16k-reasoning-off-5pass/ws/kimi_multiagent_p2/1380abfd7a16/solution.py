import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    P = list(map(int, data[1:1 + n]))

    # Fenwick tree over positions 1..n, all slots initially empty (value 1)
    tree = [0] * (n + 1)
    for i in range(1, n + 1):
        tree[i] = i & (-i)  # O(n) build of all-ones BIT

    def add(i, delta):
        while i <= n:
            tree[i] += delta
            i += i & (-i)

    def find_kth(k):
        # smallest index idx such that prefix_sum(idx) >= k
        idx = 0
        bitmask = 1 << (n.bit_length() - 1)
        while bitmask:
            nxt = idx + bitmask
            if nxt <= n and tree[nxt] < k:
                idx = nxt
                k -= tree[nxt]
            bitmask >>= 1
        return idx + 1

    ans = [0] * (n + 1)
    for i in range(n, 0, -1):
        pos = find_kth(P[i - 1])  # P_i-th empty slot
        ans[pos] = i
        add(pos, -1)              # mark slot occupied

    sys.stdout.write(' '.join(map(str, ans[1:])) + '\n')

main()