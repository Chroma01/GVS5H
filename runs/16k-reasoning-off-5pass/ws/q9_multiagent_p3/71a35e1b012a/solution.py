import sys

# Increase recursion depth just in case, though we use iterative segment tree
sys.setrecursionlimit(2000000)

class SegTreeTuple:
    def __init__(self, size):
        # Size needs to cover up to 'size'. 
        # We use 1-based indexing for logic, so size should be at least N+1.
        self.n = 1
        while self.n < size:
            self.n *= 2
        # Initialize with (-1, -1) representing no value
        self.tree = [(-1, -1)] * (2 * self.n)

    def update(self, pos, value):
        # pos is 1-based
        # value is a tuple (val, index)
        idx = pos + self.n - 1
        if value > self.tree[idx]:
            self.tree[idx] = value
            idx //= 2
            while idx > 0:
                self.tree[idx] = max(self.tree[2*idx], self.tree[2*idx+1])
                idx //= 2

    def query(self, l, r):
        # Query max in [l, r] (1-based inclusive)
        if l > r:
            return (-1, -1)
        l += self.n - 1
        r += self.n - 1
        res = (-1, -1)
        while l <= r:
            if l % 2 == 1:
                if self.tree[l] > res:
                    res = self.tree[l]
                l += 1
            if r % 2 == 0:
                if self.tree[r] > res:
                    res = self.tree[r]
                r -= 1
            l //= 2
            r //= 2
        return res

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    # Tree 1: For Type 1. At index L, store max R.
    # Query: max R in range [1, curr]
    tree1 = SegTreeTuple(N + 1)
    
    # Tree 2: For Type 2 (suffix coverage). At index L, store max L.
    # We want Type 2 with L > curr. So query range [curr+1, N].
    # Value stored is L itself.
    tree2 = SegTreeTuple(N + 1)
    
    # Tree 3: For Type 2 (prefix/suffix coverage). At index R, store max L.
    # We want Type 2 with R < curr. So query range [1, curr-1].
    # Value stored is L.
    tree3 = SegTreeTuple(N + 1)
    
    # We need to store the operations to fill the trees
    # Since we need to output the sequence of operations, we need to know which index corresponds to which op
    # But the problem asks for the sequence of operations for i=1 to M.
    # So we need to store the chosen type for each index.
    
    # Let's read and build trees
    # We also need to keep track of which index we are at to fill the answer array later?
    # No, the answer array is initialized to 0. We just need to set ans[idx] = type.
    
    ans = [0] * M
    
    for i in range(M):
        L = int(next(iterator))
        R = int(next(iterator))
        
        # Type 1: covers [L, R]
        # Update tree1 at L with (R, i)
        tree1.update(L, (R, i))
        
        # Type 2: covers [1, L-1] U [R+1, N]
        # Update tree2 at L with (L, i) -> used for L > curr query
        tree2.update(L, (L, i))
        # Update tree3 at R with (L, i) -> used for R < curr query
        tree3.update(R, (L, i))
        
    curr = 1
    possible = True
    
    while curr <= N:
        best_val = -1
        best_idx = -1
        best_type = -1
        
        # Option 1: Type 2 with R < curr
        # Covers [curr, N]. New start N+1.
        # Query tree3 in [1, curr-1] -> returns (L, idx)
        cand3 = tree3.query(1, curr - 1)
        if cand3[0] != -1:
            # This covers [curr, N], so new start is N+1.
            best_val = N + 1
            best_idx = cand3[1]
            best_type = 2
            # Since this finishes the problem, we don't need to check others.
            # But we must ensure we pick the one that maximizes L? 
            # The query returns the max L. So this is optimal for this category.
            # And N+1 is the absolute maximum possible start.
            pass
        
        if best_val == -1:
            # Option 2: Type 2 with L > curr
            # Covers [curr, L-1] and [R+1, N]. New start L.
            # Query tree2 in [curr+1, N] -> returns (L, idx)
            cand2 = tree2.query(curr + 1, N)
            if cand2[0] != -1:
                # Compare with current best (which is -1)
                if cand2[0] > best_val:
                    best_val = cand2[0]
                    best_idx = cand2[1]
                    best_type = 2
        
        if best_val == -1:
            # Option 3: Type 1 with L <= curr <= R
            # Covers [curr, R]. New start R+1.
            # Query tree1 in [1, curr] -> returns (R, idx)
            cand1 = tree1.query(1, curr)
            if cand1[0] != -1 and cand1[0] >= curr:
                # New start is R+1
                new_start = cand1[0] + 1
                if new_start > best_val:
                    best_val = new_start
                    best_idx = cand1[1]
                    best_type = 1
        
        if best_val == -1:
            possible = False
            break
        
        ans[best_idx] = best_type
        curr = best_val

    if not possible:
        print("-1")
    else:
        cost = sum(1 for x in ans if x != 0)
        print(cost)
        print(*(ans))

if __name__ == '__main__':
    solve()