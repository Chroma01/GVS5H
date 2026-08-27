import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
        B = []
        for _ in range(N):
            B.append(int(next(iterator)))
    except StopIteration:
        return

    # Step 1: Identify indices where both A[i] and B[i] are fixed (not -1)
    fixed_indices = []
    for i in range(N):
        if A[i] != -1 and B[i] != -1:
            fixed_indices.append(i)
    
    # Step 2: If there are no fixed-fixed pairs, it's always possible.
    # Reasoning: We can choose S = max(max(A_fixed), max(B_fixed), 0).
    # Then for any index with A[i] fixed, B[i] = S - A[i] >= 0.
    # For any index with B[i] fixed, A[i] = S - B[i] >= 0.
    # For indices with both -1, we can set A[i]=0, B[i]=S.
    if not fixed_indices:
        print("Yes")
        return

    # Step 3: If there are fixed-fixed pairs, S is determined by the first one.
    S = A[fixed_indices[0]] + B[fixed_indices[0]]
    
    # Check if all other fixed-fixed pairs have the same sum S
    for i in fixed_indices:
        if A[i] + B[i] != S:
            print("No")
            return

    # Step 4: Check if the remaining elements can be filled to sum to S with non-negative integers.
    # For each index i:
    # - If A[i] is fixed and B[i] is -1, we need B[i] = S - A[i] >= 0 => S >= A[i]
    # - If B[i] is fixed and A[i] is -1, we need A[i] = S - B[i] >= 0 => S >= B[i]
    # - If both are -1, we can always fill (e.g., 0 and S)
    # - If both are fixed, already checked sum is S
    
    for i in range(N):
        if A[i] != -1 and B[i] == -1:
            if S < A[i]:
                print("No")
                return
        elif A[i] == -1 and B[i] != -1:
            if S < B[i]:
                print("No")
                return
        # If both are -1, no constraint on S other than S >= 0 (which is implied if any fixed value is >=0 and S is sum of non-negatives)
        # If both are fixed, already checked.
        
    # Also, S must be non-negative. Since A[i], B[i] >= 0 for fixed-fixed pairs, S >= 0 is guaranteed.
    # However, if there were no fixed-fixed pairs, we handled it above.
    # If there are fixed-fixed pairs, S is sum of non-negatives, so S >= 0.
    
    print("Yes")

if __name__ == '__main__':
    solve()