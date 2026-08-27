import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    P = list(map(int, data[1:1 + n]))

    # Fenwick tree over slots 1..N; 1 = free, 0 = occupied
    bit = [0] * (n + 1)
    for i in range(1, n + 1):
        bit[i] = i & (-i)

    # largest power of two <= n
    LOG = 1
    while LOG * 2 <= n:
        LOG *= 2

    def find_kth(k):
        # smallest idx such that prefix_sum(idx) >= k  (k >= 1)
        idx = 0
        step = LOG
        while step:
            nxt = idx + step
            if nxt <= n and bit[nxt] < k:
                k -= bit[nxt]
                idx = nxt
            step >>= 1
        return idx + 1

    def add(i, delta):
        while i <= n:
            bit[i] += delta
            i += i & (-i)

    ans = [0] * (n + 1)
    for i in range(n, 0, -1):
        pos = find_kth(P[i - 1])
        ans[pos] = i
        add(pos, -1)

    sys.stdout.write(' '.join(map(str, ans[1:])) + '\n')

main()