import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
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

    # If strings are already identical
    if S == T:
        print("Yes")
        return

    # If length is less than X + Y, no operations can be performed
    if N < X + Y:
        print("No")
        return

    # Precompute target patterns for comparison
    pat0 = [0] * X
    pat1 = [1] * Y

    # Convert strings to lists of integers for easier manipulation
    S_list = [int(c) for c in S]
    T_list = [int(c) for c in T]

    # Greedy simulation: process from left to right
    for i in range(N):
        if S_list[i] == T_list[i]:
            continue
        
        # Mismatch found, must fix it
        if S_list[i] == 0 and T_list[i] == 1:
            # Need to turn 0 to 1. Requires Operation A at index i.
            # Operation A: 0^X 1^Y -> 1^Y 0^X
            # Requires S[i...i+X-1] == 0 and S[i+X...i+X+Y-1] == 1
            if i + X + Y > N:
                print("No")
                return
            
            # Check conditions using slicing (efficient in Python)
            if S_list[i:i+X] == pat0 and S_list[i+X:i+X+Y] == pat1:
                # Apply Operation A
                # Change S[i...i+Y-1] to 1
                # Change S[i+Y...i+Y+X-1] to 0
                S_list[i:i+Y] = [1] * Y
                S_list[i+Y:i+Y+X] = [0] * X
            else:
                print("No")
                return
        
        elif S_list[i] == 1 and T_list[i] == 0:
            # Need to turn 1 to 0. Requires Operation B at index i.
            # Operation B: 1^Y 0^X -> 0^X 1^Y
            # Requires S[i...i+Y-1] == 1 and S[i+Y...i+Y+X-1] == 0
            if i + X + Y > N:
                print("No")
                return
            
            # Check conditions
            if S_list[i:i+Y] == pat1 and S_list[i+Y:i+Y+X] == pat0:
                # Apply Operation B
                # Change S[i...i+X-1] to 0
                # Change S[i+X...i+X+Y-1] to 1
                S_list[i:i+X] = [0] * X
                S_list[i+X:i+X+Y] = [1] * Y
            else:
                print("No")
                return
        
        else:
            # This case should not be reachable given the logic above
            # (S[i] != T[i] implies one is 0 and other is 1)
            pass

    # After processing, check if S matches T
    # Note: The loop ensures we fix every mismatch encountered.
    # If we reach the end, S should match T.
    if S_list == T_list:
        print("Yes")
    else:
        # This implies we couldn't fix some mismatch or logic gap
        print("No")

if __name__ == '__main__':
    solve()