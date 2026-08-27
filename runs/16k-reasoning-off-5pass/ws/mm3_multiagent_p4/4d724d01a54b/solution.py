import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    P = [int(next(it)) for _ in range(N)]
    
    class BIT:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)
        def update(self, idx, delta):
            while idx <= self.n:
                self.bit[idx] += delta
                idx += idx & -idx
        def query(self, idx):
            s = 0
            while idx > 0:
                s += self.bit[idx]
                idx -= idx & -idx
            return s
    
    bit = BIT(N)
    total = 0
    for i, v in enumerate(P, start=1):
        # number of elements <= v seen so far
        le = bit.query(v)
        L = (i - 1) - le
        cost = L * i - L * (L + 1) // 2
        total += cost
        bit.update(v, 1)
    
    print(total)

if __name__ == "__main__":
    solve()