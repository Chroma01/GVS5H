import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    N = int(input_data[0])
    S = input_data[1]
    
    MOD = 998244353
    
    # Necessary condition 1: First vertex must be Black to be reachable
    # Necessary condition 2: Last vertex must be White to be able to reach others
    if S[0] != 'B' or S[-1] != 'W':
        print(0)
        return

    # Decompose the string into primitive components
    # A primitive component is a segment where the balance (W - B) returns to 0
    # for the first time at the end of the segment.
    
    components = []
    current_comp_start = 0
    balance = 0
    
    for i, char in enumerate(S):
        if char == 'W':
            balance += 1
        else:
            balance -= 1
            
        if balance == 0:
            # Found a primitive component from current_comp_start to i (inclusive)
            comp_str = S[current_comp_start : i+1]
            components.append(comp_str)
            current_comp_start = i + 1
            
    # If the string didn't decompose perfectly (shouldn't happen if N Ws and N Bs), handle it
    if current_comp_start != len(S):
        # This case implies the total balance is not 0, which contradicts constraints
        # But for safety, we can return 0
        print(0)
        return

    K = len(components)
    
    # Check if each component is valid
    # A component is valid if it starts with 'B' and ends with 'W'
    # This ensures that within the component, the first node can be reached
    # and the last node can reach out, which is necessary for the component
    # to participate in a strongly connected global structure.
    for comp in components:
        if comp[0] != 'B' or comp[-1] != 'W':
            print(0)
            return
            
    # If all components are valid, the number of ways to connect K components
    # into a single strongly connected cycle is (K-1)!
    # This is because we are essentially arranging K items in a circle.
    
    # Compute (K-1)! % MOD
    ans = 1
    for i in range(1, K):
        ans = (ans * i) % MOD
        
    print(ans)

if __name__ == '__main__':
    solve()