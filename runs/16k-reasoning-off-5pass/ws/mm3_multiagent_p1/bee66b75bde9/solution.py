import sys

def solve():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    B = []
    W = []
    cols = set()
    for _ in range(M):
        x, y, c = input().split()
        x = int(x)
        y = int(y)
        if c == 'B':
            B.append((x, y))
        else:
            W.append((x, y))
        cols.add(y)
    
    # Compress columns
    sorted_cols = sorted(cols)
    col_to_idx = {c: i+1 for i, c in enumerate(sorted_cols)}  # 1-based
    size = len(sorted_cols) + 2
    
    # First pass: top-down
    B.sort(key=lambda p: (p[0], p[1]))
    W.sort(key=lambda p: (p[0], p[1]))
    
    bit = [0] * size
    def update(i, v=1):
        while i < size:
            bit[i] += v
            i += i & -i
    def query(i):
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s
    
    w_ptr = 0
    for x, y in B:
        idx = col_to_idx[y]
        while w_ptr < len(W) and W[w_ptr][0] <= x:
            wy = W[w_ptr][1]
            update(col_to_idx[wy])
            w_ptr += 1
        if query(idx) > 0:
            print("No")
            return
    
    # Second pass: bottom-up
    B.sort(key=lambda p: (-p[0], -p[1]))
    W.sort(key=lambda p: (-p[0], -p[1]))
    
    bit = [0] * size
    b_ptr = 0
    for x, y in W:
        idx = col_to_idx[y]
        while b_ptr < len(B) and B[b_ptr][0] >= x:
            by = B[b_ptr][1]
            update(col_to_idx[by])
            b_ptr += 1
        # Query suffix sum from idx to end
        total = query(size - 1)
        prefix = query(idx - 1)
        if total - prefix > 0:
            print("No")
            return
    
    print("Yes")

if __name__ == "__main__":
    solve()