import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    P = [int(next(it)) for _ in range(N)]

    # Fenwick tree (1-indexed) over values 1..N
    size = N + 2
    bit = [0] * size

    def add(idx, val):
        while idx < size:
            bit[idx] += val
            idx += idx & -idx

    def sum_(idx):
        s = 0
        while idx > 0:
            s += bit[idx]
            idx -= idx & -idx
        return s

    ans = 0
    for i, x in enumerate(P):
        # number of elements already seen (to the left) that are greater than x
        greater = i - sum_(x)
        ans += greater * (i + 1)
        add(x, 1)

    sys.stdout.write(str(ans))

if __name__ == "__main__":
    solve()