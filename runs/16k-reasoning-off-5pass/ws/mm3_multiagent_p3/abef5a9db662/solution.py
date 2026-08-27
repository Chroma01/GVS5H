import sys

def solve():
    import sys
    sys.setrecursionlimit(1 << 25)
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    intervals = [(int(next(it)), int(next(it))) for _ in range(N)]
    Q = int(next(it))
    queries = [int(next(it)) for _ in range(Q)]

    MAX_RATING = 500000
    # We consider ratings up to MAX_RATING + N because rating can increase by at most N.
    M = MAX_RATING + N + 5

    # to[x] = final rating when starting from x (0-indexed for convenience)
    # Initialize to[x] = x
    to = list(range(M))

    # Fenwick tree (BIT) for range max query.
    # We need to support:
    #   - range max on [l, r]
    #   - point update: set value at pos p to new_val
    # BIT for range max: classic BIT can support prefix max; for range max we need segment tree.
    # Simpler: use segment tree.
    class SegTree:
        __slots__ = ('n', 'size', 'tree')
        def __init__(self, n):
            self.n = n
            size = 1
            while size < n:
                size <<= 1
            self.size = size
            self.tree = [0] * (2 * size)
            # Build: set each leaf to its index (0-indexed)
            for i in range(n):
                self.tree[size + i] = i
            for i in range(size - 1, 0, -1):
                self.tree[i] = max(self.tree[2*i], self.tree[2*i+1])
        def range_max(self, l, r):
            # inclusive l, r, 0-indexed
            if l > r:
                return -10**9
            l += self.size
            r += self.size
            res = -10**9
            while l <= r:
                if (l & 1) == 1:
                    res = max(res, self.tree[l])
                    l += 1
                if (r & 1) == 0:
                    res = max(res, self.tree[r])
                    r -= 1
                l >>= 1
                r >>= 1
            return res
        def point_update(self, p, val):
            # set position p (0-indexed) to val
            p += self.size
            self.tree[p] = val
            p >>= 1
            while p:
                self.tree[p] = max(self.tree[2*p], self.tree[2*p+1])
                p >>= 1

    seg = SegTree(M)

    # Process contests from last to first
    for L, R in reversed(intervals):
        # Find the maximum final rating achievable if we start at any value in [L, R]
        # after processing the current contest.
        # Actually, we need to update to[x] for x in [L, R] to be to[x+1] (i.e., shift).
        # The current `to` array represents the final rating after processing all contests *after* the current one.
        # So for x in [L, R], the final rating after this contest should be to[x+1].
        # We need to find for each x in [L, R], the value of to[x+1] and set it as the new final rating.
        # But we can't iterate over all x in [L, R] individually (too large).
        # Instead, we observe: for x in [L, R], to[x] = to[x+1] after this contest.
        # This means the `to` array becomes a "shifted" version on [L, R].
        # We can compute the maximum of to on [L+1, R+1] (since we need to_x+1 values).
        # But to[x+1] varies; we need to actually update all positions.
        # However, note that queries only ask for final rating given X, and we have M up to 500k+N ~ 700k.
        # Direct iteration over all M for each contest would be O(N*M) which is too large.
        # The typical solution uses a segment tree to quickly find the smallest x in [L, R] such that to[x] != x (i.e., to[x] = to[x+1]),
        # and then updates to[x] = to[x+1] for all x in [L, R].
        # This is exactly the "smallest to[x] != x" search.
        # Let's find the leftmost position p in [L, R] where to[p] != p. Actually we need to find all positions where to[x] != x+1?
        # The update is: for all x in [L, R], to[x] = to[x+1].
        # Note that to[x+1] >= to[x] (monotonic). Actually to is non-decreasing.
        # We can process from right to left: for x from R down to L: to[x] = to[x+1].
        # This can be done efficiently if we know where to[x] is "affected".
        # A known approach: maintain a DSU (union-find) to skip already processed positions,
        # and for each contest, iterate over x in [L, R] that are "alive", and set to[x] = to[x+1], then mark x as processed.
        # Complexity: each x is updated at most once? Actually each x can be updated many times.
        # Wait, the union-find approach is used for a different problem (interval covering).
        # Let's reconsider: we have a segment tree of to values.
        # For a given interval [L, R], we want to set to[x] = to[x+1] for all x in [L, R].
        # This is a range "shift right" operation.
        # We can find the maximum value in [L, R] after the operation, but we need to update all.
        # Alternatively, we can observe that the process of updating to on [L, R] to to on [L+1, R+1] can be done by:
        #   - to[L] = to[L+1]
        #   - to[L+1] = to[L+2]
        #   - ...
        #   - to[R] = to[R+1]
        # Since to is non-decreasing, to[x+1] >= to[x].
        # We can process from right to left: to[x] = to[x+1].
        # To do this efficiently, we can find the smallest x in [L, R] such that to[x] != to[x+1]? Not exactly.
        # Actually, we need to find the leftmost position in [L, R] that still has to[x] = x (i.e., not yet shifted).
        # If to[x] = x and to[x+1] = x+1, then after shift, to[x] becomes x+1, and to[x+1] remains x+1.
        # But this is still per-position.
        # Let's think differently: we can precompute the final rating function f(x) = final rating from start x.
        # It is known that f(x) is non-decreasing and f(x) >= x.
        # The process backwards: f_N(x) = x (no contests).
        # For contest i with interval [L_i, R_i], we have:
        #   f_i(x) = f_{i+1}(x) if x not in [L_i, R_i] OR (x in [L_i, R_i] and f_{i+1}(x+1) = f_{i+1}(x) ?)
        # Actually the recurrence: f_i(x) = f_{i+1}(x+1) if x in [L_i, R_i], else f_{i+1}(x).
        # So f_i(x) = f_{i+1}(x) + (1 if x in [L_i, R_i] and f_{i+1}(x) < f_{i+1}(x+1) ?)
        # Wait, the condition is: if x in [L_i, R_i], we do x -> x+1, then process rest.
        # So f_i(x) = f_{i+1}(x+1) if x in [L_i, R_i], else f_{i+1}(x).
        # But note: f_{i+1}(x+1) might be equal to f_{i+1}(x) in some cases (if the increment doesn't propagate).
        # Actually, since f_{i+1} is non-decreasing, f_{i+1}(x+1) >= f_{i+1}(x).
        # If x in [L_i, R_i], then f_i(x) = f_{i+1}(x+1).
        # This is exactly: for x in [L_i, R_i], f_i(x) = f_{i+1}(x+1).
        # So the update is: for all x in [L_i, R_i], f(x) = f(x+1).
        # We need to perform these updates on the array f (which is `to`) efficiently.
        # Since M <= 700,000 and N <= 200,000, we could do O(M) per update? No, that's O(N*M).
        # We need to update the segment tree to reflect these range shifts.
        # The range shift "to[x] = to[x+1]" for x in [L, R] can be seen as:
        #   to[x] = max(to[x], to[x+1])? No, it's to[x] = to[x+1].
        # But since to is non-decreasing, to[x+1] >= to[x], so to[x] = to[x+1] is equivalent to to[x] = max(to[x], to[x+1]).
        # Wait, is that true? If to[x] <= to[x+1], then to[x] = to[x+1] means to[x] becomes larger (or stays same).
        # Actually, we are overwriting to[x] with to[x+1]. Since to[x+1] >= to[x], the new to[x] is >= old to[x].
        # And because to[x+1] >= to[x], setting to[x] = to[x+1] is exactly to[x] = max(to[x], to[x+1]).
        # But is that enough? We need to ensure that after setting to[x] = to[x+1], the array remains non-decreasing.
        # Suppose we have to[x-1] <= to[x] and to[x+1] >= to[x]. After update, to[x] becomes to[x+1] which is >= to[x] >= to[x-1], so monotonicity holds.
        # However, setting to[x] = max(to[x], to[x+1]) for all x in [L, R] is a range "chmax" (range max assignment) operation.
        # But we need exactly to[x] = to[x+1], not max(to[x], to[x+1]). If to[x] < to[x+1], then max(to[x], to[x+1]) = to[x+1] which is correct.
        # If to[x] >= to[x+1], then max(to[x], to[x+1]) = to[x], but we need to[x] = to[x+1]. However, can to[x] >= to[x+1] happen?
        # Since to is non-decreasing, to[x] <= to[x+1] always! So to[x] >= to[x+1] never happens. Therefore, to[x] <= to[x+1] always.
        # Thus, to[x] = to[x+1] is equivalent to to[x] = max(to[x], to[x+1]).
        # And since to[x] <= to[x+1], this is exactly a range "chmax" operation where we raise values to at least the next value.
        # But we need to set to[x] exactly to to[x+1], not just >= to[x+1]. However, because to[x] is already <= to[x+1],
        # setting to[x] = to[x+1] is exactly setting to[x] = to[x+1] (which is the max of the two).
        # So the update "for all x in [L, R]: to[x] = to[x+1]" is exactly equivalent to "for all x in [L, R]: to[x] = max(to[x], to[x+1])".
        # But wait, this is for each x individually. If we apply to[x] = max(to[x], to[x+1]) for all x in [L, R], does it give the same result as iterating from right to left?
        # Let's check: suppose to[L]=5, to[L+1]=10, to[R]=20.
        # Right-to-left: to[R]=to[R+1], to[R-1]=to[R], ..., to[L]=to[L+1].
        # If we do to[x] = max(to[x], to[x+1]) for all x:
        #   to[R] = max(to[R], to[R+1]) = to[R+1] (if to[R+1] > to[R]).
        #   to[R-1] = max(to[R-1], to[R]) (but to[R] is now updated to to[R+1], so it's max(to[R-1], to[R+1])).
        #   This is not the same as the original shift! The original shift sets to[R-1] to to[R] (which was old to[R+1]), not to[R+1].
        # Wait, the original shift is: new_to[x] = old_to[x+1]. It does not depend on the order of updates.
        # If we compute new_to[x] = old_to[x+1] for all x in [L, R], then we can just set them.
        # But we want to do it incrementally as we process contests backwards.
        # At the time we process contest i, the array `to` holds the values of f_{i+1} (final ratings after contests i+1..N).
        # We need to compute f_i from f_{i+1} by: f_i(x) = f_{i+1}(x+1) if x in [L_i, R_i], else f_{i+1}(x).
        # So we need to set f_i(x) = f_{i+1}(x+1) for x in [L_i, R_i].
        # This is a range update where for each x, we read the value at x+1 and write it to x.
        # We cannot do this in O(1) or O(log M) per x if we have many x.
        # But notice that f_{i+1} is non-decreasing. So f_{i+1}(x+1) >= f_{i+1}(x).
        # We need to find, for each x in [L_i, R_i], the value f_{i+1}(x+1).
        # This is like shifting the array to the right by 1 in that range.
        # The key observation: if f_{i+1}(x) = f_{i+1}(x+1), then setting f_i(x) = f_{i+1}(x+1) changes nothing (f_i(x) = f_{i+1}(x)).
        # So only positions where f_{i+1}(x) < f_{i+1}(x+1) are actually changed.
        # Moreover, f_{i+1}(x) < f_{i+1}(x+1) means that starting at x, the final rating is strictly less than starting at x+1.
        # We can find the first position in [L_i, R_i] where f_{i+1}(x) < f_{i+1}(x+1), and then propagate.
        # Actually, the standard solution for this problem (AtCoder ABC 274 F? or similar) is:
        # Preprocess an array `next[x]` = final rating from x, using a segment tree to find the next "jump".
        # Let's recall the exact algorithm:
        # We process contests in reverse.
        # Maintain a segment tree over ratings 1..MAX. Each leaf holds the value f(x) (current final rating if we start at x).
        # Initially, f(x) = x.
        # For each contest [L, R] (processing backwards), we want to update f(x) for x in [L, R] to f(x+1).
        # This is equivalent to: for x in [L, R], f(x) = f(x+1).
        # Since f is non-decreasing, f(x+1) >= f(x).
        # We can find the maximum value in [L+1, R+1] of f, call it M_val.
        # Then for all x in [L, R], f(x) becomes max(f(x), M_val)? No.
        # Actually, consider the rightmost point in [L, R]. We need f(R) = f(R+1). So f(R) must be at least f(R+1).
        # Since f(R) <= f(R+1) (monotonicity), f(R) becomes exactly f(R+1).
        # For x = R-1, f(R-1) becomes f(R) (which is now f(R+1)).
        # So essentially, for all x in [L, R], f(x) becomes f(R+1) (the value at the right boundary + 1).
        # Wait, is that true? Let's test:
        # Before update: f(L), f(L+1), ..., f(R), f(R+1).
        # After update: f(L) = f(L+1) = ... = f(R) = f(R+1).
        # So yes! All positions in [L, R] take the value of f(R+1) (the first position to the right of the interval).
        # Because f is non-decreasing, f(R+1) is the maximum value in the range [L, R+1].
        # And since f(x) <= f(R+1) for all x in [L, R] (by monotonicity), setting f(x) = f(R+1) for all x in [L, R] satisfies f(x) = f(x+1) recursively.
        # Let's verify: f(R) = f(R+1). f(R-1) becomes f(R) which is f(R+1). By induction, all become f(R+1).
        # So the update is simply: for all x in [L, R], f(x) = f(R+1).
        # This is a range "chmax" (range max assignment) to the value f(R+1).
        # Since we need to set the values to exactly f(R+1), and f(x) <= f(R+1) for all x in [L, R],
        # this is exactly a range chmax operation: f(x) = max(f(x), f(R+1)).
        # And we can do this efficiently with a segment tree that supports range chmax!
        # A segment tree can support range chmax and point queries, or we can use a lazy propagation segment tree for range chmax.
        # However, we also need to know f(R+1). We can query the segment tree for the value at R+1.
        # Wait, but after we update the range [L, R] to f(R+1), the value at R+1 itself doesn't change (it stays f(R+1)).
        # So the update is: query the value at position R+1 (call it v), then apply range chmax on [L, R] with value v.
        # This will set all positions in [L, R] to at least v. Since they were <= v, they become exactly v.
        # This is O(log M) per contest! Total O(N log M) which is about 200k * 20 = 4M operations.
        # Then for each query X, we just output the value f(X) from the segment tree.
        # This is perfect.
        # Let's implement the segment tree with range chmax and point query.
        # Actually, we need to be able to query the value at a point (R+1) and also query the value at X for queries.
        # We can build a segment tree that supports:
        #   - range chmax(l, r, val): set a[i] = max(a[i], val) for i in [l, r]
        #   - point query: get a[i]
        # We can use a lazy propagation segment tree where each node stores the current maximum in its segment.
        # For range chmax, we need to update nodes. The standard trick for range chmax with lazy propagation:
        #   - If val <= node.max, we can't do anything.
        #   - If val >= node.second_max, we can set the entire node to val (since all values are <= val and > second_max? Actually, if we have values [a, b, c], max is c, second max is b. If val >= b, then after chmax with val, the max becomes val, but the other values might also increase if they are < val. But we only want to increase values that are < val. This is complex.
        # Actually, we can use a simpler approach: since we only need point queries and range chmax, we can use a BIT of some sort? No.
        # Wait, the operation is: set a[i] = max(a[i], v) for i in [L, R].
        # We need to do this many times, and finally we need point queries.
        # There is a data structure: "Segment Tree Beats" that supports range chmax efficiently (O(log M) amortized).
        # But we can also use a simpler method because the values are monotonic and we only care about point queries.
        # Alternatively, we can process the updates differently.
        # Let's think: we have an array f initially f[i] = i.
        # We process N intervals in reverse. For each interval [L, R], we set f[i] = f[R+1] for all i in [L, R].
        # This means that f becomes a step function. The array f is non-decreasing.
        # The operation "set f[i] = v for all i in [L, R]" where v = f[R+1].
        # This is like "fill" operation. We can maintain the array f using a union-find (disjoint set union) to skip already filled positions.
        # Specifically, we can iterate x from L to R, and for each x that hasn't been set to the new value yet, we set it.
        # But we need to set them all to the same value v. Actually, we can just set f[x] = v and then we don't need to process them again?
        # Wait, f is a global array. When we process a new contest, we might need to set a range to a new value.
        # If we use DSU to skip positions that already have the correct value? Not exactly.
        # Another approach: we can precompute the final f using a segment tree with range "assign" (set to value if smaller).
        # But we can do it with a simple segment tree if we maintain the maximum value in the segment.
        # Actually, since we are setting a range to a specific value v (where v is the current value at R+1),
        # we can do a range update that sets the value to v.
        # This is a range "set to v" operation, but only for positions where the current value is <= v.
        # Since we know that for all i in [L, R], f[i] <= f[R+1] = v, we can safely set them to v.
        # So we need a data structure that supports "range set to v" for all positions in [L, R] (where we know they are <= v),
        # and point queries.
        # This is exactly a range assignment operation. We can use a lazy segment tree for range assignment and point queries.
        # But we need to be careful: after we assign [L, R] to v, the values in [L, R] become v.
        // Then for the next contest, when we query R+1, we get the correct value.
        // We can use a segment tree that supports range assignment (lazy) and point query.
        // However, range assignment is O(log M) per update, which is fine.
        // But we need to be careful: the assignment is "set to v" only if we know the current value is <= v.
        // We can just do unconditional range assignment to v? No, because for positions outside [L, R], we don't want to change them.
        // For positions inside [L, R], we know f[i] <= f[R+1] = v. So we can safely set them to v.
        // But wait, what if some position in [L, R] was already set to v by a previous contest? Then setting it to v again is fine.
        // So we can simply do: range assign [L, R] to v.
        // But is it always true that f[i] <= f[R+1] for i in [L, R]?
        // Yes, because f is non-decreasing. f[i] <= f[R] <= f[R+1].
        // So range assign [L, R] to v where v = f[R+1] is correct.
        // However, we must be careful: we need to query f[R+1] *before* we update the range [L, R] (if R+1 is inside the range, but R+1 is outside [L, R] because the interval is [L, R] inclusive, so R+1 is not in the range).
        // Actually, R+1 is the first index to the right of the interval. It is not affected by the current update.
        // So we can query the segment tree at R+1 to get v, then range assign [L, R] to v.
        // This works perfectly! The segment tree can support range assignment and point query.
        // Since we only need point queries at the end (for Q up to 300k), we can do range assignment and then read the values.
        // Let's build a segment tree that supports:
        //   - point update: set value at index i
        //   - range assign: set all values in [l, r] to v
        //   - point query: get value at index i
        // Actually, we can just use a Fenwick tree or just an array if we do the DSU trick.
        // But segment tree with lazy propagation is straightforward and fast enough (N log M = 200k * 20 = 4M).
        // Let's implement a segment tree with range assign and point query.
        // But wait, we need to read f[R+1] which is a point query.
        // Then we do range assign [L, R] to v.
        // This is O(log M) per contest.
        // Then for each query X, we do a point query to get f[X].
        // Total complexity: O((N + Q) log M) which is about 500k * 20 = 10M operations. Very fast.
        // Let's code this.

        # First, build the segment tree.
        # We need to support range assign and point query.
        # We can use a lazy propagation segment tree where each node has a "set" lazy tag.
        # But since we only need point queries, we can also use a simpler approach:
        # Use a segment tree that stores the values, and for range assign, we just set the lazy tag.
        # When we query a point, we traverse down and apply the tags.
        # This is standard.

        # However, there is a catch: the value v = f[R+1] might be larger than 500000 + N.
        # We need the array size to be at least max_R + N + 2 to accommodate all possible ratings.
        # Max rating is 500000 (from input) + N (max increments) = 700000.
        # We have M = MAX_RATING + N + 5 = 700005. That's fine.

        # Let's implement the segment tree.
        pass

    # After processing all contests, we have the final f array in the segment tree.
    # For each query X, we output f[X].
    # We need to collect the output and print.

# This is just a plan. I need to write the actual code.