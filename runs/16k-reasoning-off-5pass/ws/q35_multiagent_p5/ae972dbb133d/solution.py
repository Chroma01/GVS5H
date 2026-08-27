import sys

# Set recursion depth just in case, though we won't use recursion
sys.setrecursionlimit(2000)

def solve():
    # Read all input at once
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        T_str = next(iterator)
        T = int(T_str)
    except StopIteration:
        return

    MOD = 998244353

    results = []

    for _ in range(T):
        try:
            H = int(next(iterator))
            W = int(next(iterator))
        except StopIteration:
            break
            
        grid = []
        for _ in range(H):
            grid.append(next(iterator))
            
        # Count rows with even number of 'A's
        h_valid = 0
        for r in range(H):
            row_str = grid[r]
            a_count = row_str.count('A')
            if a_count % 2 == 0:
                h_valid += 1
                
        # Count columns with even number of 'A's
        v_valid = 0
        for c in range(W):
            a_count = 0
            for r in range(H):
                if grid[r][c] == 'A':
                    a_count += 1
            if a_count % 2 == 0:
                v_valid += 1
                
        total_valid = h_valid + v_valid
        ans = pow(2, total_valid, MOD)
        results.append(str(ans))

    print('\n'.join(results))

if __name__ == '__main__':
    solve()