import sys

class Fenwick:
    """1‑based Fenwick tree for prefix sums."""
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx: int, delta: int) -> None:
        while idx <= self.n:
            self.bit[idx] += delta
            idx += idx & -idx

    def sum(self, idx: int) -> int:
        s = 0
        while idx:
            s += self.bit[idx]
            idx -= idx & -idx
        return s

def solve() -> None:
    input = sys.stdin.readline
    N = int(input())
    P = list(map(int, input().split()))
    # pos[value] = index (1‑based) of value in the permutation
    pos = [0] * (N + 1)
    for i, v in enumerate(P, start=1):
        pos[v] = i

    bit = Fenwick(N)
    ans = 0

    # Process values in increasing order
    for v in range(1, N + 1):
        # number of already processed (smaller) values to the left of v
        left_smaller = bit.sum(pos[v] - 1)
        # r(v) = number of smaller elements to the right of v
        r = (v - 1) - left_smaller
        # contribution of v to the total cost
        ans += r * v - r * (r + 1) // 2
        # insert v into the BIT
        bit.add(pos[v], 1)

    print(ans)

if __name__ == "__main__":
    solve()