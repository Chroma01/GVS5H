import sys

def solve():
    MOD = 998244353
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    S = input_data[1].strip()
    
    # Check ballot condition: every prefix has #B >= #W
    bal = 0
    for c in S:
        if c == 'B':
            bal += 1
        else:
            bal -= 1
        if bal < 0:
            print(0)
            return
    
    # Get positions of B and W (0-indexed)
    B = [i for i, c in enumerate(S) if c == 'B']
    W = [i for i, c in enumerate(S) if c == 'W']
    
    # The number of valid matchings is the number of permutations pi of B
    # such that the matching W_i -> B_{pi(i)} makes the graph strongly connected.
    # This is equivalent to: the matching forms a single cycle when combined
    # with the path. The count is the product of (number of available B's)
    # at each step when processing W's in order, where a B is available if
    # it is unmatched and its position is < current W's position.
    # The number of choices for the i-th W (0-indexed) is:
    # (number of B's in positions 0..w_i-1) - i
    # = (cumulative B count up to w_i) - i
    # This is the number of B's to the left of w_i minus the number of
    # W's already processed.
    
    ans = 1
    b_count = 0
    w_idx = 0
    for i, c in enumerate(S):
        if c == 'B':
            b_count += 1
        else:
            # This is the w_idx-th W (0-indexed)
            choices = b_count - w_idx
            if choices <= 0:
                ans = 0
                break
            ans = ans * choices % MOD
            w_idx += 1
    
    print(ans)

if __name__ == "__main__":
    solve()