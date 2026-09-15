import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    P = list(map(int, data[1:1 + n]))

    # Fenwick tree over n slots, each slot initially "empty" (value 1).
    # tree[i] = i & (-i) is the correct base build for an all-ones array.
    tree = [0] * (n + 1)
    for i in range(1, n + 1):
        tree[i] = i & (-i)

    res = [0] * (n + 1)
    topbit = 1 << (n.bit_length() - 1)

    # Reconstruct in reverse: the last inserted element never moves again.
    for i in range(n, 0, -1):
        rem = P[i - 1]          # place i at the P_i-th still-empty slot
        pos = 0
        bit = topbit
        # Binary lifting to find smallest idx with prefix_sum >= rem.
        while bit:
            nxt = pos + bit
            if nxt <= n and tree[nxt] < rem:
                pos = nxt
                rem -= tree[nxt]
            bit >>= 1
        idx = pos + 1
        res[idx] = i
        # Mark slot idx used (remove one).
        j = idx
        while j <= n:
            tree[j] -= 1
            j += j & (-j)

    sys.stdout.write(' '.join(map(str, res[1:])))
    sys.stdout.write('\n')

main()