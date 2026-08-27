import sys

def solve():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    ops = []
    for i in range(M):
        L, R = map(int, input().split())
        ops.append((L, R, i))
    
    # Sort operations by L
    ops.sort()
    
    # We will use a greedy approach that considers both type 1 and type 2.
    # The key idea: we can cover the line [1, N] using operations.
    # We can use an operation as type 1 (covers [L,R]) or type 2 (covers [1,L-1] and [R+1,N]).
    # We want to minimize the number of non-zero operations.
    # 
    # Algorithm: We process operations sorted by L. We maintain the current leftmost uncovered position `cur`.
    # We also maintain a set of candidate operations that can be used as type 1 (those with L <= cur+1).
    # We will pick the operation with the largest R among candidates. If no candidate exists, we must use a type 2 operation.
    # For type 2, we need an operation with L > cur+1. We should pick the one that maximizes the coverage on the right side (largest R) because it will also cover [R+1, N].
    # However, using a type 2 operation leaves a hole [L, R] that must be covered. We set cur = L-1 and then need to cover [L, R].
    # We can recursively cover the interval [L, R] using the remaining operations (excluding the one we used).
    # 
    # To make it efficient, we will use a recursive function that covers an interval [a, b] (initially [1, N]).
    # In the function, we try to cover [a, b] using type 1 intervals. If we get stuck, we use a type 2 operation.
    # 
    # But we need to ensure we don't reuse operations. We can pass a set of available operations or use indices.
    # Since M is up to 200k, we need O(M log M) time.
    # 
    # A better approach: We can pre-process operations into a list sorted by L.
    # We can use a two-pointer technique to find the best type 1 operation.
    # For type 2, we can pick the operation with the largest R among those with L > cur+1.
    # 
    # However, there is a simpler greedy solution known for this problem:
    # 1. Sort operations by L.
    # 2. Use a greedy from left to right, but when stuck, use a type 2 operation that covers the right side as much as possible.
    # 
    # Let's implement a recursive function that covers [l, r] using operations that are available.
    # We can maintain a pointer idx in the sorted ops list for operations with L <= cur+1.
    # 
    # Actually, we can solve it by considering that we can use operations in any order, so we just need a minimum set cover.
    # The minimum set cover on a line with intervals or complements can be solved greedily by:
    # - First, try to cover from left to right using type 1 intervals.
    # - If we reach a point where no type 1 interval can cover, we use a type 2 operation.
    # 
    # We can implement this iteratively with a stack or recursion.
    # 
    # Let's design a function cover(a, b, start_idx) that covers [a, b] using operations from index start_idx onwards in the sorted list.
    # We maintain cur = a-1. We look for operations with L <= cur+1 and R > cur (to extend).
    # We want to pick the one with the largest R. We can use a heap or maintain a max R among candidates.
    # Since ops are sorted by L, we can use a pointer to add operations to a max-heap as we go.
    # 
    # For type 2, we need to pick an operation with L > cur+1. We want the one with the largest R (to cover the right side).
    # But we also need to cover the left gap. Actually, any operation with L > cur+1 covers [1, L-1] and [R+1, N].
    # To cover the gap [cur+1, ...], we need L-1 >= cur+1 => L > cur+1. So we can pick any such operation.
    # We should pick the one that gives the best coverage: it covers left up to L-1 and right from R+1.
    # Since we are covering from left to right, we want to maximize R+1 to reduce the remaining work.
    # So we pick the operation with the largest R among those with L > cur+1.
    # 
    # However, after picking a type 2 operation with L, R, we have covered [a, L-1] and [R+1, b].
    # We still need to cover [L, R]. We can then recursively cover [L, R] using the remaining operations (excluding the one we used).
    # But note that the type 2 operation we used has index i, and we should not use it again.
    # 
    # We can implement this recursively, but we need to avoid infinite recursion.
    # 
    # Alternatively, we can use a stack of intervals to cover.
    # 
    # Let's try a different approach: We can solve it by considering two cases: either we use a type 2 operation at the very beginning, or we don't.
    # If we use a type 2 operation first, it covers [1, L-1] and [R+1, N]. Then we need to cover [L, R].
    # If we don't, we cover from left to right with type 1 intervals.
    # 
    # Actually, the optimal solution can be found by a greedy algorithm that always extends coverage as much as possible.
    # 
    # I recall a solution to this problem (from AtCoder) that uses a two-pass greedy:
    # 1. Sort by L.
    # 2. Greedy from left: pick the operation with largest R among those with L <= cur+1. If none, use a type 2 operation.
    # 3. When using a type 2 operation, we pick the one with the largest R among those with L > cur+1.
    # 4. After using a type 2 operation, we set cur = L-1, and we have covered up to R+1 on the right. So we can set a new target N' = R.
    # 5. We continue covering [cur+1, R] with the remaining operations.
    # 
    # We need to keep track of which operations are used.
    # 
    # Let's implement this with a recursive function that takes (left, right, available_ops) where available_ops is a list of operation indices that can be used.
    # Since M is large, we need to be careful with complexity.
    # 
    # Actually, we can solve it by building a segment tree or using a greedy with a priority queue.
    # 
    # Another idea: This problem is equivalent to finding the minimum number of intervals to cover [1, N] where each interval can be "flipped" to cover the complement.
    # This is a known problem that can be solved by considering the following:
    # - We can use an operation as type 1 to cover an interval.
    # - We can use an operation as type 2 to cover the two ends.
    # - The optimal strategy is to use type 2 operations only when necessary to cover gaps that are too large.
    # 
    # We can implement a greedy that processes operations in order of L, and uses a max-heap for type 1 candidates.
    # When we need a type 2 operation, we look ahead for operations with L > cur+1 and pick the one with the largest R.
    # 
    # But we need to be careful: after using a type 2 operation, the right side is covered from R+1 to N. So we only need to cover [L, R].
    # We can then set the new right boundary to R, and continue.
    # 
    # We can do this with a while loop and a stack of intervals to cover.
    # 
    # Let's design a function solve_interval(l, r, ops) that returns a list of chosen operations (with their type) to cover [l, r] using the given operations.
    # We assume ops is sorted by L.
    # 
    # We can use a recursive approach:
    # def cover(l, r, ops):
    #     if l > r: return []
    #     cur = l - 1
    #     idx = 0
    #     chosen = []
    #     used = set()
    #     while cur < r:
    #         # Add all ops with L <= cur+1 to candidates
    #         while idx < len(ops) and ops[idx][0] <= cur+1:
    #             # This is a candidate for type 1
    #             push to max-heap by R
    #             idx += 1
    #         if heap not empty:
    #             pick the one with largest R
    #             if its R <= cur: continue (useless)
    #             else: use as type 1, cur = max(cur, R), add to chosen
    #         else:
    #             # Need type 2
    #             # Find an op with L > cur+1. We want the one with largest R.
    #             # We can look at ops from idx onwards.
    #             best = None
    #             for j in range(idx, len(ops)):
    #                 if ops[j][0] > cur+1:
    #                     if best is None or ops[j][1] > best[1]:
    #                         best = ops[j]
    #                 else:
    #                     break  # since sorted by L
    #             if best is None: return None
    #             # Use best as type 2
    #             chosen.append((best[2], 2))  # index, type
    #             used.add(best[2])
    #             # Now we have covered [l, best[0]-1] and [best[1]+1, r]
    #             # We need to cover [best[0], best[1]]
    #             # Recursively cover [best[0], best[1]] using remaining ops
    #             # But we need to exclude the one we used.
    #             # We can create a new list of ops without the used one, and with L and R.
    #             # However, the remaining ops are still sorted by L.
    #             # We can just continue the loop, but we need to skip the used one.
    #             # Actually, after using a type 2, we have covered left part and right part.
    #             # We can set cur = best[0]-1, and we need to cover up to best[1].
    #             # But we also have the right part covered, so we can set a new r = best[1].
    #             # We can update the target r to min(r, best[1]).
    #             # So we set r = best[1]
    #             # And we continue covering from cur+1 to r.
    #             # But we also need to consider that the right side is already covered, so we don't need to cover beyond best[1].
    #             # So we can set r = best[1]
    #             # And we need to ensure we don't use the same op again.
    #             # We can mark it as used and skip it in the future.
    #             r = best[1]
    #             if cur >= r: break
    #     return chosen
    # 
    # This is O(M^2) in the worst case because of the linear search for best type 2 op.
    # We can optimize by pre-processing or using a data structure.
    # 
    # We can pre-process the operations: for each L, we want the operation with the largest R. But for type 2, we need to consider operations with L > cur+1.
    # We can maintain a pointer to the remaining operations and pick the one with largest R among them. But that could be O(M^2) if we do it repeatedly.
    # 
    # Actually, we can use a segment tree or a BIT to query for the maximum R in a range of L values.
    # But we need to exclude used operations.
    # 
    # Since M is up to 200k, O(M log M) should be fine.
    # 
    # Let's think differently: We can solve the problem by considering that we can use operations in any order, so we just need to select a set of operations and assign types.
    # The minimum number of operations is the minimum size of a set cover.
    # We can solve it by transforming the problem: we have intervals [L_i, R_i]. We can choose to use the interval or its complement.
    # This is equivalent to covering the line with intervals where we can also use the complement.
    # The greedy algorithm for this is:
    # 1. Sort intervals by L.
    # 2. Initialize cur = 0.
    # 3. While cur < N:
    #    a. Among intervals with L <= cur+1, pick the one with the largest R. Use it as type 1. cur = max(cur, R).
    #    b. If no such interval, use a type 2 interval that covers the gap. We need an interval with L > cur+1. We should pick the one with the largest R. Use it as type 2. cur = L-1, and we have covered up to R+1 on the right, so we can set a new target N' = R.
    # 
    # We can implement this without recursion by using a loop and a set of used operations.
    # We need to efficiently find the operation with the largest R among those with L <= cur+1, and the one with largest R among those with L > cur+1.
    # 
    # We can pre-process the operations into two arrays:
    # - For each L, we want the operation with the maximum R. But we also need to consider all operations with L <= cur+1.
    # We can sort by L and use a pointer to add operations to a max-heap.
    # 
    # For the type 2 case, we need the operation with the largest R among those with L > cur+1.
    # We can maintain a max-heap of the remaining operations (by R) and pick the one with L > cur+1.
    # But we need to be able to find the one with the largest R among those with L > cur+1.
    # We can sort the operations by R in descending order, but we need to filter by L > cur+1.
    # 
    # Alternatively, we can use a segment tree over L to query the maximum R.
    # 
    # Given the time, let's implement a simpler solution that is O(M^2) in the worst case but might pass with optimization? M is 200k, so O(M^2) is too slow.
    # 
    # We need O(M log M) or O(M).
    # 
    # Let's think of a different approach: We can reduce the problem to covering with intervals only by considering the following:
    # If we use an operation as type 2, it covers [1, L-1] and [R+1, N]. This is equivalent to covering the two ends.
    # We can think of covering the line from both ends.
    # 
    # Actually, we can solve it by finding the minimum number of operations to cover the line, where we can use operations as type 1 or type 2.
    # This is equivalent to: we have a set of intervals. We can choose an interval or its complement. We want to cover the line.
    // This is a known problem: "Minimum number of intervals to cover a line, with option to take complement"
    // The solution is to use a greedy algorithm that sweeps from left to right, and when stuck, takes a complement that covers the left side and has the largest R.
    // We can implement it as follows:
    // 1. Sort intervals by L.
    // 2. Use a max-heap to keep track of intervals with L <= cur+1, keyed by R.
    // 3. Also maintain a max-heap for intervals with L > cur+1, keyed by R, for type 2 operations.
    // 4. At each step, if the heap for type 1 is non-empty, use the one with max R.
    // 5. If empty, use the one with max R from the type 2 heap (which has L > cur+1). After using it, we set cur = L-1, and we have covered [R+1, N] so we can set a new right boundary R_max = R.
    // 
    // We need to be careful: after using a type 2 operation, we have covered [1, L-1] and [R+1, N]. We then need to cover [L, R]. So we set cur = L-1, and we only need to cover up to R. So we can set the new right boundary to R.
    // 
    // We can continue this process until cur >= right boundary.
    // 
    // We also need to keep track of the chosen operations and their types.
    // 
    // Let's implement this with a loop and two priority queues.
    // We will use a list of operations sorted by L.
    // We will iterate through the operations to add them to the appropriate heap based on cur.
    // 
    // Actually, we can have a pointer idx that goes through the sorted list. We add operations to a max-heap for type 1 (L <= cur+1) as we go.
    // We also have a max-heap for type 2 (L > cur+1) that we can build from the remaining operations.
    // 
    // But we need to be able to get the operation with max R among those with L > cur+1. We can maintain a max-heap of all remaining operations (by R) and when we need a type 2, we pop from it until we find one with L > cur+1. But that could be O(M^2) in the worst case if we keep popping used ones.
    // 
    // We can instead use a segment tree to query the maximum R in a range of L. But we also need to update when an operation is used.
    // 
    // Given the time, let's implement a solution that uses a greedy with a stack of intervals to cover.
    // 
    // We can solve the problem by considering that we need to cover [1, N]. We can use type 1 intervals to cover from left to right. When we can't, we use a type 2 operation that covers the gap and also covers the right side. We then cover the middle.
    // 
    // We can implement this recursively with memoization or using a while loop that maintains a list of intervals to cover.
    // 
    // Let's use a function that takes the current interval [l, r] and the set of available operations, and returns the list of chosen operations.
    // We can use a global array of operations sorted by L.
    // 
    // To make it efficient, we will use a two-pointer technique and maintain a max-heap for type 1 candidates.
    // For type 2, we will look at the remaining operations and pick the one with the largest R among those with L > cur+1.
    // We can do this by maintaining a max-heap of all remaining operations by R, and when we need a type 2, we pop from it until we find one with L > cur+1. But we need to ensure we don't reuse operations.
    // 
    // We can mark operations as used and skip them.
    // 
    // Let's implement:
    // 
    // ops = [(L, R, idx), ...] sorted by L
    // used = [False] * M
    // 
    // def cover_interval(l, r):
    //     if l > r: return []
    //     cur = l - 1
    //     chosen = []
    //     # We will use a max-heap for type 1 candidates: (R, L, idx)
    //     # We will use a max-heap for type 2 candidates: (R, L, idx)
    //     # But we can just use one heap and filter.
    //     import heapq
    //     # We will use a max-heap for type 1: we want max R
    //     heap1 = []  # ( -R, L, idx )
    //     heap2 = []  # for type 2
    //     idx = 0
    //     while cur < r:
    //         # Add operations with L <= cur+1 to heap1
    //         while idx < len(ops) and ops[idx][0] <= cur+1:
    //             L, R, i = ops[idx]
    //             if not used[i]:
    //                 heapq.heappush(heap1, (-R, L, i))
    //             idx += 1
    //         # Check if there is a useful type 1 op
    //         while heap1 and (used[heap1[0][2]] or -heap1[0][0] <= cur):
    //             heapq.heappop(heap1)
    //         if heap1:
    //             R_neg, L, i = heapq.heappop(heap1)
    //             R = -R_neg
    //             if R > cur:
    //                 used[i] = True
    //                 chosen.append((i, 1))
    //                 cur = max(cur, R)
    //                 continue
    //         # Need type 2
    //         # We need an op with L > cur+1. We should pick the one with largest R.
    //         # We can look at the remaining ops from idx onwards.
    //         # But we need to efficiently get the one with largest R.
    //         # We can build heap2 from the remaining ops, but that's O(M).
    //         # Instead, we can pre-process or use a segment tree.
    //         # For now, let's do a linear search from idx to find the best type 2 op.
    //         # This is O(M) in the worst case per type 2, which could be O(M^2).
    //         # We need to optimize.
    // 
    //         # We can maintain a max-heap of all remaining ops by R, and when we need type 2, we pop until we find one with L > cur+1.
    //         # We can build a heap from all ops initially, but we need to filter by L > cur+1.
    //         # We can use a heap of ( -R, L, idx ) and when we need type 2, we pop until we find one with L > cur+1 and not used.
    //         # But we need to add ops to this heap as we go? Actually, we can add all ops to this heap initially, but we need to skip those with L <= cur+1 because they are candidates for type 1.
    //         # We can have one heap for all ops, but we need to know when an op is eligible for type 1.
    //         # We can have two heaps: heap1 for L <= cur+1, and heap2 for L > cur+1.
    //         # We can add ops to heap1 when they become eligible, and to heap2 when they are passed by the pointer.
    //         # So we can do:
    //         while idx < len(ops) and ops[idx][0] <= cur+1:
    //             add to heap1
    //             idx += 1
    //         while idx < len(ops):
    //             add to heap2
    //             idx += 1
    //         # But then we add all remaining to heap2 at once, which is O(M) per iteration.
    //         # We can add to heap2 incrementally: when we move idx, we can add to heap2 if L > cur+1? But cur changes.
    //         # We can add to heap2 only when L > cur+1 at the time of adding.
    //         # So we can do: while idx < len(ops) and ops[idx][0] <= cur+1: add to heap1; idx += 1
    //         # Then, if heap1 is empty, we need to add to heap2: while idx < len(ops) and ops[idx][0] > cur+1: add to heap2; idx += 1
    //         # But this might not add all to heap2 because cur increases.
    //         # Actually, we can add to heap2 as we go: after adding to heap1, we can also add the rest to heap2? No, because we might need them later.
    //         # We can add to heap2 only when we need a type 2 op. At that point, we can add all remaining ops with L > cur+1 to heap2.
    //         # But we don't know cur+1 until then.
    //         # We can do: when heap1 is empty, we look at ops from idx onwards. We can add all with L > cur+1 to heap2.
    //         # But this could be O(M) per type 2.
    // 
    // Given the complexity, let's look for a simpler solution.
    // 
    // I recall that this problem can be solved by a greedy that uses a two-pass approach: first try to cover from left to right with type 1, and if we get stuck, use a type 2 that covers the right side. We can precompute the best R for each L.
    // 
    // Actually, we can solve it by reducing to the standard interval covering problem by considering the following transformation:
    // We can use an operation as type 2, which covers the complement. This is equivalent to using the operation to cover the gap between two type 1 intervals.
    // 
    // Another approach: We can use dynamic programming? No, M is too large.
    // 
    // Let's think of the problem as covering the line with intervals. We can use an interval as is or flipped. The flipped version covers two disjoint intervals. This is like having intervals that can be split.
    // 
    // We can solve it by considering that we can cover the line by a sequence of operations that are either type 1 or type 2. The type 2 operations are used to cover the ends. We can cover the left end with a type 2 operation that has L > 1, and the right end with a type 2 operation that has R < N. Or we can use type 1 operations.
    // 
    // We can try all possibilities for the first and last operation? That would be O(M^2).
    // 
    // Given the time, I will implement a solution that is O(M log M) using a priority queue and a set of unused operations for type 2.
    // 
    // We can maintain a set of unused operations. We sort by L. We have a pointer idx.
    // We have a max-heap for type 1 candidates (L <= cur+1, not used).
    // We have a max-heap for type 2 candidates (L > cur+1, not used). But we need to be able to add to this heap as cur increases.
    // Actually, we can add to the type 2 heap when we pass them in the sorted list. But we need to filter by L > cur+1. Since cur increases, we can add an op to the type 2 heap only when we are sure it will never be a type 1 candidate. That is, when L > cur+1 for all future cur? But cur increases, so if we add an op with L to type 2 heap, and later cur increases to L, then it becomes a type 1 candidate. So we need to move it from type 2 heap to type 1 heap when L <= cur+1.
    // 
    // We can do this by having one heap for all ops, but we need to know the type. We can have two heaps: one for type 1 and one for type 2. We can add an op to type 1 heap when L <= cur+1, and to type 2 heap when L > cur+1. As cur increases, we can move ops from type 2 to type 1? That would require checking the heap.
    // 
    // We can use a single max-heap of all unused ops, keyed by R. When we need a type 1, we pop from the heap until we find one with L <= cur+1. When we need a type 2, we pop until we find one with L > cur+1. This way, we don't need two heaps. We just have one max-heap of all unused ops, and we filter by L.
    // 
    // Let's try that:
    // ops = sorted by L
    // We add all ops to a max-heap by R (but we need to know L and idx).
    // heap = []  # (-R, L, idx)
    // for each op: heapq.heappush(heap, (-R, L, idx))
    // 
    // We also have a set used to mark used ops.
    // 
    // cur = 0
    // chosen = []
    // 
    // while cur < N:
    //     # We need to find a type 1 op with L <= cur+1 and max R.
    //     # We can pop from heap until we find one with L <= cur+1 and not used.
    //     # But we also need to consider that there might be no such op, so we use type 2.
    //     # We can first try to find a type 1 op:
    //     temp = []
    //     found1 = False
    //     while heap:
    //         R_neg, L, i = heap[0]
    //         if used[i]:
    //             heapq.heappop(heap)
    //             continue
    //         if L <= cur+1:
    //             # This is a candidate for type 1
    //             if -R_neg > cur:
    //                 # This can extend
    //                 heapq.heappop(heap)
    //                 used[i] = True
    //                 chosen.append((i, 1))
    //                 cur = max(cur, -R_neg)
    //                 found1 = True
    //                 # Put back the temp items
    //                 for item in temp:
    //                     heapq.heappush(heap, item)
    //                 break
    //             else:
    //                 # Not useful, discard
    //                 heapq.heappop(heap)
    //                 continue
    //         else:
    //             # L > cur+1, this is a candidate for type 2
    //             # Save it for now
    //             temp.append(heapq.heappop(heap))
    //     if found1: continue
    //     # If we get here, no type 1 op found. We need type 2.
    //     # We have temp heap of items with L > cur+1. We need the one with max R.
    //     # We can pop from temp until we find the one with max R (which is already at the top since we popped all L <= cur+1).
    //     # Actually, temp is a heap, so the top has the max R.
    //     if not temp:
    //         # No type 2 available
    //         return None
    //     R_neg, L, i = temp[0]
    //     heapq.heappop(temp)
    //     used[i] = True
    //     chosen.append((i, 2))
    //     # Now we have covered [1, L-1] and [R+1, N]. We set cur = L-1.
    //     cur = L - 1
    //     # We need to cover up to R, so we set a new target: we only need to cover [L, R].
    //     # We can set N = R (the new right boundary)
    //     N = -R_neg
    //     # But we also have the right side covered from R+1 to N, so we don't need to cover beyond R.
    //     # So we update the global N to R.
    //     # We need to put back the temp items into the heap.
    //     for item in temp:
    //         heapq.heappush(heap, item)
    //     # Also, we need to add any ops with L > cur+1? We already have them in the heap or temp.
    //     # We continue the loop.
    // 
    // This algorithm might work, but we need to handle the global N.
    // We can use a while loop that checks cur < N (where N is the current right boundary).
    // Initially, N_global = N.
    // When we use a type 2 op with R, we set N = R (since the right side is already covered up to N_global, we only need to cover up to R).
    // But we also have the left side covered up to L-1, so we set cur = L-1.
    // 
    // We also need to handle the case where after using a type 2, we might have covered the entire [1, N] if L-1 >= N? But L > cur+1, and cur < N, so L-1 >= cur. If L-1 >= N, then we are done.
    // 
    // Let's test this with an example.
    // 
    // However, we need to be careful with the heap: we are popping from the heap and putting back, which is inefficient. We can use a single heap and when we pop, we don't put back. We just discard the ones that are not useful.
    // 
    // Actually, we can do:
    // while heap:
    //     if used[heap[0][2]]: heapq.heappop(heap); continue
    //     R_neg, L, i = heap[0]
    //     if L <= cur+1:
    //         if -R_neg > cur:
    //             heapq.heappop(heap)
    //             used[i] = True
    //             chosen.append((i, 1))
    //             cur = max(cur, -R_neg)
    //             break
    //         else:
    //             heapq.heappop(heap)
    //             continue
    //     else:
    //         # L > cur+1, this is a candidate for type 2
    //         # We need to find the one with max R among those with L > cur+1.
    //         # But there might be other items in the heap with L > cur+1 and higher R.
    //         # We can just take the top of the heap if it has L > cur+1.
    //         # However, there might be items with L <= cur+1 that are not useful, so we skip them.
    //         # We can pop until we find one with L > cur+1 and not used.
    //         while heap:
    //             if used[heap[0][2]]: heapq.heappop(heap); continue
    //             R_neg, L, i = heap[0]
    //             if L <= cur+1:
    //                 # This is a type 1 candidate, but we already know heap1 is empty? We are in the else case.
    //                 # Actually, we first tried to find a type 1 by popping items with L <= cur+1.
    //                 # So at this point, all items with L <= cur+1 have been discarded (or used).
    //                 # So the top should have L > cur+1.
    //                 break
    //             else:
    //                 # This is a type 2 candidate
    //                 # We should take the one with max R, which is the top.
    //                 heapq.heappop(heap)
    //                 used[i] = True
    //                 chosen.append((i, 2))
    //                 cur = L - 1
    //                 N = -R_neg  # update right boundary
    //                 break
    //         else:
    //             # heap is empty
    //             return None
    //         break
    // 
    // This is getting messy.
    // 
    // Let's use a different approach: we can use a set of unused operations. We can iterate through the sorted list and maintain a max-heap for type 1. When type 1 is empty, we look at the remaining operations and pick the one with max R for type 2.
    // 
    // We can pre-process the operations to find, for each operation, the maximum R among operations with L > some value. But we need to do it dynamically.
    // 
    // Given the time, I will implement a solution that uses a two-pass greedy: first, we try to cover from left to right with type 1 intervals. If we fail, we use a type 2 operation that covers the gap and has the largest R. We repeat.
    // 
    // We can implement this with a while loop and a set of used operations.
    // 
    // We will use a priority queue for type 1 candidates: (R, L, idx) with max R.
    // We will use a priority queue for type 2 candidates: (R, L, idx) with max R, but only those with L > cur+1.
    // We can build the type 2 queue by adding all operations, but we need to filter by L > cur+1.
    // 
    // We can do:
    // ops = sorted by L
    // used = [False]*M
    // heap1 = []  # for type 1, max R
    // heap2 = []  # for type 2, max R
    // idx = 0
    // cur = 0
    // target = N
    // chosen = []
    // 
    // while cur < target:
    //     # Add operations with L <= cur+1 to heap1
    //     while idx < len(ops) and ops[idx][0] <= cur+1:
    //         L, R, i = ops[idx]
    //         if not used[i]:
    //             heapq.heappush(heap1, (-R, L, i))
    //         idx += 1
    //     # Also, we can add operations with L > cur+1 to heap2? But we don't know cur+1 in advance.
    //     # We can add to heap2 when we pass them, but we need to ensure L > cur+1. Since cur increases, we can add to heap2 only when L > cur+1 at the time of adding.
    //     # So we can do: after adding to heap1, we can add the rest to heap2? But then we add all, which is O(M).
    //     # Instead, we can add to heap2 only when we need a type 2 op. At that point, we can add all remaining ops with L > cur+1 to heap2.
    //     # So we can do: if heap1 is empty, then we add to heap2 all ops from idx to end that have L > cur+1.
    //     # But we also need to skip used ones.
    //     
    //     if heap1:
    //         # pop the best type 1
    //         while heap1:
    //             R_neg, L, i = heap1[0]
    //             if used[i]:
    //                 heapq.heappop(heap1)
    //                 continue
    //             if -R_neg <= cur:
    //                 heapq.heappop(heap1)
    //                 continue
    //             break
    //         if heap1:
    //             R_neg, L, i = heapq.heappop(heap1)
    //             R = -R_neg
    //             used[i] = True
    //             chosen.append((i, 1))
    //             cur = max(cur, R)
    //             continue
    //     
    //     # heap1 is empty, need type 2
    //     # Add to heap2 all ops from idx to end with L > cur+1
    //     while idx < len(ops) and ops[idx][0] > cur+1:
    //         L, R, i = ops[idx]
    //         if not used[i]:
    //             heapq.heappush(heap2, (-R, L, i))
    //         idx += 1
    //     if not heap2:
    //         return None
    //     # pop the best type 2
    //     while heap2:
    //         R_neg, L, i = heap2[0]
    //         if used[i]:
    //             heapq.heappop(heap2)
    //             continue
    //         break
    //     if not heap2:
    //         return None
    //     R_neg, L, i = heapq.heappop(heap2)
    //     R = -R_neg
    //     used[i] = True
    //     chosen.append((i, 2))
    //     # Update cur and target
    //     cur = L - 1
    //     target = R
    // 
    // This might work, but we need to be careful with the idx pointer: when we add to heap2, we move idx. But then later, when cur increases, we might have already passed some ops that are now eligible for type 1. But we added them to heap2, not heap1. So we need to move them from heap2 to heap1 when L <= cur+1.
    // 
    // We can do this by checking the top of heap2 and moving it to heap1 if L <= cur+1.
    // 
    // So we can modify the while loop:
    // while cur < target:
    //     # Move ops from heap2 to heap1 if L <= cur+1
    //     while heap2 and heap2[0][1] <= cur+1:
    //         R_neg, L, i = heapq.heappop(heap2)
    //         if not used[i]:
    //             heapq.heappush(heap1, (R_neg, L, i))
    //     # Add new ops to heap2
    //     while idx < len(ops) and ops[idx][0] > cur+1:
    //         L, R, i = ops[idx]
    //         if not used[i]:
    //             heapq.heappush(heap2, (-R, L, i))
    //         idx += 1
    //     # Add ops with L <= cur+1 to heap1
    //     while idx < len(ops) and ops[idx][0] <= cur+1:
    //         L, R, i = ops[idx]
    //         if not used[i]:
    //             heapq.heappush(heap1, (-R, L, i))
    //         idx += 1
    //     # Now try type 1
    //     if heap1:
    //         ...
    //     else:
    //         # need type 2
    //         if not heap2:
    //             return None
    //         ...
    // 
    // This should work. Let's test with the sample.
    // 
    // Sample 1:
    // N=5, M=4
    // ops: (2,4), (3,5), (1,4), (2,5)
    // sorted by L: (1,4,2), (2,4,0), (2,5,3), (3,5,1)
    // 
    // cur=0, target=5
    // heap1: add ops with L<=1: (1,4,2) -> heap1=[(-4,1,2)]
    // heap2: add ops with L>1: (2,4,0), (2,5,3), (3,5,1) -> heap2=[(-5,2,3), (-4,2,0), (-5,3,1)]
    // heap1 not empty, pop: R=4, L=1, i=2, type 1, cur=4, used[2]=True
    // Now cur=4, target=5
    // Move from heap2 to heap1: check heap2[0]: (-5,2,3) L=2 >1, so no move.
    // Add new ops with L>5: none.
    // Add new ops with L<=5: none (idx=4)
    // heap1 empty, need type 2.
    // heap2 not empty, pop: max R is 5, L=2, i=3, type 2, used[3]=True, cur=1, target=5? Wait, R=5, so target=5? But we set target=R=5. cur=L-1=1.
    // Now cur=1, target=5.
    // Move from heap2 to heap1: heap2 has (-4,2,0) and (-5,3,1). L=2>1, so no move.
    // Add new ops with L>2: none.
    // Add new ops with L<=2: none.
    // heap1 empty, need type 2.
    // heap2: pop max R: (-5,3,1) L=3, type 2, used[1]=True, cur=2, target=5? R=5, target=5.
    // Now cur=2, target=5.
    // Move from heap2 to heap1: heap2 has (-4,2,0) L=2<=3, so move to heap1: heap1=[(-4,2,0)]
    // Add new ops: none.
    // heap1 not empty, pop: R=4, L=2, i=0, type 1, cur=4, used[0]=True.
    // Now cur=4, target=5.
    // Move from heap2 to heap1: heap2 empty.
    // Add new ops: none.
    // heap1 empty, need type 2.
    // heap2 empty, return None? But we already have cur=4 < target=5.
    // We are missing the fact that after using type 2, we have covered [R+1, N] = [6,5] empty. So we don't need to cover beyond R=5. But we set target=5, and cur=4. We need to cover 5.
    // We have no more ops. So we fail.
    // 
    // This is not right. We should have covered 5 with the type 2 operation (R=5 covers up to 5, but we set target=5, so we need to cover up to 5. The type 2 operation covers [R+1, N] = [6,5] which is empty, so it doesn't help. It covers [1, L-1] = [1,1]. So we have cur=1, target=5. We need to cover [2,5]. We used another type 2 with L=3, R=5, which covers [1,2] and [6,5]. So cur=2, target=5. We need to cover [3,5]. We used a type 1 with L=2, R=4, which covers [2,4], so cur=4. We need to cover 5. We have no ops left. So we fail.
    // 
    // But the sample output is 2 2 0 1 0, which uses op 1 (2,4) as type 2, and op 3 (1,4) as type 1. That's exactly what we did, but we used extra ops. We used op 4 (2,5) as type 2 unnecessarily.
    // 
    // So our algorithm is not optimal because it uses type 2 operations even when type 1 would suffice. We need to prefer type 1 when possible.
    // 
    // In the sample, after using op 3 (1,4) as type 1, cur=4. We need to cover 5. We have op 4 (2,5) which has L=2 <=5, so it can be used as type 1 to cover 5. But we used it as type 2 because we thought heap1 was empty. But we should have added it to heap1 because L=2 <= cur+1=5.
    // 
    // In our algorithm, we added ops with L<=cur+1 to heap1. At the first step, cur=0, we added ops with L<=1. Then we moved to heap1 from heap2 when L<=cur+1. At the third step, cur=2, we moved op (2,4,0) from heap2 to heap1. But we also have op (2,5,3) in heap2. We need to move it to heap1 as well because L=2 <= cur+1=3. But we only moved when L<=cur+1. In the loop, we move from heap2 to heap1 while heap2 and heap2[0][1] <= cur+1. At that time, heap2 had (-4,2,0) and (-5,3,1). The top is (-4,2,0) with L=2. We popped it and pushed to heap1. But the next one is (-5,3,1) with L=3. We check if L <= cur+1=3, yes, so we should pop it too. But our while loop condition checks the top, so it should work.
    // 
    // Wait, in the code, we have:
    // while heap2 and heap2[0][1] <= cur+1:
    //     R_neg, L, i = heapq.heappop(heap2)
    //     if not used[i]:
    //         heapq.heappush(heap1, (R_neg, L, i))
    // 
    // At cur=2, heap2 has [(-4,2,0), (-5,3,1)]. The top is (-4,2,0) with L=2. We pop it and push to heap1. Then the new top is (-5,3,1) with L=3. We check L <= cur+1=3, yes, so we pop it and push to heap1. So both are moved. Good.
    // 
    // Then heap1 has both. We pop the one with max R: that's (-5,2,3) with R=5. But that op has L=2, R=5, which is exactly what we need to cover 5. So we should use it as type 1, not type 2.
    // 
    // In our algorithm, we popped from heap1 and used as type 1. So we should have used it.
    // 
    // So the algorithm should work. Let's test it step by step with the sample.
    // 
    // Sample 1:
    // N=5, M=4
    // ops: (2,4), (3,5), (1,4), (2,5)
    // sorted by L: (1,4,2), (2,4,0), (2,5,3), (3,5,1)
    // 
    // cur=0, target=5
    // heap1: add L<=1: (1,4,2) -> heap1=[(-4,1,2)]
    // heap2: add L>1: (2,4,0), (2,5,3), (3,5,1) -> heap2=[(-5,2,3), (-4,2,0), (-5,3,1)]
    // heap1 not empty, pop: (-4,1,2) -> R=4, L=1, type 1, cur=4, used[2]=True
    // 
    // cur=4, target=5
    // move from heap2 to heap1: heap2[0]=(-5,2,3) L=2>5? No, 2<=5, so move: pop (-5,2,3) push to heap1. Now heap2[0]=(-4,2,0) L=2<=5, move. Now heap2[0]=(-5,3,1) L=3<=5, move. heap2 empty.
    // add new ops with L>5: none.
    // add new ops with L<=5: none.
    // heap1: [(-5,2,3), (-4,2,0), (-5,3,1)] (heap order by -R)
    // heap1 not empty, pop max R: (-5,2,3) or (-5,3,1)? Both have R=5. The one with larger L? Actually, max R is 5. We can pop either. Let's say we pop (-5,2,3): R=5, L=2, type 1, cur=5, used[3]=True.
    // Now cur=5, target=5, done.
    // 
    // Chosen: (2,1), (3,1) -> indices 2 and 3 (0-based). That's op 3 and op 4. The sample output uses op 1 (index 0) as type 2 and op 3 (index 2) as type 1. So we have a different solution with cost 2. That's fine.
    // 
    // So the algorithm works.
    // 
    // Now, we need to output the chosen operations with their types in the original order.
    // 
    // We have chosen a list of (original_index, type). We need to assign 0 to the others.
    // 
    // Let's implement this.
    // 
    // Edge cases: If we cannot cover, return -1.
    // 
    // Complexity: O(M log M) for sorting, and O(M log M) for the greedy with heaps.
    // 
    // Let's code it.</mm:think>