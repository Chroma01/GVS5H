import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    N = int(input_data[0])
    X = int(input_data[1])
    Y = int(input_data[2])
    S = input_data[3]
    T = input_data[4]

    # Check invariant: number of 1s must be equal
    if S.count('1') != T.count('1'):
        print("No")
        return

    # Convert strings to lists for mutability
    s_list = list(S)
    
    # Iterate through the string to fix mismatches from left to right
    i = 0
    while i < N:
        if s_list[i] == T[i]:
            i += 1
            continue
        
        # Mismatch found: s_list[i] != T[i]
        # We must fix this position.
        # Case 1: s_list[i] is '0' and T[i] is '1'
        # We need to apply Operation A.
        # Op A requires: s_list[i...i+X-1] == '0' and s_list[i+X...i+X+Y-1] == '1'
        # Effect: s_list[i...i+Y-1] becomes '1', s_list[i+Y...i+Y+X-1] becomes '0'
        if s_list[i] == '0' and T[i] == '1':
            # Check if we have enough space and the pattern exists
            if i + X + Y > N:
                print("No")
                return
            
            # Check pattern: X zeros followed by Y ones
            # We can check this by slicing or iterating. Since N is up to 5*10^5, 
            # slicing creates copies but is O(X+Y) which is acceptable per mismatch.
            # However, to be safe and efficient, we check explicitly.
            
            # Check X zeros
            if not all(c == '0' for c in s_list[i : i+X]):
                print("No")
                return
            
            # Check Y ones
            if not all(c == '1' for c in s_list[i+X : i+X+Y]):
                print("No")
                return
            
            # Apply Operation A
            # Change s_list[i...i+Y-1] to '1'
            # Change s_list[i+Y...i+Y+X-1] to '0'
            for k in range(i, i+Y):
                s_list[k] = '1'
            for k in range(i+Y, i+Y+X):
                s_list[k] = '0'
            
            # After operation, the first Y characters are now '1'.
            # Since T[i] is '1', we fixed position i.
            # We can skip ahead by Y because positions i to i+Y-1 are now guaranteed to match T?
            # Wait, strictly speaking, we only know s_list[i] matches T[i].
            # The operation changes s_list[i+1...i+Y-1] to '1'. 
            # Does T[i+1...i+Y-1] necessarily have '1's? Not necessarily.
            # However, the operation is forced. We must apply it if we are at a mismatch.
            # After applying, we continue checking from i+1.
            # Optimization: Since we set s_list[i...i+Y-1] to '1', and we know T[i] is '1',
            # we can at least skip i. But we cannot skip more without checking T.
            # Let's just increment i by 1 to be safe and correct.
            # Actually, since we just set them to '1', if T had '0' in that range, we would have created a mismatch later.
            # That's fine, the loop will catch it.
            i += 1

        # Case 2: s_list[i] is '1' and T[i] is '0'
        # We need to apply Operation B.
        # Op B requires: s_list[i...i+Y-1] == '1' and s_list[i+Y...i+Y+X-1] == '0'
        # Effect: s_list[i...i+X-1] becomes '0', s_list[i+X...i+X+Y-1] becomes '1'
        elif s_list[i] == '1' and T[i] == '0':
            if i + X + Y > N:
                print("No")
                return
            
            # Check pattern: Y ones followed by X zeros
            if not all(c == '1' for c in s_list[i : i+Y]):
                print("No")
                return
            
            if not all(c == '0' for c in s_list[i+Y : i+Y+X]):
                print("No")
                return
            
            # Apply Operation B
            # Change s_list[i...i+X-1] to '0'
            # Change s_list[i+X...i+X+Y-1] to '1'
            for k in range(i, i+X):
                s_list[k] = '0'
            for k in range(i+X, i+X+Y):
                s_list[k] = '1'
            
            i += 1
        else:
            # This case should not be reachable if logic is correct (handled by if/elif)
            # If we are here, it means s_list[i] != T[i] but neither case matched.
            # This implies s_list[i] == T[i] which contradicts the loop check, 
            # OR the logic above missed a case.
            # Given the structure:
            # if match: continue
            # if 0->1: ...
            # elif 1->0: ...
            # else: unreachable.
            pass

    # If we successfully processed the whole string
    print("Yes")

if __name__ == '__main__':
    solve()