import sys

# Set recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

MOD = 998244353

def solve():
    # Read input from stdin
    try:
        input_data = sys.stdin.read().split()
        if not input_data:
            return
        W = int(input_data[0])
        H = int(input_data[1])
        L = int(input_data[2])
        R = int(input_data[3])
        D = int(input_data[4])
        U = int(input_data[5])
    except ValueError:
        return

    # Helper function to calculate sum of arithmetic series
    # Sum of (A - k) for k in [0, n-1] = n*A - n*(n-1)/2
    def sum_linear(n, A):
        if n <= 0:
            return 0
        term1 = (n * A) % MOD
        term2 = (n * (n - 1)) // 2
        return (term1 - term2) % MOD

    total_paths = 0

    # Precompute common sums for y-ranges
    # Sum_{y=0}^{H} (H-y+1) = Sum_{k=1}^{H+1} k = (H+1)(H+2)/2
    C_y = (H + 1) * (H + 2) // 2
    
    # Sum_{y=0}^{D-1} (H-y+1)
    # y=0 -> H+1, y=D-1 -> H-D+2. Count = D.
    # Sum = D * (H+1 + H-D+2) // 2 = D * (2H - D + 3) // 2
    S_y1 = (D * (2 * H - D + 3)) // 2
    
    # Sum_{y=U+1}^{H} (H-y+1)
    # y=U+1 -> H-U, y=H -> 1. Count = H-U.
    # Sum = (H-U)*(H-U+1)//2
    S_y2 = (H - U) * (H - U + 1) // 2

    # Range 1: x in [0, L-1]
    # Valid y: [0, H]. Intersection with blocked [L, R]x[D, U] is empty.
    # Contribution: Sum_{x=0}^{L-1} (W-x+1) * C_y
    if L > 0:
        n_x = L
        # Sum_{x=0}^{L-1} (W-x+1)
        # x=0 -> W+1, x=L-1 -> W-L+2
        # Sum = n_x * (W+1) - n_x*(n_x-1)//2
        sum_x = (n_x * (W + 1) - n_x * (n_x - 1) // 2) % MOD
        term1 = (C_y * sum_x) % MOD
        total_paths = (total_paths + term1) % MOD

    # Range 2: x in [L, R]
    # Valid y: [0, D-1] and [U+1, H]
    if R >= L:
        n_x = R - L + 1
        
        # Sum_{x=L}^{R} (W-x+1)
        # x=L -> W-L+1, x=R -> W-R+1
        sum_Wx = (n_x * (W - L + 1) - n_x * (n_x - 1) // 2) % MOD
        
        # Sum_{x=L}^{R} (R-x+1)
        # x=L -> R-L+1, x=R -> 1
        sum_Rx = (n_x * (R - L + 1) - n_x * (n_x - 1) // 2) % MOD
        
        # Part A: y in [0, D-1]
        # Term = (W-x+1)*(H-y+1) - (R-x+1)*(U-D+1)
        # Sum over y: (W-x+1)*S_y1 - (R-x+1)*(U-D+1)*D
        # Sum over x: S_y1 * sum_Wx - (U-D+1)*D * sum_Rx
        const_B = (U - D + 1) * D
        term2a = (S_y1 * sum_Wx) % MOD
        term2b = (const_B * sum_Rx) % MOD
        term2 = (term2a - term2b) % MOD
        total_paths = (total_paths + term2) % MOD

        # Part B: y in [U+1, H]
        # Term = (W-x+1)*(H-y+1)
        # Sum over y: (W-x+1)*S_y2
        # Sum over x: S_y2 * sum_Wx
        if U < H:
            term2b2 = (S_y2 * sum_Wx) % MOD
            total_paths = (total_paths + term2b2) % MOD

    # Range 3: x in [R+1, W]
    # Valid y: [0, H]. Intersection with blocked [L, R]x[D, U] is empty.
    if W > R:
        n_x = W - R
        # Sum_{x=R+1}^{W} (W-x+1)
        # x=R+1 -> W-R, x=W -> 1
        # Sum = n_x * (W-R+1) // 2
        sum_Wx3 = (n_x * (W - R + 1)) // 2
        term3 = (C_y * sum_Wx3) % MOD
        total_paths = (total_paths + term3) % MOD

    print(total_paths)

if __name__ == '__main__':
    solve()