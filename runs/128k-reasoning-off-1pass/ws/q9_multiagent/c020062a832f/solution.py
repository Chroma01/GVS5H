import sys

# Increase recursion depth just in case, though we use iterative approaches
sys.setrecursionlimit(200005)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
    except StopIteration:
        return

    # Fenwick Tree (Binary Indexed Tree) implementation
    # 1-based indexing for BIT
    class FenwickTree:
        def __init__(self, size):
            self.tree = [0] * (size + 1)

        def update(self, i, delta):
            while i < len(self.tree):
                self.tree[i] += delta
                i += i & (-i)

        def query(self, i):
            s = 0
            while i > 0:
                s += self.tree[i]
                i -= i & (-i)
            return s

        def query_range(self, l, r):
            if l > r:
                return 0
            return self.query(r) - self.query(l - 1)

    # Step 1: Calculate initial inversion count for k=0
    # We need to count pairs (i, j) such that i < j and A[i] > A[j].
    # Since 0 <= A[i] < M, we can use a Fenwick tree of size M.
    
    bit = FenwickTree(M)
    initial_inversions = 0
    
    # Traverse from right to left to count inversions
    # For each A[i], count how many elements to its right are smaller than A[i]
    # Or traverse left to right and count how many elements to the left are larger.
    # Let's do left to right: for current x, inversions += (count of elements seen so far > x)
    # count(> x) = total_seen - count(<= x)
    
    total_seen = 0
    for x in A:
        # count elements <= x
        cnt_le = bit.query(x + 1) # query(x+1) gives sum from 1 to x+1 (indices 1..x+1)
        # Since values are 0..M-1, we map value v to index v+1 in BIT.
        # query(v+1) returns sum of frequencies for values 0..v.
        
        # Elements seen so far > x
        greater = total_seen - cnt_le
        initial_inversions += greater
        
        bit.update(x + 1, 1)
        total_seen += 1

    # Step 2: Prepare for incremental updates
    # We need to track which elements wrap around.
    # An element A[i] wraps around when A[i] + k >= M.
    # Specifically, at step k (0-indexed), elements with A[i] >= M - k are in the "wrapped" set (S_large).
    # Elements with A[i] < M - k are in the "unwrapped" set (S_small).
    #
    # Transition from k to k+1:
    # Elements with A[i] == M - 1 - k move from S_small to S_large.
    # Let this set of indices be W.
    #
    # Logic for update:
    # Let S_small be indices where A[i] + k < M.
    # Let S_large be indices where A[i] + k >= M.
    #
    # Current Inversions = 
    #   (Inversions within S_small) + 
    #   (Inversions within S_large) + 
    #   (Inversions between S_small and S_large)
    #
    # Note: For any i in S_small and j in S_large:
    #   B[i] = A[i] + k >= k
    #   B[j] = A[j] + k - M < k
    #   So B[i] > B[j] is always true.
    #   Thus, an inversion exists between i and j if and only if i < j.
    #   So, Cross Inversions = count of pairs (i, j) such that i in S_small, j in S_large, and i < j.
    #
    # When moving from k to k+1:
    # Elements in W (where A[i] = M - 1 - k) move from S_small to S_large.
    #
    # Change in Inversions:
    # 1. Internal S_small: No change (relative order of values A[i]+k vs A[p]+k is same as A[i] vs A[p]).
    # 2. Internal S_large: No change (relative order of values A[i]-M+k vs A[p]-M+k is same).
    # 3. Cross Inversions:
    #    Before (at k): i in S_small, j in S_large. Inversion if i < j.
    #    After (at k+1): i in S_large, j in S_large (if j was already wrapped) OR i in S_large, j in S_small (if j is new).
    #    Wait, let's look at the specific change for an element i moving from S_small to S_large.
    #    
    #    Let i be an element moving from S_small to S_large.
    #    Let S_large_old be the set of elements already in S_large before this step.
    #    Let S_small_old be the set of elements in S_small before this step (including i).
    #    
    #    Pairs involving i:
    #    a) i with j in S_large_old:
    #       Before: i in S_small, j in S_large. B[i] > B[j]. Inversion if i < j.
    #       After: i in S_large, j in S_large. B[i] = A[i] + (k+1) - M, B[j] = A[j] + k - M.
    #             Wait, B[i] at k+1 is A[i] + k + 1 - M. B[j] at k+1 is A[j] + k - M.
    #             Difference B[i] - B[j] = A[i] - A[j] + 1.
    #             This relative order might change!
    #             Actually, the values in S_large are A[x] - (M - (k+1)).
    #             So B[i] = A[i] - (M - k - 1). B[j] = A[j] - (M - k - 1).
    #             The comparison B[i] > B[j] is equivalent to A[i] > A[j].
    #             So the relative order within S_large is determined by A values.
    #             However, we need to be careful. The set S_large_old contains elements with A[j] >= M - k.
    #             The new element i has A[i] = M - 1 - k.
    #             So A[i] < A[j] for all j in S_large_old.
    #             Therefore, B[i] < B[j] for all j in S_large_old.
    #             Before: i in S_small, j in S_large. B[i] > B[j]. Inversion if i < j.
    #             After: i in S_large, j in S_large. B[i] < B[j]. Inversion if i < j? No, B[i] < B[j] means NOT an inversion for pair (i, j) if i < j.
    #             Wait, inversion definition: i < j and B[i] > B[j].
    #             Before: i < j and B[i] > B[j] -> Inversion.
    #             After: i < j and B[i] < B[j] -> No Inversion.
    #             So for all j in S_large_old with j > i, we lose an inversion.
    #             For all j in S_large_old with j < i: Before (i > j, B[i] > B[j] -> No inv). After (i > j, B[i] < B[j] -> No inv). No change.
    #             So we subtract count of j in S_large_old such that j > i.
    #
    #    b) i with p in S_small_old (p != i):
    #       Before: Both in S_small. B[p] = A[p] + k, B[i] = A[i] + k.
    #             Inversion if p < i and B[p] > B[i] <=> A[p] > A[i].
    #       After: p in S_small, i in S_large.
    #             B[p] = A[p] + (k+1), B[i] = A[i] + (k+1) - M.
    #             B[p] >= k+1, B[i] < k+1. So B[p] > B[i] is always true.
    #             Inversion if p < i.
    #             So for all p in S_small_old with p < i:
    #               Before: Inversion if A[p] > A[i].
    #               After: Inversion (always).
    #               Change: +1 if A[p] <= A[i], 0 if A[p] > A[i].
    #             For all p in S_small_old with p > i:
    #               Before: No inversion (since p > i).
    #               After: No inversion (since p > i).
    #             So we add count of p in S_small_old such that p < i AND A[p] <= A[i].
    #
    #    c) i with itself: No change.
    #
    #    Summary for one element i moving from S_small to S_large:
    #      Delta = (Count of p in S_small_old with p < i and A[p] <= A[i]) 
    #            - (Count of j in S_large_old with j > i)
    #
    #    We need to efficiently query these counts.
    #    We can maintain a Fenwick tree for S_small (based on indices) and another for S_large (based on indices).
    #    Actually, we need:
    #      1. Count of j in S_large_old with j > i. This is simply (Total in S_large_old) - (Count of j in S_large_old with j <= i).
    #         We can maintain a BIT over indices for S_large.
    #      2. Count of p in S_small_old with p < i and A[p] <= A[i].
    #         This requires a 2D structure or careful ordering.
    #         Notice that we process elements in increasing order of A[i] (since A[i] = M - 1 - k decreases as k increases? No, k increases, so M-1-k decreases).
    #         Wait, the set of elements moving is defined by A[i] = M - 1 - k.
    #         As k goes 0 -> M-1, the required A[i] goes M-1 -> 0.
    #         So we process elements with large A[i] first, then small A[i].
    #         When we process a batch of elements with the same A[i], they all move simultaneously.
    #         Within the same batch, the relative order of A[p] <= A[i] is tricky because A[p] = A[i] for p in the same batch.
    #         Condition A[p] <= A[i] includes p in the same batch.
    #         For p in the same batch (A[p] == A[i]):
    #           Before: Both in S_small. Inversion if p < i and A[p] > A[i] -> False (equal). So 0 inversions.
    #           After: p in S_small, i in S_large. Inversion if p < i. Always true.
    #           So for p in same batch with p < i, we add 1.
    #         For p in previous batches (A[p] < A[i]):
    #           Before: Inversion if p < i and A[p] > A[i] -> False (since A[p] < A[i]). So 0 inversions.
    #           After: Inversion if p < i. Always true.
    #           So for p in previous batches with p < i, we add 1.
    #         So effectively, for all p in S_small_old with p < i, we add 1.
    #         Wait, let's re-verify "Before: Inversion if p < i and A[p] > A[i]".
    #         If A[p] < A[i], then A[p] > A[i] is false. So 0 inversions.
    #         If A[p] == A[i], then A[p] > A[i] is false. So 0 inversions.
    #         So yes, for ALL p in S_small_old with p < i, the contribution changes from 0 to 1.
    #         So we just need count of p in S_small_old with p < i.
    #
    #    Revised Delta for element i:
    #      Delta = (Count of p in S_small_old with p < i) - (Count of j in S_large_old with j > i)
    #
    #    This simplifies things greatly!
    #    We need two BITs:
    #      BIT_small: Tracks indices of elements currently in S_small.
    #      BIT_large: Tracks indices of elements currently in S_large.
    #
    #    Algorithm:
    #      1. Initialize BIT_small with all indices 1..N.
    #      2. Initialize BIT_large empty.
    #      3. Calculate initial inversions (done).
    #      4. Group indices by A[i]. Let groups be G[v] = list of indices where A[i] == v.
    #      5. Iterate k from 0 to M-1:
    #           a. Identify elements to move: those with A[i] == M - 1 - k.
    #           b. For each such element i:
    #              - Query BIT_small for count of indices < i. Let this be C1.
    #              - Query BIT_large for count of indices > i. Let this be C2.
    #                (C2 = total_in_large - query_large(i))
    #              - Update total_inversions += C1 - C2.
    #              - Move i from BIT_small to BIT_large (update BIT_small -1, BIT_large +1).
    #           c. Print total_inversions.
    #
    #    Wait, is the order of processing within the batch important?
    #    The formula Delta = C1 - C2 assumes that when we process i, the state of BIT_small reflects S_small_old (before any of the batch moves) and BIT_large reflects S_large_old.
    #    If we move elements one by one, the state changes.
    #    However, the condition "p in S_small_old" means p is in S_small BEFORE the batch moves.
    #    So we must calculate C1 and C2 for ALL elements in the batch using the state BEFORE the batch moves, then update the BITs.
    #    So:
    #      1. Identify batch W = {i | A[i] == M - 1 - k}.
    #      2. For each i in W:
    #           C1 = query_small(i - 1)
    #           C2 = query_large(N) - query_large(i)
    #           inv += C1 - C2
    #      3. For each i in W:
    #           update_small(i, -1)
    #           update_large(i, 1)
    #
    #    This looks correct and O(N log N) total.

    # Group indices by value
    groups = [[] for _ in range(M)]
    for idx, val in enumerate(A):
        groups[val].append(idx + 1) # 1-based index

    # BITs
    bit_small = FenwickTree(N)
    bit_large = FenwickTree(N)
    
    # Initialize bit_small with all indices
    for i in range(1, N + 1):
        bit_small.update(i, 1)
        
    # Process k from 0 to M-1
    results = []
    
    for k in range(M):
        # Elements to move: A[i] == M - 1 - k
        target_val = M - 1 - k
        if target_val < 0:
            # Should not happen given constraints and loop range, but safety
            continue
            
        batch = groups[target_val]
        
        # Calculate changes
        current_inv = initial_inversions
        for i in batch:
            # Count p in S_small with p < i
            c1 = bit_small.query(i - 1)
            
            # Count j in S_large with j > i
            # Total in large is bit_large.query(N)
            total_large = bit_large.query(N)
            c2 = total_large - bit_large.query(i)
            
            current_inv += (c1 - c2)
        
        results.append(current_inv)
        
        # Update BITs
        for i in batch:
            bit_small.update(i, -1)
            bit_large.update(i, 1)

    # Output results
    for res in results:
        print(res)

if __name__ == '__main__':
    solve()