import sys

class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)
    
    def update(self, i, delta):
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i
    
    def query(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    idx = 0
    N = int(data[idx]); idx += 1
    P = list(map(int, data[idx:idx+N])); idx += N
    
    where = [0] * (N + 1)
    for i in range(N):
        where[P[i]] = i  # 0-indexed original position
    
    bit = FenwickTree(N)
    for i in range(1, N + 1):
        bit.update(i, 1)  # initially all positions are alive
    
    total_cost = 0
    for v in range(N, 0, -1):
        orig_idx = where[v]  # 0-indexed
        pos = bit.query(orig_idx + 1)  # 1-indexed position in compressed array
        # current size of the compressed array is v
        if pos < v:
            # sum of integers from pos to v-1
            cost = (pos + (v - 1)) * (v - pos) // 2
            total_cost += cost
        # remove v
        bit.update(orig_idx + 1, -1)
    
    print(total_cost)

if __name__ == "__main__":
    solve()