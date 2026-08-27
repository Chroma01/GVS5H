import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    P = list(map(int, data[1:1 + n]))

    # Fenwick tree over positions 1..n, initially all slots free (value 1)
    bit = [0] * (n + 1)
    for i in range(1, n + 1):
        bit[i] = i & (-i)  # O(n) build: each position holds 1

    # largest power of two <= n
    log = 1
    while (log << 1) <= n:
        log <<= 1

    def find_kth(k):
        # smallest index idx such that prefix sum >= k (k is 1-indexed)
        idx = 0
        step = log
        while step:
            nxt = idx + step
            if nxt <= n and bit[nxt] < k:
                idx = nxt
                k -= bit[nxt]
            step >>= 1
        return idx + 1

    def add(i, delta):
        while i <= n:
            bit[i] += delta
            i += i & (-i)

    ans = [0] * (n + 1)
    for i in range(n, 0, -1):
        pos = find_kth(P[i - 1])  # P_i-th free slot
        ans[pos] = i
        add(pos, -1)              # mark slot used

    sys.stdout.write(' '.join(map(str, ans[1:])) + '\n')

main()