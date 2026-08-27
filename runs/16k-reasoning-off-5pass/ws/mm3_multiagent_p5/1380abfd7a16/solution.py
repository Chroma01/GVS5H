import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    P = [0] * (N + 1)  # 1-indexed
    for i in range(1, N + 1):
        P[i] = int(next(it))

    # Fenwick tree implementation
    class Fenwick:
        __slots__ = ('n', 'bit')
        def __init__(self, n: int):
            self.n = n
            self.bit = [0] * (n + 1)
            for i in range(1, n + 1):
                self.bit[i] += 1
                j = i + (i & -i)
                if j <= n:
                    self.bit[j] += self.bit[i]
        def add(self, idx: int, delta: int):
            n = self.n
            bit = self.bit
            while idx <= n:
                bit[idx] += delta
                idx += idx & -idx
        def find_kth(self, k: int) -> int:
            # find smallest idx such that prefix sum >= k (1 <= k <= total)
            bit = self.bit
            idx = 0
            bit_mask = 1 << (self.n.bit_length() - 1)
            while bit_mask:
                nxt = idx + bit_mask
                if nxt <= self.n and bit[nxt] < k:
                    k -= bit[nxt]
                    idx = nxt
                bit_mask >>= 1
            return idx + 1

    ft = Fenwick(N)
    ans = [0] * (N + 1)  # 1-indexed positions
    for i in range(N, 0, -1):
        pos = ft.find_kth(P[i])
        ans[pos] = i
        ft.add(pos, -1)

    # output 1..N
    out = ' '.join(str(ans[i]) for i in range(1, N + 1))
    sys.stdout.write(out)

if __name__ == "__main__":
    solve()