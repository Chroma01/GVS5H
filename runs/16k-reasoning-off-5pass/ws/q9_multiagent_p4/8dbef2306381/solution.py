import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        A = int(next(iterator))
        B = int(next(iterator))
        
        bad_intervals = []
        for _ in range(M):
            L = int(next(iterator))
            R = int(next(iterator))
            bad_intervals.append((L, R))
    except StopIteration:
        return

    # Sort bad intervals by L
    bad_intervals.sort()

    # reachable is a list of tuples (start, end) representing contiguous intervals of reachable squares.
    # Initially, only square 1 is reachable.
    # We maintain the invariant that all squares in these intervals are reachable,
    # and no square outside these intervals (up to the current processing point) is reachable.
    reachable = [(1, 1)]

    for L, R in bad_intervals:
        new_reachable = []
        
        # For each existing reachable interval [s, e], we can jump to any square x such that:
        # s + A <= x <= s + B
        # Since we cannot land on bad squares [L, R], we are only interested in x > R.
        # Also, we can only jump from s if s is reachable.
        # The set of reachable squares strictly greater than R is the union of:
        # [s + A, s + B] intersected with (R, infinity) for all s in reachable intervals.
        
        for s, e in reachable:
            # The range of squares reachable from the interval [s, e] is [s+A, e+B].
            # We intersect this with (R, infinity), i.e., [R+1, infinity).
            start_new = s + A
            end_new = e + B
            
            # Intersection: [max(start_new, R + 1), end_new]
            actual_start = max(start_new, R + 1)
            actual_end = end_new
            
            if actual_start <= actual_end:
                new_reachable.append((actual_start, actual_end))
        
        if not new_reachable:
            # If no squares are reachable after the bad interval, we can't proceed.
            print("No")
            return

        # Merge overlapping or adjacent intervals to maintain the list of disjoint intervals.
        new_reachable.sort()
        merged = []
        curr_start, curr_end = new_reachable[0]
        
        for s, e in new_reachable[1:]:
            # If intervals overlap or are adjacent (e.g., [1, 2] and [3, 4] -> [1, 4]), merge them.
            # Note: Since we are dealing with integers, [1, 2] and [3, 4] are contiguous.
            if s <= curr_end + 1:
                curr_end = max(curr_end, e)
            else:
                merged.append((curr_start, curr_end))
                curr_start, curr_end = s, e
        merged.append((curr_start, curr_end))
        
        # Optimization: If we have a contiguous block of reachable squares of length >= B,
        # we can reach any square up to the end of this block + B.
        # This effectively means we have "infinite" reachability until the next obstacle
        # (or indefinitely if no more obstacles).
        # Specifically, if we have [u, v] with v - u + 1 >= B, then for any x in [u+A, v+B],
        # there exists s in [u, v] such that x - s in [A, B].
        # The length of the new reachable block [u+A, v+B] is (v+B) - (u+A) + 1 = (v-u+1) + (B-A) >= B.
        # So the property is preserved.
        
        simplified = False
        if len(merged) == 1:
            u, v = merged[0]
            if v - u + 1 >= B:
                # We have a "full" block. Update it to the next potential reach.
                # The new reachable block will be [u+A, v+B].
                reachable = [(u + A, v + B)]
                simplified = True
        else:
            # If we have multiple intervals, check if any single one has length >= B.
            # If one does, it dominates the reachability because it can bridge any gap 
            # smaller than B (which would have merged the intervals anyway if they were close enough).
            # If there are multiple disjoint "full" blocks, they are separated by gaps >= B.
            # However, the one that extends furthest to the right is the most powerful for reaching N.
            # We can replace the list with just that one expanded interval.
            full_candidates = []
            for u, v in merged:
                if v - u + 1 >= B:
                    full_candidates.append((u + A, v + B))
            
            if full_candidates:
                # Take the one that extends furthest to the right.
                # Since they are disjoint in 'merged', their expansions might overlap or not.
                # But the one with the largest end is the best candidate to reach N.
                # Actually, if we have multiple full blocks, they are separated by gaps.
                # If a gap is large, the earlier block cannot reach the later block's start.
                # But the later block is reachable from the previous bad interval logic.
                # Wait, if we have multiple intervals in 'merged', it means there are gaps between them.
                # If one is full, it can reach across gaps of size < B.
                # If the gap is >= B, the full block cannot reach the next block.
                # So we should keep the one that reaches furthest?
                # Yes, because if we can reach N, we need the furthest reach.
                # Any square reachable by an earlier full block is also reachable by the later one?
                # Not necessarily. But if we have a full block, we can reach everything up to its end + B.
                # If we have multiple, we just need the one with the max end to check N.
                # However, to be safe and simple, let's just keep the one with the max end.
                best_u, best_v = max(full_candidates, key=lambda x: x[1])
                reachable = [(best_u, best_v)]
                simplified = True
            else:
                reachable = merged
                simplified = False

    # After processing all bad intervals, check if N is reachable
    for s, e in reachable:
        if s <= N <= e:
            print("Yes")
            return

    print("No")

if __name__ == '__main__':
    solve()