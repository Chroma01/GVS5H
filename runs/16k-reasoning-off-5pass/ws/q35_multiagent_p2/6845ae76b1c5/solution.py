import sys

def solve():
    # Fast I/O
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
        B = [int(next(iterator)) for _ in range(N)]
        K = int(next(iterator))
        queries = []
        for k in range(K):
            x = int(next(iterator))
            y = int(next(iterator))
            queries.append((x, y, k))
    except StopIteration:
        return

    # Sort A and B
    A.sort()
    B.sort()
    
    # Precompute prefix sums for B
    # SB[i] = sum(B[0]...B[i-1])
    SB = [0] * (N + 1)
    for i in range(N):
        SB[i+1] = SB[i] + B[i]
        
    # Group queries by Y
    # queries_by_y[y] = list of (x, original_index)
    queries_by_y = {}
    for x, y, k in queries:
        if y not in queries_by_y:
            queries_by_y[y] = []
        queries_by_y[y].append((x, k))
        
    # Answers array
    answers = [0] * K
    
    # Process each distinct Y
    for y, q_list in queries_by_y.items():
        # B_sub is B[0:y], but we use indices to avoid copying
        # SB is already computed for full B, so sum(B[0:y]) = SB[y]
        
        # We need to compute S[i] = sum_{j=0}^{y-1} |A[i] - B[j]| for all i=0..N-1
        # Then prefix sum of S to answer queries for different X
        
        # Two-pointer approach
        # ptr points to the first element in B[0:y] that is > A[i]
        # All B[0...ptr-1] are <= A[i]
        
        S = [0] * N
        ptr = 0
        sum_le = 0
        sum_gt = SB[y] # Sum of all B[0...y-1]
        
        # Iterate over A
        for i in range(N):
            val_a = A[i]
            # Move ptr forward while B[ptr] <= val_a
            while ptr < y and B[ptr] <= val_a:
                sum_le += B[ptr]
                sum_gt -= B[ptr]
                ptr += 1
            
            # Number of elements <= val_a is ptr
            # Number of elements > val_a is y - ptr
            # Sum = ptr * val_a - sum_le + sum_gt - (y - ptr) * val_a
            cnt_le = ptr
            cnt_gt = y - ptr
            S[i] = cnt_le * val_a - sum_le + sum_gt - cnt_gt * val_a
            
        # Compute prefix sums of S
        # prefix_S[x] = sum(S[0]...S[x-1])
        prefix_S = [0] * (N + 1)
        current = 0
        for i in range(N):
            current += S[i]
            prefix_S[i+1] = current
            
        # Answer queries for this Y
        for x, k in q_list:
            # Query asks for sum_{i=0}^{x-1} S[i] (since A is 0-indexed in code, but 1-indexed in problem)
            # A[0]...A[x-1] corresponds to first x elements
            answers[k] = prefix_S[x]
            
    # Print answers
    for ans in answers:
        print(ans)

if __name__ == '__main__':
    solve()