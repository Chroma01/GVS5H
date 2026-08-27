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

    # Identify the required sum S from pairs where both A[i] and B[i] are known
    required_S = None
    possible = True
    
    # Also track the minimum required S from pairs with one unknown
    min_S = 0
    
    for i in range(N):
        a_val = A[i]
        b_val = B[i]
        
        if a_val != -1 and b_val != -1:
            # Both known: sum must be consistent
            current_sum = a_val + b_val
            if required_S is None:
                required_S = current_sum
            else:
                if required_S != current_sum:
                    possible = False
                    break
        elif a_val == -1 and b_val != -1:
            # A is unknown, B is known: need S >= B[i]
            if b_val > min_S:
                min_S = b_val
        elif a_val != -1 and b_val == -1:
            # B is unknown, A is known: need S >= A[i]
            if a_val > min_S:
                min_S = a_val
        else:
            # Both unknown: no constraint on S other than S >= 0 (handled by min_S init)
            pass
            
    if not possible:
        print("No")
        return

    if required_S is not None:
        # We have a fixed sum requirement
        if required_S < min_S:
            print("No")
        else:
            print("Yes")
    else:
        # No fixed sum requirement, we can choose any S >= min_S
        # Since min_S >= 0, we can always pick S = min_S
        print("Yes")

if __name__ == '__main__':
    solve()