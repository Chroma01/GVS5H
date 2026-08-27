import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

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
    except StopIteration:
        return

    # The input is guaranteed to be sorted in ascending order by constraints.
    # A_i <= A_{i+1} is given, so A is already sorted.
    
    # Greedy Strategy:
    # We want to maximize the number of pairs (top, base) such that top <= base / 2.
    # This is equivalent to 2 * top <= base.
    #
    # To maximize pairs, we should pair the smallest available top with the smallest 
    # available base that satisfies the condition.
    # Why? Because larger bases are more versatile (they can support larger tops).
    # If we use a large base for a small top, we might waste its capacity.
    # By using the smallest valid base for the current smallest top, we save larger 
    # bases for larger tops that appear later in the sorted array.
    #
    # Algorithm:
    # 1. Initialize `left` pointer to 0 (smallest top candidate).
    # 2. Initialize `right` pointer to 1 (smallest base candidate).
    # 3. Iterate while `left` < N - 1:
    #    a. Advance `right` until we find an element A[right] >= 2 * A[left].
    #    b. If such an element is found (right < N):
    #       - We form a pair (A[left], A[right]).
    #       - Increment the answer count.
    #       - Move `left` forward to the next top candidate.
    #       - Move `right` forward to the next base candidate (since A[right] is used).
    #    c. If no such element is found (right reaches N):
    #       - It means there are no remaining bases large enough to support A[left].
    #       - Since the array is sorted, any subsequent top A[left+1] will be >= A[left],
    #         requiring an even larger base. Thus, no more pairs can be formed.
    #       - Break the loop.
    
    left = 0
    right = 1
    ans = 0
    n = len(A)
    
    while left < n - 1:
        # Find the smallest base >= 2 * A[left]
        while right < n and A[right] < 2 * A[left]:
            right += 1
        
        if right < n:
            # Pair found
            ans += 1
            left += 1
            right += 1
        else:
            # No base found for A[left]. Since A is sorted, no base for any subsequent top.
            break
            
    print(ans)

if __name__ == '__main__':
    solve()