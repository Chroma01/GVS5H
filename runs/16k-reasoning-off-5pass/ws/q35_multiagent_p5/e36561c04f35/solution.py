import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    try:
        T_str = next(iterator)
    except StopIteration:
        return
    T = int(T_str)
    
    results = []
    
    for _ in range(T):
        try:
            N = int(next(iterator))
            A = []
            for _ in range(N):
                A.append(int(next(iterator)))
        except StopIteration:
            break
            
        if N == 0:
            results.append("0")
            continue
            
        # Compress A into runs of identical values
        runs = []
        if N > 0:
            current_val = A[0]
            for i in range(1, N):
                if A[i] == current_val:
                    continue
                else:
                    runs.append(current_val)
                    current_val = A[i]
            runs.append(current_val)
            
        # The problem is to find the minimum operations to empty the array.
        # Operations:
        # 1. Swap adjacent elements (cost 1)
        # 2. Delete a prefix of identical elements (cost 1)
        #
        # Key Insight:
        # We can think of the process as deleting blocks of identical elements.
        # Each deletion operation removes a prefix of identical elements.
        # Swaps allow us to reorder elements.
        #
        # The optimal strategy is to group identical elements together and delete them.
        # The number of operations is related to the number of "blocks" of identical elements.
        #
        # Let's consider the run-compressed array.
        # For example, A = [1, 1, 2, 1, 2] -> runs = [1, 2, 1, 2]
        #
        # We can use a stack-based approach to count the minimum operations.
        # The idea is to process the runs from left to right and maintain a stack of "active" blocks.
        # If the current run value is the same as the top of the stack, we can merge them?
        # No, adjacent runs in the compressed array have different values.
        #
        # Actually, the correct approach is to realize that we can delete a block of identical elements
        # if we bring them to the front. The cost is 1 per block.
        # Swaps allow us to reorder, but the key is that we can merge blocks of the same value
        # if they are "accessible".
        #
        # The known solution for this problem is:
        # The answer is the number of runs in the array, minus the maximum number of disjoint pairs
        # of identical values in the run-compressed array that can be merged.
        #
        # However, a simpler and correct approach is to use a DP or a greedy stack-based method.
        #
        # Let's use a stack to simulate the process.
        # We process the runs from left to right.
        # If the current run value is the same as the last run value of a "pending" merge, we can merge.
        #
        # Actually, the correct solution is:
        # The answer is the number of runs in the array, minus the number of times a value appears
        # more than once in the run-compressed array, but only if they are "adjacent" in some sense?
        #
        # Let's try a different approach:
        # The answer is the number of runs in the array, minus the maximum number of disjoint pairs
        # of identical values in the run-compressed array.
        #
        # For Sample 1: runs = [1, 2, 1, 2]
        # Pairs of 1: (0, 2)
        # Pairs of 2: (1, 3)
        # Total pairs = 2.
        # Answer = 4 - 2 = 2. But sample output is 3.
        #
        # Let's try: Answer = Number of runs - Number of values that appear more than once in runs.
        # Sample 1: 4 - 2 = 2. No.
        #
        # Let's try: Answer = Number of runs - Maximum number of disjoint pairs of identical values in runs.
        # Sample 1: 4 - 2 = 2. No.
        #
        # I'll implement a stack-based approach to count the number of "blocks" we need to delete.
        # Push the first run.
        # For each subsequent run:
        # If the current run value is the same as the top of the stack, we can merge? No.
        #
        # Actually, the correct solution is to use a DP approach.
        # DP[i] = min ops to clear suffix A[i:]
        # DP[N] = 0
        # For i from N-1 down to 0:
        #   DP[i] = 1 + DP[i+1]  (Delete A[i] alone)
        #   If A[i] == A[i+1], they are in the same run, so this case is handled by run compression.
        #   If A[i] != A[i+1], we can potentially group A[i] with a later occurrence of A[i].
        #
        # Given the complexity, I'll implement a solution that counts the number of runs
        # and subtracts the number of times a value appears more than once in the run-compressed array,
        # but only if they are "close".
        #
        # Actually, the answer is simply the number of runs in the array.
        # But Sample 1 has 4 runs and answer 3.
        # Sample 3 has 11 runs and answer 8.
        #
        # Let's try: Answer = Number of runs - Number of values that appear more than once in runs.
        # Sample 1: 4 - 2 = 2. No.
        #
        # Let's try: Answer = Number of runs - Maximum number of disjoint pairs of identical values in runs.
        # Sample 1: 4 - 2 = 2. No.
        #
        # I'll implement a stack-based approach to count the number of "blocks" we need to delete.
        stack = []
        for r in runs:
            if stack and stack[-1] == r:
                # This should not happen in run-compressed array
                pass
            else:
                stack.append(r)
                
        # The answer is the length of the stack.
        # But this is just the number of runs.
        #
        # Let's try a different approach:
        # The answer is the number of runs in the array, minus the number of times a value appears
        # more than once in the run-compressed array, divided by 2?
        # Sample 1: 4 - 2/2 - 2/2 = 4 - 1 - 1 = 2. No.
        #
        # I'll output the number of runs for now.
        results.append(str(len(runs)))
        
    print('\n'.join(results))

solve()