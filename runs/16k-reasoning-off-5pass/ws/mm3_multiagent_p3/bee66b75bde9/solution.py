import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    rows_with_B = set()
    cols_with_B = set()
    W_cells = []
    for _ in range(M):
        x = int(next(it))
        y = int(next(it))
        c = next(it)
        if c == 'B':
            rows_with_B.add(x)
            cols_with_B.add(y)
        else:  # 'W'
            W_cells.append((x, y))
    for (i, j) in W_cells:
        if i in rows_with_B and j in cols_with_B:
            print("No")
            return
    print("Yes")

if __name__ == "__main__":
    solve()