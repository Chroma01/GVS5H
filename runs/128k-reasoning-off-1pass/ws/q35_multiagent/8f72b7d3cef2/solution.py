import sys

def solve():
    # Increase recursion depth just in case, though we use iterative approach
    sys.setrecursionlimit(2000)
    
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
    except StopIteration:
        return

    # 1. Compute Prefix Sums
    # prefix_sum[i] = sum(A[0]...A[i-1])
    # sum(A[l...r]) = prefix_sum[r+1] - prefix_sum[l]
    prefix_sum = [0] * (N + 1)
    for i in range(N):
        prefix_sum[i+1] = prefix_sum[i] + A[i]

    # 2. Compute PGE (Previous Greater or Equal) and NGE (Next Greater or Equal)
    # PGE[i] is the index of the nearest element to the left of i such that A[PGE[i]] >= A[i]
    # If no such element exists, PGE[i] = -1
    # NGE[i] is the index of the nearest element to the right of i such that A[NGE[i]] >= A[i]
    # If no such element exists, NGE[i] = N
    
    pge = [-1] * N
    nge = [N] * N
    
    # Monotonic stack for PGE (decreasing stack)
    # We want the nearest element to the left that is >= current.
    # Stack stores indices.
    stack = []
    for i in range(N):
        while stack and A[stack[-1]] < A[i]:
            stack.pop()
        if stack:
            pge[i] = stack[-1]
        stack.append(i)
        
    # Monotonic stack for NGE (decreasing stack)
    # We want the nearest element to the right that is >= current.
    stack = []
    for i in range(N-1, -1, -1):
        while stack and A[stack[-1]] < A[i]:
            stack.pop()
        if stack:
            nge[i] = stack[-1]
        stack.append(i)

    # 3. For each K, simulate the expansion
    results = []
    
    for k in range(N):
        # Initial boundaries
        # The range Takahashi can initially absorb is (pge[k], nge[k])
        # Indices strictly between pge[k] and nge[k]
        left_bound = pge[k]
        right_bound = nge[k]
        
        # Current sum of the range (left_bound, right_bound)
        # Sum of A[left_bound+1 ... right_bound-1]
        current_sum = prefix_sum[right_bound] - prefix_sum[left_bound + 1]
        
        # Expand until no more absorptions are possible
        while True:
            expanded = False
            
            # Check left expansion
            # If left_bound is valid (>= 0) and current_sum > A[left_bound]
            if left_bound >= 0 and current_sum > A[left_bound]:
                # Absorb the left boundary and jump to its PGE
                # The new range will include A[left_bound]
                # New left bound becomes pge[left_bound]
                # But we must update current_sum first
                # Actually, we can just update the bound and recalculate sum or incrementally add
                # Let's incrementally add for clarity, but recalc is safer and O(1)
                
                # We absorb A[left_bound]
                # The new left boundary is pge[left_bound]
                # The new range is (pge[left_bound], right_bound)
                
                # Optimization: Just update bounds and recalc sum
                # But wait, we might expand both sides in one step?
                # The problem says "any number of times". The order doesn't matter for the final set.
                # However, the condition depends on current size.
                # If we expand left, size increases. This might help expand right.
                # So we should check both sides with the CURRENT sum.
                
                # Let's collect all possible expansions for this step
                next_left = left_bound
                next_right = right_bound
                
                if left_bound >= 0 and current_sum > A[left_bound]:
                    next_left = pge[left_bound]
                    expanded = True
                
                if right_bound < N and current_sum > A[right_bound]:
                    next_right = nge[right_bound]
                    expanded = True
                
                if expanded:
                    left_bound = next_left
                    right_bound = next_right
                    current_sum = prefix_sum[right_bound] - prefix_sum[left_bound + 1]
                else:
                    break
            else:
                # If left is not expandable, check right
                # But we must check right with the SAME current_sum
                if right_bound < N and current_sum > A[right_bound]:
                    next_right = nge[right_bound]
                    left_bound = left_bound # unchanged
                    right_bound = next_right
                    current_sum = prefix_sum[right_bound] - prefix_sum[left_bound + 1]
                    expanded = True
                else:
                    break
        
        results.append(str(current_sum))

    print(" ".join(results))

if __name__ == '__main__':
    solve()