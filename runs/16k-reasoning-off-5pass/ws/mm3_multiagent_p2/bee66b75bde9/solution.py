import sys
from collections import defaultdict

def solve():
    data = sys.stdin.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    
    # row_max_black[i] = max column index of black in row i, -1 if none
    # row_min_white[i] = min column index of white in row i, N+1 if none
    row_max_black = defaultdict(lambda: -1)
    row_min_white = defaultdict(lambda: N + 1)
    
    # col_max_black[j] = max row index of black in col j, -1 if none
    # col_min_white[j] = min row index of white in col j, N+1 if none
    col_max_black = defaultdict(lambda: -1)
    col_min_white = defaultdict(lambda: N + 1)
    
    for _ in range(M):
        x = int(next(it))
        y = int(next(it))
        c = next(it)
        if c == 'B':
            if y > row_max_black[x]:
                row_max_black[x] = y
            if x > col_max_black[y]:
                col_max_black[y] = x
        else:  # W
            if y < row_min_white[x]:
                row_min_white[x] = y
            if x < col_min_white[y]:
                col_min_white[y] = x
    
    # Check rows
    for i in row_max_black:
        # if row has both black and white
        if row_max_black[i] != -1 and row_min_white[i] != N + 1:
            if row_max_black[i] >= row_min_white[i]:
                print("No")
                return
    for i in row_min_white:
        if row_max_black[i] != -1 and row_min_white[i] != N + 1:
            if row_max_black[i] >= row_min_white[i]:
                print("No")
                return
    
    # Check columns
    for j in col_max_black:
        if col_max_black[j] != -1 and col_min_white[j] != N + 1:
            if col_max_black[j] >= col_min_white[j]:
                print("No")
                return
    for j in col_min_white:
        if col_max_black[j] != -1 and col_min_white[j] != N + 1:
            if col_max_black[j] >= col_min_white[j]:
                print("No")
                return
    
    print("Yes")

if __name__ == "__main__":
    solve()