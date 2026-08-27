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

    # Identify indices where both A[i] and B[i] are known (not -1)
    # These pairs impose a hard constraint on the sum S = A[i] + B[i].
    # Since we can rearrange A, the position doesn't matter for the sum constraint,
    # but the values themselves are fixed. If we have two fully known pairs (a1, b1) and (a2, b2),
    # they must both sum to the same S.
    known_pairs = []
    for i in range(N):
        if A[i] != -1 and B[i] != -1:
            known_pairs.append((A[i], B[i]))
    
    # If there are no fully known pairs, we can choose any S (e.g., 0) and fill all -1s with 0.
    # Thus, it is always possible.
    if len(known_pairs) == 0:
        print("Yes")
        return

    # Check if all known pairs have the same sum
    target_sum = known_pairs[0][0] + known_pairs[0][1]
    possible = True
    
    for a, b in known_pairs[1:]:
        if a + b != target_sum:
            possible = False
            break
    
    if possible:
        print("Yes")
    else:
        print("No")

if __name__ == '__main__':
    solve()