import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(300000)

def solve():
    # Read all input at once
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        H = int(next(iterator))
        W = int(next(iterator))
        
        A = []
        for i in range(H):
            row = []
            for j in range(W):
                row.append(int(next(iterator)))
            A.append(row)
            
        Q = int(next(iterator))
        sh = int(next(iterator))
        sw = int(next(iterator))
    except StopIteration:
        return

    # Transpose if H > W to ensure H is the smaller dimension
    # This helps in keeping the grid "narrow" which is beneficial for some optimizations
    # although the O(HW) per query approach is used here.
    transpose = False
    if H > W:
        transpose = True
        new_A = [[0] * H for _ in range(W)]
        for i in range(H):
            for j in range(W):
                new_A[j][i] = A[i][j]
        A = new_A
        H, W = W, H
        sh, sw = sw, sh
        
    MOD = 998244353
    
    # Precompute modular inverse for numbers if needed, but we can compute on fly or precompute
    # Since A[i][j] can be 0, we handle it carefully.
    
    # L[i][j] = sum of products of paths from (0,0) to (i,j)
    # R[i][j] = sum of products of paths from (i,j) to (H-1,W-1)
    
    L = [[0] * W for _ in range(H)]
    R = [[0] * W for _ in range(H)]
    
    # Compute L table
    for i in range(H):
        for j in range(W):
            val = A[i][j]
            if i == 0 and j == 0:
                L[i][j] = val
            else:
                up = L[i-1][j] if i > 0 else 0
                left = L[i][j-1] if j > 0 else 0
                L[i][j] = val * ((up + left) % MOD) % MOD
                
    # Compute R table
    for i in range(H-1, -1, -1):
        for j in range(W-1, -1, -1):
            val = A[i][j]
            if i == H-1 and j == W-1:
                R[i][j] = val
            else:
                down = R[i+1][j] if i < H-1 else 0
                right = R[i][j+1] if j < W-1 else 0
                R[i][j] = val * ((down + right) % MOD) % MOD
                
    # Function to compute the answer using the formula: sum_{i,j} L[i][j] * R[i][j] / A[i][j]
    def get_answer():
        ans = 0
        for i in range(H):
            for j in range(W):
                if A[i][j] == 0:
                    continue
                # We need modular inverse of A[i][j]
                # Since MOD is prime, we can use Fermat's Little Theorem
                inv = pow(A[i][j], MOD-2, MOD)
                term = L[i][j] * R[i][j] % MOD * inv % MOD
                ans = (ans + term) % MOD
        return ans
        
    # Process queries
    # Current position of Takahashi (0-indexed)
    cur_h, cur_w = sh - 1, sw - 1
    
    # Precompute inverses for all possible A values? No, A values change.
    # But we can compute inverse on the fly. pow(a, MOD-2, MOD) is O(log MOD).
    
    output = []
    
    for _ in range(Q):
        try:
            d = next(iterator)
            a_val = int(next(iterator))
        except StopIteration:
            break

        # Move Takahashi
        if d == 'L':
            cur_w -= 1
        elif d == 'R':
            cur_w += 1
        elif d == 'U':
            cur_h -= 1
        elif d == 'D':
            cur_h += 1
            
        # Update the grid
        old_val = A[cur_h][cur_w]
        A[cur_h][cur_w] = a_val
        
        # If the value didn't change, the answer doesn't change
        if old_val == a_val:
            # We still need to print the current answer
            # But we haven't stored it. We can recompute or store it.
            # Recomputing is O(HW) which is too slow if done every query.
            # However, if old_val == a_val, we can just print the previous answer.
            # But we don't store the previous answer.
            # Let's just recompute the answer. It's O(HW).
            # To optimize, we can store the last answer.
            pass
            
        # Recompute L and R tables partially or fully?
        # Full recomputation is O(HW).
        # Given constraints and typical time limits, this might TLE.
        # But it's the most straightforward correct solution.
        
        # Let's try to optimize by only updating affected parts?
        # Updating L: only cells (i,j) with i >= cur_h, j >= cur_w are affected.
        # Updating R: only cells (i,j) with i <= cur_h, j <= cur_w are affected.
        
        # Update L table from (cur_h, cur_w) to (H-1, W-1)
        # We need to update row by row
        for i in range(cur_h, H):
            for j in range(cur_w, W):
                if i == cur_h and j == cur_w:
                    L[i][j] = A[i][j]
                else:
                    up = L[i-1][j] if i > 0 else 0
                    left = L[i][j-1] if j > 0 else 0
                    L[i][j] = A[i][j] * ((up + left) % MOD) % MOD
                    
        # Update R table from (cur_h, cur_w) to (0, 0)
        # We need to update row by row in reverse
        for i in range(cur_h, -1, -1):
            for j in range(cur_w, -1, -1):
                if i == cur_h and j == cur_w:
                    R[i][j] = A[i][j]
                else:
                    down = R[i+1][j] if i < H-1 else 0
                    right = R[i][j+1] if j < W-1 else 0
                    R[i][j] = A[i][j] * ((down + right) % MOD) % MOD
                    
        # Compute answer
        ans = 0
        for i in range(H):
            for j in range(W):
                if A[i][j] == 0:
                    continue
                inv = pow(A[i][j], MOD-2, MOD)
                term = L[i][j] * R[i][j] % MOD * inv % MOD
                ans = (ans + term) % MOD
                
        output.append(str(ans))
        
    print('\n'.join(output))

if __name__ == '__main__':
    solve()