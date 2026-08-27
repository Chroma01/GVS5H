import sys
from bisect import bisect_right

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    # We need to track bounds for rows and columns.
    # LB[r] = max column index of a black cell in row r (0 if none)
    # UB[r] = min (column index of a white cell - 1) in row r (N if none)
    # Similarly for columns LB[c], UB[c].
    
    row_LB = {}
    row_UB = {}
    col_LB = {}
    col_UB = {}

    for _ in range(M):
        r = int(next(iterator))
        c = int(next(iterator))
        color = next(iterator)
        
        # Update Row r
        if color == 'B':
            if r not in row_LB or c > row_LB[r]:
                row_LB[r] = c
        else: # color == 'W'
            if r not in row_UB or c - 1 < row_UB[r]:
                row_UB[r] = c - 1

        # Update Col c
        if color == 'B':
            if c not in col_LB or r > col_LB[c]:
                col_LB[c] = r
        else: # color == 'W'
            if c not in col_UB or r - 1 < col_UB[c]:
                col_UB[c] = r - 1

    # Check basic validity: LB <= UB for all constrained rows/cols
    possible = True
    
    # Check rows
    for r in row_LB:
        ub = row_UB.get(r, N)
        if row_LB[r] > ub:
            possible = False
            break
    
    if possible:
        # Check cols
        for c in col_LB:
            ub = col_UB.get(c, N)
            if col_LB[c] > ub:
                possible = False
                break

    if possible:
        # Prepare prefix minimums for columns
        # We need min(UB[c]) for c <= K.
        # Only columns with UB[c] < N are relevant for the minimum (since N is the max possible).
        col_pairs = []
        for c, ub in col_UB.items():
            if ub < N:
                col_pairs.append((c, ub))
        col_pairs.sort(key=lambda x: x[0])
        
        prefix_min_col = []
        if col_pairs:
            current_min = col_pairs[0][1]
            prefix_min_col.append(current_min)
            for i in range(1, len(col_pairs)):
                current_min = min(current_min, col_pairs[i][1])
                prefix_min_col.append(current_min)
        
        # Prepare prefix minimums for rows
        row_pairs = []
        for r, ub in row_UB.items():
            if ub < N:
                row_pairs.append((r, ub))
        row_pairs.sort(key=lambda x: x[0])
        
        prefix_min_row = []
        if row_pairs:
            current_min = row_pairs[0][1]
            prefix_min_row.append(current_min)
            for i in range(1, len(row_pairs)):
                current_min = min(current_min, row_pairs[i][1])
                prefix_min_row.append(current_min)

        # Helper to get min UB for index <= K
        def get_min_ub_col(K):
            if K == 0:
                return N
            # Binary search for rightmost c <= K
            # col_pairs is sorted by c
            # We extract just the c values for bisect
            c_values = [p[0] for p in col_pairs]
            idx = bisect_right(c_values, K) - 1
            if idx < 0:
                return N
            return prefix_min_col[idx]

        def get_min_ub_row(K):
            if K == 0:
                return N
            r_values = [p[0] for p in row_pairs]
            idx = bisect_right(r_values, K) - 1
            if idx < 0:
                return N
            return prefix_min_row[idx]

        # Condition 3: For all r, if LB[r] > 0, min(UB[c] for c <= LB[r]) >= r
        for r in row_LB:
            limit = row_LB[r]
            min_ub = get_min_ub_col(limit)
            if min_ub < r:
                possible = False
                break

        if possible:
            # Condition 4: For all c, if LB[c] > 0, min(UB[r] for r <= LB[c]) >= c
            for c in col_LB:
                limit = col_LB[c]
                min_ub = get_min_ub_row(limit)
                if min_ub < c:
                    possible = False
                    break

    if possible:
        print("Yes")
    else:
        print("No")

if __name__ == '__main__':
    solve()