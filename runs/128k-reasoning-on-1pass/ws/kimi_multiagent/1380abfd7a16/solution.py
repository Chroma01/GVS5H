import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    P = list(map(int, data[1:1 + n]))

    # Fenwick tree over final positions; 1 means still empty.
    bit = [0] * (n + 1)
    for i in range(1, n + 1):
        bit[i] = i & -i  # all positions initially empty

    def find_kth(k: int) -> int:
        """Smallest index pos such that prefix_sum(pos) >= k."""
        idx = 0
        cur = 0
        step = 1 << (n.bit_length() - 1)
        while step:
            nxt = idx + step
            if nxt <= n and cur + bit[nxt] < k:
                idx = nxt
                cur += bit[nxt]
            step >>= 1
        return idx + 1

    def occupy(pos: int) -> None:
        x = pos
        while x <= n:
            bit[x] -= 1
            x += x & -x

    ans = [0] * (n + 1)
    for i in range(n, 0, -1):
        pos = find_kth(P[i - 1])
        ans[pos] = i
        occupy(pos)

    sys.stdout.write(" ".join(map(str, ans[1:])))

if __name__ == "__main__":
    main()