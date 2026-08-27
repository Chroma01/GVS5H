import sys
from collections import defaultdict

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    N = int(input_data[idx]); idx += 1
    M = int(input_data[idx]); idx += 1
    
    # a_row[i] = max y for B cells in row i (default 0)
    # b_row[i] = min (y-1) for W cells in row i (default N)
    a_row = defaultdict(int)
    b_row = defaultdict(lambda: N)
    # Similarly for columns
    a_col = defaultdict(int)  # c_j
    b_col = defaultdict(lambda: N)  # d_j
    
    cells = []
    for _ in range(M):
        x = int(input_data[idx]); idx += 1
        y = int(input_data[idx]); idx += 1
        c = input_data[idx]; idx += 1
        cells.append((x, y, c))
        if c == 'B':
            if y > a_row[x]:
                a_row[x] = y
            if x > a_col[y]:
                a_col[y] = x
        else:  # W
            if y - 1 < b_row[x]:
                b_row[x] = y - 1
            if x - 1 < b_col[y]:
                b_col[y] = x - 1
    
    # Check row constraints
    rows_in_constraints = set(a_row.keys()) | set(b_row.keys())
    for r in rows_in_constraints:
        if a_row[r] > b_row[r]:
            print("No")
            return
    
    # Check column constraints
    cols_in_constraints = set(a_col.keys()) | set(b_col.keys())
    for c in cols_in_constraints:
        if a_col[c] > b_col[c]:
            print("No")
            return
    
    # Check W cells: not (a_row[x] >= y and a_col[y] >= x)
    for x, y, c in cells:
        if c == 'W':
            if a_row[x] >= y and a_col[y] >= x:
                print("No")
                return
    
    print("Yes")

if __name__ == "__main__":
    solve()