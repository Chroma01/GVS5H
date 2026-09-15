import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    P = list(map(int, data[1:n + 1]))

    # Fenwick tree over N slots; tree[i] = lowbit(i) means all slots are empty (value 1).
    tree = [0] * (n + 1)
    for i in range(1, n + 1):
        tree[i] = i & (-i)

    ans = [0] * (n + 1)
    LOG = 1 << (n.bit_length() - 1)  # highest power of two <= n

    # Place values N, N-1, ..., 1 into the P_i-th empty slot.
    P_rev = P[::-1]
    for idx in range(n):
        i = n - idx
        k = P_rev[idx]

        # Find smallest slot with prefix sum (# empty) >= k via binary lifting.
        pos = 0
        rem = k
        bit = LOG
        while bit:
            nxt = pos + bit
            if nxt <= n and tree[nxt] < rem:
                rem -= tree[nxt]
                pos = nxt
            bit >>= 1
        slot = pos + 1
        ans[slot] = i

        # Mark slot occupied (remove 1 from Fenwick).
        j = slot
        while j <= n:
            tree[j] -= 1
            j += j & -j

    sys.stdout.write(' '.join(map(str, ans[1:])) + '\n')

main()