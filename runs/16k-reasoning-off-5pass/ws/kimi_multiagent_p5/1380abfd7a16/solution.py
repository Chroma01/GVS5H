import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    P = list(map(int, data[1:1 + n]))

    # Fenwick tree, initially all positions occupied (bit[i] = i & -i)
    bit = [0] * (n + 1)
    for i in range(1, n + 1):
        bit[i] = i & -i

    # Largest power of two <= n
    LOG = 1
    while LOG * 2 <= n:
        LOG *= 2

    ans = [0] * (n + 1)

    # Process elements in reverse: element i is the P_i-th occupied position
    for i in range(n, 0, -1):
        k = P[i - 1]
        # Binary lifting: find smallest idx with prefix sum >= k
        idx = 0
        step = LOG
        while step:
            nxt = idx + step
            if nxt <= n and bit[nxt] < k:
                idx = nxt
                k -= bit[nxt]
            step >>= 1
        pos = idx + 1
        ans[pos] = i
        # Remove position pos
        j = pos
        while j <= n:
            bit[j] -= 1
            j += j & -j

    sys.stdout.write(' '.join(map(str, ans[1:])))

main()