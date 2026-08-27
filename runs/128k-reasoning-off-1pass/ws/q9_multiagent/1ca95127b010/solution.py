import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        X = int(next(iterator))
        Y = int(next(iterator))
        S = next(iterator)
        T = next(iterator)
    except StopIteration:
        return

    # The problem asks if we can transform S to T using specific block-swap operations.
    # Operation A: Swap X zeros and Y ones (0...0 -> 1...1, 1...1 -> 0...0).
    # Operation B: Swap Y ones and X zeros (1...1 -> 0...0, 0...0 -> 1...1).
    #
    # Key Insight:
    # Let P_S[i] be the number of 1s in S[0...i-1] (prefix sum of 1s).
    # Let P_T[i] be the number of 1s in T[0...i-1].
    # Define D[i] = P_T[i] - P_S[i].
    #
    # Operation A (at index i, 0-based) affects the prefix sums as follows:
    # It turns X zeros to ones and Y ones to zeros.
    # This effectively increases the count of 1s by X and decreases by Y in the affected range.
    # However, looking at the difference array D[i]:
    # Operation A adds -1 to D[k] for k in [i, i+X-1] (relative to the prefix sum definition).
    # Operation B adds +1 to D[k] for k in [i, i+Y-1].
    #
    # We want to make D[i] = 0 for all i from 1 to N.
    # We can use a greedy approach: iterate i from 1 to N.
    # If D[i] > 0, we must apply Operation A starting at i to reduce D[i] by 1.
    # If D[i] < 0, we must apply Operation B starting at i to increase D[i] by 1.
    #
    # To handle range updates efficiently, we use a difference array (or "pending updates" array).
    # pending_add[k] stores the value to be added to D[k] relative to D[k-1] (conceptually).
    # Actually, we maintain 'current_D' which is the value of D[i] at the current step.
    # When we apply an operation that affects range [i, i+L-1] by adding 'val',
    # we update current_D by 'val' immediately, and we need to remember to add 'val' back at i+L.
    # So we use pending_add[i+L] to store the correction for the next index.

    pending_add = [0] * (N + 2)
    
    current_D = 0
    possible = True
    
    # Iterate i from 1 to N (1-based index for logic, corresponds to prefix length)
    for i in range(1, N + 1):
        # Update current_D with pending changes from previous operations
        current_D += pending_add[i]
        
        # If current_D is not 0, we must fix it to 0
        if current_D > 0:
            # We need to decrease current_D.
            # This corresponds to Operation A (swapping 0^X 1^Y -> 1^Y 0^X).
            # Effectively adds -1 to D in range [i, i+X-1].
            # We need to check if the operation fits in the string.
            # The operation affects D indices up to i+X-1.
            # So we need i+X-1 <= N.
            if i + X - 1 > N:
                possible = False
                break
            
            # Apply the operation: subtract 1 from D[i...i+X-1]
            current_D -= 1
            # Schedule the +1 to be added back at i+X so that the effect stops there
            pending_add[i + X] += 1
            
        elif current_D < 0:
            # We need to increase current_D.
            # This corresponds to Operation B (swapping 1^Y 0^X -> 0^X 1^Y).
            # Effectively adds +1 to D in range [i, i+Y-1].
            # We need to check if the operation fits in the string.
            # The operation affects D indices up to i+Y-1.
            # So we need i+Y-1 <= N.
            if i + Y - 1 > N:
                possible = False
                break
            
            # Apply the operation: add 1 to D[i...i+Y-1]
            current_D += 1
            # Schedule the -1 to be added back at i+Y so that the effect stops there
            pending_add[i + Y] -= 1
            
        # If current_D == 0, we do nothing and move to next i.
        # Note: The loop continues to i+1. The pending_add[i+1] will be added to current_D in the next iteration.
        # This correctly propagates the effects of operations.
    
    if possible:
        print("Yes")
    else:
        print("No")

if __name__ == '__main__':
    solve()