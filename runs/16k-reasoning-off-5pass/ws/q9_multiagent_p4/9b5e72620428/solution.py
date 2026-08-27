import sys
from collections import Counter

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

    # Identify indices where both A[i] and B[i] are known (not -1)
    known_pairs = []
    for i in range(N):
        if A[i] != -1 and B[i] != -1:
            known_pairs.append((A[i], B[i]))
    
    # If there are known pairs, they must all sum to the same S
    if known_pairs:
        target_S = known_pairs[0][0] + known_pairs[0][1]
        for a, b in known_pairs[1:]:
            if a + b != target_S:
                print("No")
                return
        
        S = target_S
        
        # Check 1: For any index i where B[i] != -1, we must be able to form sum S.
        # If A[i] is -1, we need to fill it with S - B[i]. This requires S >= B[i].
        # If A[i] is not -1, it's already in known_pairs, so sum is S (checked above).
        # So we just need to check S >= B[i] for all i where B[i] != -1.
        for i in range(N):
            if B[i] != -1:
                if S < B[i]:
                    print("No")
                    return
        
        # Check 2: We have a multiset of known values in A (M_A).
        # We need to assign these values to indices.
        # Indices are split into U (where B[i] != -1) and V (where B[i] == -1).
        # - If we assign a value v from M_A to an index in U, we must have v + B[i] = S => v = S - B[i].
        #   This means v must be exactly the required value for that slot.
        # - If we assign a value v from M_A to an index in V, we must have v + B'[i] = S => B'[i] = S - v.
        #   Since we can choose B'[i] >= 0, we just need S - v >= 0 => v <= S.
        # - Values in M_A that are > S CANNOT be placed in V. They MUST be placed in U.
        #   If placed in U, they must match the specific requirement S - B[i].
        
        M_A_counts = Counter()
        for x in A:
            if x != -1:
                M_A_counts[x] += 1
        
        U_requirements = Counter()
        for i in range(N):
            if B[i] != -1:
                req = S - B[i]
                U_requirements[req] += 1
        
        # Check if all values in M_A that are > S can be satisfied by U_requirements
        for val, count in M_A_counts.items():
            if val > S:
                # These values MUST go to U
                if count > U_requirements[val]:
                    print("No")
                    return
        
        # If all checks pass, it is possible.
        print("Yes")
    else:
        # No known pairs where both A[i] and B[i] are non-negative.
        # We can choose S arbitrarily large.
        # Let S = max(max(A_known), max(B_known), 0) + 1 (if any exist), else 0.
        # With sufficiently large S:
        # 1. For all i where B[i] != -1, S >= B[i] holds.
        # 2. For all v in M_A, v <= S holds.
        #    - Values in M_A can all be placed in V (since v <= S).
        #    - Slots in U can be filled with new values (since S >= B[i]).
        # Thus, it is always possible.
        print("Yes")

if __name__ == '__main__':
    solve()