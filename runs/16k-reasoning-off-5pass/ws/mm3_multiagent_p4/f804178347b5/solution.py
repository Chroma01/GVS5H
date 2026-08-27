import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    # Collect all characters from remaining tokens (handles both space-separated and concatenated)
    chars = []
    for token in data[1:]:
        chars.extend(token)
    total_len = 3 ** N
    A_str = ''.join(chars[:total_len])
    if len(A_str) < total_len:
        A_str += '0' * (total_len - len(A_str))
    
    # Initialize dp0 and dp1 for leaves
    dp0 = []
    dp1 = []
    for ch in A_str:
        if ch == '0':
            dp0.append(0)
            dp1.append(1)
        else:
            dp0.append(1)
            dp1.append(0)
    
    # Track current majority values at each level
    cur_level = list(A_str)
    
    # Bottom-up DP
    while len(dp0) > 1:
        new_dp0 = []
        new_dp1 = []
        new_cur = []
        for i in range(0, len(dp0), 3):
            c0 = [dp0[i], dp0[i+1], dp0[i+2]]
            c1 = [dp1[i], dp1[i+1], dp1[i+2]]
            
            sum_dp0 = sum(c0)
            sum_dp1 = sum(c1)
            
            # To force output 0: all three 0, or two 0 and one 1
            penalty_to_1 = min(c1[j] - c0[j] for j in range(3))
            node_dp0 = sum_dp0 + min(0, penalty_to_1)
            
            # To force output 1: all three 1, or two 1 and one 0
            penalty_to_0 = min(c0[j] - c1[j] for j in range(3))
            node_dp1 = sum_dp1 + min(0, penalty_to_0)
            
            new_dp0.append(node_dp0)
            new_dp1.append(node_dp1)
            
            # Compute current majority for this node
            v = [cur_level[i], cur_level[i+1], cur_level[i+2]]
            ones = sum(1 for x in v if x == '1')
            new_cur.append('1' if ones >= 2 else '0')
        
        dp0 = new_dp0
        dp1 = new_dp1
        cur_level = new_cur
    
    cur_root = cur_level[0]
    
    if cur_root == '0':
        print(dp1[0])
    else:
        print(dp0[0])

if __name__ == "__main__":
    solve()