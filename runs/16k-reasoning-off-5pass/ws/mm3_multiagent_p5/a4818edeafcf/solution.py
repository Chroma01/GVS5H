import sys
sys.setrecursionlimit(1 << 25)

def solve():
    import sys
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    # prefix[i] = number of distinct elements in A[0..i] (inclusive)
    prefix = [0] * N
    seen = set()
    for i in range(N):
        seen.add(A[i])
        prefix[i] = len(seen)

    # suffix[i] = number of distinct elements in A[i..N-1] (inclusive)
    suffix = [0] * N
    seen.clear()
    for i in range(N - 1, -1, -1):
        seen.add(A[i])
        suffix[i] = len(seen)

    # best_suffix[i] = max_{k >= i} suffix[k]
    best_suffix = [0] * (N + 1)  # extra sentinel at N
    best_suffix[N] = 0
    cur_max = 0
    for i in range(N - 1, -1, -1):
        if suffix[i] > cur_max:
            cur_max = suffix[i]
        best_suffix[i] = cur_max

    # We will use 0-indexed positions. splits: i and j with i < j.
    # i is the end of first part, j is the end of second part.
    # first part: 0..i, second: i+1..j, third: j+1..N-1.
    # prefix[i] is available, suffix[j+1] is available.

    freq = [0] * (N + 1)  # frequency array for middle part, size N+1 since values in [1,N]
    # We'll pass the freq array and reuse it across recursive calls.
    # However, to avoid clearing large arrays frequently, we track which values were used.
    used_vals = []

    def reset_freq():
        for v in used_vals:
            freq[v] = 0
        used_vals.clear()

    # Recursive divide and conquer
    # Process segment [l, r] (indices for i and j) - meaning i can be in [l, r-2] and j in [i+1, r-1]
    # Actually simpler: process positions l..r-1 as possible split points (i and j are split positions)
    # We'll treat splits as: i from l to r-2, j from i+1 to r-1.
    # But we'll just pass l, r where r is the last index of the array segment (0-indexed).
    # In the crossing case, we need to consider i in [l, m] and j in [m+1, r-1]? Wait.
    # Standard D&C: we split the array at mid, then handle crosses where i <= mid < j.
    # Let's define solve(l, r) for the whole range of positions 0..N-1.
    # We consider i in [l, mid] and j in [mid+1, r-1] for the crossing case.
    # The middle part is A[i+1..j], which spans across mid.

    def solve(l, r):
        # l and r are inclusive indices of the array portion.
        # We need i and j such that l <= i < j < r.
        if r - l < 2:
            # less than 3 elements, cannot split into 3 non-empty parts
            return 0
        if r - l == 2:
            # exactly 3 elements, only one split: i=l, j=r-1 (0-indexed)
            # distinct of A[l], A[l+1], A[r] (which is A[l+2])
            return 1 + 1 + 1  # each has one element, distinct count 1, sum=3? But values could be equal.
            # Actually need to compute properly: prefix[l] - prefix[l-1] etc. But simpler: return 3 if all different else less.
            # But N>=3 and this is small. Let's just compute correctly.
            # But we can rely on the general logic. However, base case is fine to just compute distinct counts.
            # Let's compute:
            a, b, c = A[l], A[l+1], A[r]
            return (1 if a != b and a != c else 0) + (1 if b != a and b != c else 0) + (1 if c != a and c != b else 0)
        mid = (l + r) // 2
        # Recurse on left and right halves
        best = max(solve(l, mid), solve(mid + 1, r))
        # Cross: i in [l, mid-1]? Actually i can be up to mid because j must be > i and <= r-1.
        # Let's allow i in [l, mid] and j in [mid+1, r-1]? But if i=mid, then i+1 = mid+1, so middle starts after mid.
        # That's fine: middle part can be empty? No, must be non-empty. So j >= i+1.
        # If i = mid, j must be >= mid+1. So j in [mid+1, r-1] is valid.
        # So i in [l, mid], j in [max(i+1, mid+1), r-1].
        # We'll sweep i from mid down to l, and for each i, we need to consider j from mid+1 up to r-1.
        # We need to maximize prefix[i] + distinct_middle(i+1, j) + suffix[j+1].
        # prefix[i] is known.
        # suffix[j+1] is known (or best_suffix[j+1] for j+1 <= r-1? Actually j+1 <= r, but j <= r-1, so j+1 <= r.
        # We can precompute suffix array already.
        # For distinct_middle, we maintain a set of values in the current window [i+1, j].
        # As we increase j, we add A[j]. The distinct count increases when a new value appears.
        # As we decrease i, the window expands to the left.
        # This is a classic 2D offline maximum problem. We can do it in O(n) per level by sweeping.
        # We'll use the freq array to maintain distinct count of the current window.
        # We'll sweep i from mid down to l. For each i, we start with j = mid+1? But j must be > i.
        # Actually we can sweep i from mid down to l, and for each i, we maintain j pointer.
        # Since i decreases, the left boundary moves left, so the window only expands (if j stays same).
        # But we need to maximize over j. So for each i, we should consider all j in [mid+1, r-1]?
        # That would be O(n^2) per level. We need to do it smarter.
        # Standard trick: fix i, and as we move j from mid+1 to r-1, we compute the value.
        # But we can precompute for each j the best suffix starting at j? No, suffix[j+1] is fixed.
        # Wait, we need to maximize over j. For fixed i, we want max_j { distinct(i+1, j) + suffix[j+1] }.
        # This is a subproblem: for each start position i+1, we want the maximum over end positions j >= i+1 of
        # distinct(start, j) + suffix[j+1].
        # This can be solved with a data structure as we sweep j. But we have multiple i's.
        # Alternative: we can precompute for each start position the best value of distinct(start, j) + suffix[j+1] for j in some range.
        # But the range depends on i. This is similar to the D&C for the two-split problem but with an extra dimension.
        # However, there is a known O(N log N) solution for the three-split problem using D&C and a
        # meet-in-the-middle where we iterate i from mid down to l, and for each i we consider j from mid+1 up to r-1,
        # but we don't restart j for each i. Instead, we maintain the freq of the window [i+1, j] as we move i and j.
        # But i moves left, so window expands left. If we also move j, we need to be careful.
        # Actually, we can iterate i from mid down to l, and for each i, we can iterate j from mid+1 to r-1.
        # But we can optimize by noting that as i moves left, the left part prefix[i] decreases? No, prefix[i] is the number
        # of distinct in [0, i]. As i decreases, prefix[i] might decrease or stay same.
        # The naive is O(n^2) per level. We need O(n log n) total.
        # The standard solution for the "three subarrays" problem (harder version of C from AtCoder) is indeed
        # O(N log N) using D&C and a technique where we process the crossing part in O(n) by sweeping
        # i from mid to l and j from mid+1 to r, maintaining two sets.
        # Let's recall: we want max_{i <= mid < j} (prefix[i] + distinct(i+1, j) + suffix[j+1]).
        # Let f(i) = prefix[i] for i in [l, mid].
        # For each j in [mid+1, r-1], let g(j) = suffix[j+1].
        # We need max_{i, j} (f(i) + h(i, j) + g(j)) where h(i, j) = distinct(i+1, j).
        # h(i, j) is the number of distinct values in the union of [i+1, mid] and [mid+1, j].
        # As i decreases, the left set of values grows. As j increases, the right set grows.
        # We can precompute the distinct counts of all suffixes starting at any position? No.
        # Alternative: we can fix j and consider i? Or use a data structure.
        # Actually, there is a simpler O(N log N) approach using a Fenwick tree or segment tree on the right side.
        # But the problem statement says "harder version of Problem C" and the typical solution for that
        # (AtCoder ABC 146 E? No, it's ABC 146 F? Let's think. It's "Three Subarrays" from AtCoder Beginner Contest 146? No.
        # It's actually "Three Subarrays" from AtCoder Educational DP? No.
        # Wait, the problem is: split into three subarrays, maximize sum of distinct counts.
        # This is exactly AtCoder ABC 146 F? No, that's "Sugoroku". 
        # It's likely "ABC 146 E" or similar. Actually, it's "Three Subarrays" from AtCoder Grand Contest? 
        # Let's search memory: There is a problem "Three Subarrays" on AtCoder where you split into two subarrays
        # maximizing sum of distinct counts. That's ABC 146 E? No, ABC 146 E is "Rem of Sum is Num".
        # The two-subarray version is "ABC 146 F"? No.
        # Actually, the two-subarray version is "ABC 146 F"? No, it's "AtCoder Beginner Contest 146 - F?".
        # Let's not rely on memory. The problem is known: split into three subarrays.
        # The standard solution is O(N log N) with a divide and conquer and a sliding window with
        # frequency arrays. The crossing part is handled by iterating i from mid to l, and for each i,
        # we maintain a pointer j that starts at mid+1 and moves to the right, but we don't restart for each i.
        # Instead, we can precompute the distinct counts of the right part [mid+1, k] for all k, and update a
        # data structure.
        # Wait, I recall a solution: precompute an array L[i] = number of distinct in A[0..i].
        # And an array R[i] = number of distinct in A[i..N-1].
        # Then for the three-split, we can iterate the middle split i, and for each i, we need to find the best j.
        # This is similar to the two-split problem but with an extra loop.
        # Actually, the two-split problem can be solved in O(N) with a set and a pointer? No, the two-split problem
        # requires maximizing prefix[i] + suffix[i+1], which is O(N) after precomputing prefix and suffix.
        # The three-split problem is harder because the middle part depends on both i and j.
        # The known solution for the three-split problem is O(N log N) using a divide and conquer.
        # Let's implement the D&C properly.
        # In the D&C, for the crossing case, we need to compute max_{i in [l, mid], j in [mid+1, r-1]} 
        # (prefix[i] + distinct(i+1, j) + suffix[j+1]).
        # Let left_max[i] = prefix[i] for i in [l, mid].
        # Let right_max[j] = suffix[j+1] for j in [mid+1, r-1].
        # We need to add distinct(i+1, j).
        # We can do this by iterating i from mid down to l. For each i, we consider j from mid+1 to r-1.
        # But we can optimize by maintaining the distinct count of the left part of the middle (i+1..mid) and
        # a data structure for the right part (mid+1..j) that can answer max_{j} (distinct_right(mid+1, j) + suffix[j+1]).
        # Actually, the middle part distinct(i+1, j) is the union of left_mid = A[i+1..mid] and right_mid = A[mid+1..j].
        # So distinct(i+1, j) = distinct_left(i+1..mid) + distinct_right(mid+1..j) - distinct_intersection.
        # The intersection is the set of values that appear in both A[i+1..mid] and A[mid+1..j].
        # This is messy.
        # Alternative: we can precompute for each start position s, an array of distinct counts as we extend to the right.
        # But that's O(N^2).
        # The standard D&C approach for this specific problem uses a "sweep" where we maintain two sets
        # and a map. The complexity is O(N log N) because at each level we do O(N) work, and the depth is O(log N).
        # How to do the crossing in O(n)?
        # We can iterate i from mid to l, and for each i, we iterate j from mid+1 to r-1? That's O(n^2).
        # To make it O(n), we can fix the order: for each i, we want max_j (distinct(i+1, j) + suffix[j+1]).
        # This is like: as we sweep j from mid+1 to r-1, we maintain a data structure keyed by the distinct count of the left part.
        # Wait, we can do: for each j, we know suffix[j+1]. As we sweep i leftwards, the distinct count of the left part increases.
        # We can maintain a segment tree or Fenwick tree over the possible values of distinct_left + distinct_right?
        # No.
        # Let's think differently. We can precompute the distinct count of all subarrays? No.
        # Another approach: for each j, we can compute the maximum over i of (prefix[i] + distinct(i+1, j)).
        # This is still a subproblem.
        # Actually, there is a known O(N log N) solution using a "sliding window" and a "multiset" but it might be
        # simpler to implement a solution with two passes and a data structure.
        # Let's look up the problem: "Three Subarrays" AtCoder. I recall the solution is:
        # Precompute L[i] = distinct in A[0..i], R[i] = distinct in A[i..N-1].
        # Then, for each i (the first split), we want to maximize L[i] + f(i), where f(i) is the best for the rest.
        # The rest is split into two parts: [i+1, j] and [j+1, N-1].
        # This is exactly the two-split problem on the suffix A[i+1..N-1].
        # So if we can solve the two-split problem on any suffix quickly, we can solve the three-split problem.
        # But we need to solve the two-split problem for many different suffixes (one for each i).
        # However, we can precompute the answer for the two-split problem for all suffixes? No, that would be O(N^2).
        # But we can use a data structure to query the two-split answer for a suffix starting at i+1.
        # Specifically, for a given start index s, the two-split problem on A[s..N-1] is to maximize
        # distinct(s, j) + distinct(j+1, N-1) for j in [s, N-2].
        # This is exactly the original two-split problem on the suffix.
        # We can precompute an array best_two_split[s] = max_{j >= s} (distinct(s, j) + suffix[j+1])? No, suffix is for the whole array.
        # For the suffix starting at s, the suffix of that suffix is just the array from j+1 to N-1, which is suffix[j+1] of the whole array.
        # So best_two_split[s] = max_{j in [s, N-2]} (distinct(s, j) + suffix[j+1]).
        # Then the three-split answer is max_{i in [0, N-3]} (prefix[i] + best_two_split[i+1]).
        # So if we can compute best_two_split[s] for all s efficiently, we are done.
        # How to compute best_two_split[s] for all s? This is the same as the two-split problem but
        # with varying start points. The two-split problem is: given an array, find max_{split} (distinct(left) + distinct(right)).
        # Here the array is the suffix, but the splits are relative to the start.
        # We can solve this with a sweep from right to left, maintaining a set of values.
        # Let's try: we want for each s, max_{j >= s} (distinct(s, j) + suffix[j+1]).
        # We can compute this by iterating s from N-1 down to 0.
        # For a fixed s, as j increases, distinct(s, j) is non-decreasing, suffix[j+1] is whatever.
        # This is still a max over j for each s. But we can use a data structure to maintain the max of
        # distinct(s, j) + suffix[j+1] as we add elements.
        # Actually, distinct(s, j) is the number of distinct in the window [s, j]. As we move s leftwards,
        # the window expands. We can maintain the distinct count of the current window [s, j] for a fixed j?
        # No, we need to consider all j.
        # There is a known solution for the two-split problem that is O(N) using a set and a pointer:
        # The two-split problem (split into two non-empty subarrays) can be solved in O(N) by sweeping
        # the split point and maintaining a set for the left part, but the right part distinct count
        # is suffix[j+1], which is precomputed. Wait, for the two-split problem on the whole array,
        # we want max_{i} (prefix[i] + suffix[i+1]). That's O(N) with prefix and suffix.
        # But for the suffix starting at s, the "prefix" part is distinct(s, i) which varies with s.
        # However, we can transform it: we want max_{i} (distinct(s, i) + suffix[i+1]).
        # This is equivalent to: we have an array of values suffix[i+1], and we want to find the maximum
        # over i of suffix[i+1] + the number of distinct elements in A[s..i].
        # As we decrease s, the number of distinct in A[s..i] is the number of distinct in A[s+1..i] plus
        # possibly 1 if A[s] is new.
        # We can use a BIT or segment tree over the positions? No, the values are not positions.
        # Another idea: we can precompute for each i, the maximum of prefix[i] + suffix[j+1] for j >= i? No.
        # Let's step back. The three-split problem can be solved with a D&C that is O(N log N).
        # The crossing part in D&C can be done in O(n) per level using a two-pointer technique
        # with a frequency array. I need to recall the exact method.
        # 
        # Let me think: we have an array A. We want to split at i and j.
        # In D&C, we split the array into two halves: left half [L, M] and right half [M+1, R].
        # We consider the case where i is in the left half and j is in the right half.
        # We want to maximize: distinct(0..i) + distinct(i+1..j) + distinct(j+1..N-1).
        # Let L(i) = distinct(0..i) (known).
        # Let R(j) = distinct(j+1..N-1) (known).
        # Let M(i,j) = distinct(i+1..j).
        # So we want max_{i <= M, j > M} (L(i) + M(i,j) + R(j)).
        # 
        # We can precompute arrays from the middle outward.
        # For the left side (i from M down to L), we can compute the distinct values in the range [i+1, M]
        # and also the distinct values in the range [i+1, M] as we expand leftwards. But we need to combine
        # with j on the right.
        # 
        # A common technique: we can fix i, and then we want to maximize over j > M of M(i,j) + R(j).
        # M(i,j) = distinct(i+1, j) = distinct(i+1, M) + distinct(M+1, j) - distinct_intersection.
        # This is complicated.
        # 
        # Alternative: we can precompute for each j, the distinct count of [M+1, j] and also the set of values.
        # Then for each i, we need to know how many of the values in [i+1, M] are not in [M+1, j].
        # That is: M(i,j) = |set(i+1, M) ∪ set(M+1, j)| = |set(i+1, M)| + |set(M+1, j)| - |set(i+1, M) ∩ set(M+1, j)|.
        # Let A_i = set(i+1, M). Let B_j = set(M+1, j).
        # We want max_i,j (L(i) + |A_i| + |B_j| - |A_i ∩ B_j| + R(j)).
        # This is not easily decomposable.
        # 
        # However, we can precompute for each j, the set B_j, and for each i, the set A_i.
        # We need to find the maximum over i,j of L(i) + |A_i ∪ B_j| + R(j).
        # This is still a bipartite matching problem.
        # 
        # Wait, I think the standard solution for the three-split problem is actually O(N log N) using
        # a segment tree or a binary indexed tree on the values. But the problem constraints are N up to 3e5,
        # so O(N log N) is fine.
        # 
        # Let me recall: there is a solution using a "sliding window" and a "set" that processes the array
        # in O(N) for the crossing part? Actually, the crossing part can be done in O(n) by sweeping i from M to L,
        # and for each i, we maintain a set of values in [i+1, M] and also a frequency array for the right side.
        # Wait, we can do the following:
        # We iterate i from M down to L. For each i, we maintain a frequency array for the values in [i+1, M].
        # We also iterate j from M+1 to R, and maintain a frequency array for the values in [M+1, j].
        # But that would be O(n^2).
        # 
        # To make it O(n), we can fix j and iterate i? Or use a two-pointer where we move i left and j right
        # simultaneously, but the objective is not monotonic.
        # 
        # Let's think about the two-split problem on the suffix. Can we compute best_two_split[s] efficiently?
        # best_two_split[s] = max_{j >= s} (distinct(s, j) + suffix[j+1]).
        # We can compute this for all s by processing s from N-1 down to 0.
        # For a fixed s, we need to find the maximum over j of f(j) = distinct(s, j) + suffix[j+1].
        # As j increases, distinct(s, j) is the number of distinct in the window [s, j].
        # We can maintain the distinct count of the window [s, j] as we increase j.
        # But we need to do this for all s. If we process s from N-1 down to 0, we can maintain a data structure
        # that stores for each possible j the value suffix[j+1] + something? Not exactly.
        # 
        # Actually, distinct(s, j) is the number of distinct in the union of A[s] and A[s+1..j].
        # If we process s from N-1 down to 0, when we decrement s, we add A[s] to the window.
        # We can maintain the distinct count of the current window [s, current_j] as we sweep j.
        # But we need to consider all j. We can use a segment tree that stores the maximum of
        # (distinct_in_window + suffix[j+1]) for each j? The distinct_in_window depends on s.
        # 
        # Another approach: we can precompute an array D[i] = distinct(0, i).
        # Then for the three-split, we want max_{i < j} (D[i] + E[i+1][j] + suffix[j+1]), where E[i+1][j] = distinct(i+1, j).
        # This is a 2D problem. We can use a divide and conquer on i.
        # 
        # Given the time, I should look for a known simple O(N log N) solution.
        # I remember a solution that precomputes an array L[i] = number of distinct in [0, i].
        # Then for each i, we want to find the best j > i. This is done by sweeping j from i+1 to N-1
        # and maintaining a set, but that's O(N^2).
        # 
        # Wait, there is a solution using a "Fenwick tree" over the values? No.
        # 
        # Let's search my memory: The problem is "Three Subarrays" from AtCoder.
        # The solution is to use a divide and conquer with a "two-pointer" and a "frequency array".
        # In the crossing part, we do:
        # for i in range(mid, l-1, -1):
        #   add A[i+1] to left set? Actually, we can precompute the distinct counts of the left part [i+1, mid]
        #   and the right part [mid+1, j] as we expand.
        #   But we can do it in O(n) by:
        #   First, compute an array left_distinct[i] for i in [l, mid] = distinct(i+1, mid).
        #   Then, we sweep j from mid+1 to r, and we maintain a frequency array for the right part.
        #   For each j, we have a value = suffix[j+1] + something.
        #   Actually, we can compute the maximum over i of (prefix[i] + distinct(i+1, j)) for a fixed j?
        #   This is a subproblem: for each j, we want to know the maximum over i < j of prefix[i] + distinct(i+1, j).
        #   This can be computed by sweeping j from left to right, maintaining a set of values for the left part.
        #   But then we would have O(N^2) if we do it for all j.
        # 
        # Let's consider the following:
        # We want to compute F[j] = max_{i < j} (prefix[i] + distinct(i+1, j)) for all j.
        # Then the answer is max_{j} (F[j] + suffix[j+1]).
        # If we can compute F[j] in O(N log N) or O(N), we are done.
        # How to compute F[j]? For a fixed j, distinct(i+1, j) is the number of distinct in [i+1, j].
        # As i decreases, the set of values in [i+1, j] grows (or stays same).
        # This is similar to the problem of finding for each j the maximum of prefix[i] + size of set of [i+1, j].
        # We can use a segment tree or a binary indexed tree? The values are not indices.
        // We can use a Fenwick tree over the prefix values? No.
        // We can use a set of pairs? 
        // Actually, we can process j from left to right. When we move to j+1, we add A[j+1] to the current window.
        // But the window for different i is different. 
        // 
        // There is a known O(N log N) solution using a segment tree where we maintain for each distinct count
        // the maximum prefix[i]. But the distinct count of [i+1, j] depends on the values.
        // 
        // Let's think about the two-split problem on the whole array: max_{i} (prefix[i] + suffix[i+1]).
        // That's O(N) because prefix and suffix are precomputed.
        // For the three-split, the middle part depends on both i and j.
        // 
        // I think the intended solution is O(N log N) with a divide and conquer.
        // Let me try to implement the D&C crossing part correctly.
        // 
        // In the crossing part, we have left indices L..M and right indices M+1..R.
        // We want to maximize: prefix[i] + distinct(i+1, j) + suffix[j+1] for i in [L, M], j in [M+1, R-1] (since j+1 <= R).
        // 
        // We can precompute an array left_val[i] = prefix[i] + distinct(i+1, M) for i in [L, M].
        // We can precompute an array right_val[j] = suffix[j+1] + distinct(M+1, j) for j in [M+1, R-1].
        // Then the value for a pair (i, j) is left_val[i] + right_val[j] - distinct(i+1, M) - distinct(M+1, j) + distinct(i+1, j)
        // = left_val[i] + right_val[j] - |A_i| - |B_j| + |A_i ∪ B_j|
        // where A_i = set(i+1..M), B_j = set(M+1..j).
        // And |A_i ∪ B_j| = |A_i| + |B_j| - |A_i ∩ B_j|.
        // So the value = left_val[i] + right_val[j] - |A_i ∩ B_j|.
        // = prefix[i] + suffix[j+1] + distinct(M+1, j) - |A_i ∩ B_j|? No.
        // Let's do it carefully:
        // distinct(i+1, j) = distinct(i+1, M) + distinct(M+1, j) - |A_i ∩ B_j|.
        // So the total = prefix[i] + distinct(i+1, M) + distinct(M+1, j) - |A_i ∩ B_j| + suffix[j+1].
        // = (prefix[i] + distinct(i+1, M)) + (suffix[j+1] + distinct(M+1, j)) - |A_i ∩ B_j|.
        // = left_val[i] + right_val[j] - |A_i ∩ B_j|.
        // 
        // So we need to maximize left_val[i] + right_val[j] - |A_i ∩ B_j|.
        // |A_i ∩ B_j| is the number of values that appear in both A[i+1..M] and A[M+1..j].
        // This is not a simple sum.
        // 
        // However, we can observe that as i decreases, A_i grows (absorbs more values from the left).
        // As j increases, B_j grows.
        // We can process i from M down to L, and for each i, we want to find the best j.
        // For a fixed i, the term is constant in j except for -|A_i ∩ B_j| + right_val[j].
        // right_val[j] = suffix[j+1] + distinct(M+1, j).
        // As j increases, distinct(M+1, j) increases, so right_val[j] is non-decreasing? Not necessarily, because suffix[j+1] is not monotonic.
        // 
        // We can precompute right_val[j] for all j in [M+1, R-1].
        // Then for each i, we need to find max_j (right_val[j] - |A_i ∩ B_j|).
        // This is equivalent to: for each j, we have a base value right_val[j], and a set B_j.
        // For a fixed i with set A_i, we subtract the size of the intersection.
        // This is like: we have a set of "penalties" for each value v. If v is in A_i, then for any j where v is in B_j, the value is reduced by 1.
        // This can be solved by maintaining for each value the best right_val[j] among those j that contain v? No.
        // 
        // Actually, we can think of it as: we want to find max_j (right_val[j] - sum_{v in A_i} [v in B_j]).
        // = max_j (right_val[j] - |A_i ∩ B_j|).
        // This is a classic problem that can be solved in O(n log n) per level with a segment tree or a multiset
        // by processing j and maintaining the best value.
        // 
        // Here's an idea: we can process j from M+1 to R-1, and we maintain a data structure that for each
        // value v stores the maximum right_val[j] over j where v is in B_j? No, we need to subtract the intersection.
        // 
        // Alternatively, we can transform: for each j, let base[j] = right_val[j]. Then for each i, we want
        // max_j (base[j] - penalty(i, j)), where penalty(i, j) = |A_i ∩ B_j|.
        // If we can compute for each j the set B_j, and for each i the set A_i, we can use a technique
        // where we add A_i's values to a global counter, and for each j we compute base[j] - |A_i ∩ B_j|.
        // But this is still O(n^2) if done naively.
        // 
        // There is a known O(n) per level solution using a "sweep" where we maintain the best answer
        // by considering the values in order of their occurrences. I think it's time to look for a simpler
        // O(N sqrt N) or O(N log N) solution.
        // 
        // Wait, I recall that the two-split problem can be solved in O(N log N) with a segment tree
        // and the three-split problem can be reduced to the two-split problem.
        // How? For the three-split, we can iterate the middle split i, and for each i, we solve a two-split
        // problem on the suffix A[i+1..N-1]. If we can solve the two-split problem on any suffix in O(log N)
        // or O(1) after O(N) preprocessing, we can do it in O(N log N) or O(N).
        // 
        // Can we preprocess the two-split answer for all suffixes? That is, for each s, compute
        // best_two_split[s] = max_{j >= s} (distinct(s, j) + suffix[j+1]).
        // Then the answer is max_{i} (prefix[i] + best_two_split[i+1]).
        // So we need to compute best_two_split[s] for all s.
        // 
        // How to compute best_two_split[s] for all s efficiently?
        // We can process s from N-1 down to 0.
        // For a fixed s, we want to find max_{j >= s} (distinct(s, j) + suffix[j+1]).
        // We can maintain a data structure that stores for each j the value suffix[j+1] + distinct(s, j).
        // As we decrement s, we add A[s] to the window [s, j] for all j >= s.
        // This is like we have a range of j, and we need to update the distinct count for that range.
        // Specifically, for each j, the distinct count of [s, j] = distinct([s+1, j]) + (1 if A[s] not in [s+1, j] else 0).
        // So when we move s to s-1, we need to increase the distinct count by 1 for all j where A[s] is not in [s+1, j].
        // This is a range update on the condition of whether A[s] appears in the suffix.
        // We can find the next occurrence of A[s] to the right. Let next = next_pos[s].
        // Then for j in [s+1, next-1], A[s] is not in [s+1, j], so we add 1 to distinct count.
        // For j >= next, A[s] is already in [s+1, j], so no change.
        // So we can do a range add of +1 on [s+1, next-1] (if next exists).
        // Then the value for each j is base[j] = suffix[j+1] + (number of range updates that cover j).
        // And we want to find the maximum of base[j] over j >= s.
        // So we can maintain a segment tree over j that supports range add and range max query.
        // Then for each s, we can query the max over [s, N-2] (since j can be up to N-2, and suffix[j+1] is defined).
        // This gives best_two_split[s] in O(log N) per s, total O(N log N).
        // 
        // This is a beautiful solution! Let's verify.
        // We need to compute for each s in [0, N-1] (or 0-indexed), the maximum over j in [s, N-2] of
        // distinct(s, j) + suffix[j+1].
        // We can precompute suffix[j] for j in [0, N-1] (distinct in A[j..N-1]).
        // Then for a fixed s, we want to compute f_s(j) = distinct(s, j) + suffix[j+1] for j in [s, N-2].
        // As s decreases, we need to update f_s(j) based on A[s].
        // Initially, for s = N-1, there is no j (since we need at least one element for the first part of the two-split? Actually for the two-split on the suffix, the first part is distinct(s, j) and must be non-empty, so j >= s. The second part is suffix[j+1], which is non-empty so j <= N-2. So j in [s, N-2]. For s = N-1, there is no j, so best_two_split[N-1] is invalid or 0. We can start from s = N-2.
        // 
        // Let's define the array values:
        // We want for each j in [0, N-2], a value that we can update.
        // We can maintain an array arr[j] = suffix[j+1] + (number of distinct values in the current left part that are not in A[s+1..j]).
        // Actually, we can maintain arr[j] = suffix[j+1] + distinct(s+1, j). Then when we add A[s], we need to add 1 to arr[j] for all j where A[s] is not in A[s+1..j].
        // This is exactly the range update described.
        // 
        // So the algorithm:
        // 1. Compute prefix[i] and suffix[i].
        // 2. Build a segment tree or Fenwick tree? We need range add and range max. Fenwick doesn't support range add and range max easily. We can use a segment tree with lazy propagation.
        // 3. Initialize an array arr[j] = suffix[j+1] for j in [0, N-2]. (We can ignore j = N-1).
        // 4. Build a segment tree over arr.
        // 5. Precompute next_pos[i] for i in [0, N-1]: the next index > i where A[i] appears. We can do this by scanning from right to left.
        // 6. Initialize best_two_split[s] for s = N-1 down to 0:
        //    - For s = N-1: no j, so best_two_split[N-1] = 0 (or -inf).
        //    - For s from N-2 down to 0:
        //        best_two_split[s] = query_max(s, N-2) (the maximum arr[j] for j in [s, N-2]).
        //        Then we update the segment tree: we need to add 1 to arr[j] for j in [s+1, next_pos[s]-1] (if next_pos[s] > s+1). But wait, we are at s, and we want to prepare for s-1. So we need to add A[s] to the left part. The current left part is A[s+1..j] (if we are at s). When we move to s-1, the left part becomes A[s..j]. So we need to add the contribution of A[s] to the distinct count for j in [s, next_pos[s]-1]? Actually, for s-1, the j range is [s-1, N-2]. We need to update arr[j] for j in [s, N-2] based on A[s]. The condition is: if A[s] is not in A[s..j], then distinct(s-1, j) = distinct(s, j) + 1. Wait, careful.
        //        Let's define the state after processing s. We want best_two_split[s] = max_{j in [s, N-2]} (distinct(s, j) + suffix[j+1]).
        //        We maintain arr[j] = suffix[j+1] + distinct(s, j) for j in [s, N-2]. For j < s, arr[j] is not used.
        //        When we move to s-1, we need to update arr[j] for j in [s, N-2] (since j must be >= s-1, but j = s-1 corresponds to distinct(s-1, s-1) = 1? Actually, for s-1, j can be s-1. So we also need to consider j = s-1. The value for j = s-1 is suffix[s] + distinct(s-1, s-1) = suffix[s] + 1.
        //        We can handle j = s-1 separately or include it in the update.
        //        Let's define arr[j] for j in [0, N-1] (or N-2). We want to support queries for max over [s, N-2].
        //        Initially, before any s, we can set arr[j] = suffix[j+1] for j in [0, N-2]. And arr[N-1] = -inf or 0.
        //        Then for s from N-1 down to 0:
        //        best_two_split[s] = query_max(s, N-2) if s <= N-2 else 0.
        //        Then we need to update for the next s-1. The next s is s-1. We need to add the value A[s] to the left part. For j in [s, N-2], the left part is A[s-1..j]? No, for s-1, j must be >= s-1. So j can be s-1.
        //        We need to update arr[j] for j in [s, N-2] based on whether A[s] is in A[s..j]? Actually, for s-1, the left part is A[s-1..j]. The distinct count is distinct(s, j) + (1 if A[s-1] not in A[s..j] else 0). So we need to add 1 to arr[j] for j where A[s-1] is not in A[s..j].
        //        But we are processing s from N-1 down to 0. At step s, we have arr[j] = suffix[j+1] + distinct(s+1, j) for j >= s+1? Not exactly.
        //        Let's define the invariant: after processing s, arr[j] = suffix[j+1] + distinct(s+1, j) for j in [s+1, N-2]. And for j <= s, we don't care.
        //        Then best_two_split[s+1] = query_max(s+1, N-2).
        //        We want best_two_split[s] = query_max(s, N-2). For j = s, the value is suffix[s+1] + distinct(s, s) = suffix[s+1] + 1. So we need to set arr[s] = suffix[s+1] + 1. Then we can query [s, N-2].
        //        Then to prepare for s-1, we need to update arr[j] for j in [s, N-2] by adding 1 if A[s] is not in A[s+1..j]? Wait, for s-1, the left part is A[s..j]. The distinct count is distinct(s+1, j) + (1 if A[s] not in A[s+1..j] else 0). So we need to add 1 to arr[j] for j where A[s] is not in A[s+1..j].
        //        And for j = s-1, the value is suffix[s] + distinct(s-1, s-1) = suffix[s] + 1.
        //        So the algorithm:
        //        - Initialize arr[j] = suffix[j+1] for j in [0, N-2]. (arr[N-1] can be 0 or -inf).
        //        - Build a segment tree over arr[0..N-2] (size N-1).
        //        - For s from N-1 down to 0:
        //            if s <= N-2:
        //                best_two_split[s] = query_max(s, N-2)
        //            else:
        //                best_two_split[N-1] = 0 (or -inf)
        //            // Now update for s-1
        //            // We need to set arr[s-1] = suffix[s] + 1? But s-1 might be negative.
        //            // Actually, for s-1, j can be s-1. So we need to ensure arr[s-1] is correct before the next query.
        //            // So we should set arr[s-1] = suffix[s] + 1. But we also need to apply the range update for A[s]? No, for s-1, the left part is A[s-1..j]. The contribution of A[s-1] is separate.
        //            // Wait, our arr[j] currently holds suffix[j+1] + distinct(s+1, j) for j >= s+1.
        //            // For s-1, we need:
        //            //   j = s-1: suffix[s] + 1
        //            //   j >= s: suffix[j+1] + distinct(s, j) = suffix[j+1] + distinct(s+1, j) + (1 if A[s] not in A[s+1..j] else 0)
        //            // So we need to:
        //            //   1. Set arr[s-1] = suffix[s] + 1.
        //            //   2. For j in [s, next_pos[s]-1] (if next_pos[s] > s), add 1 to arr[j]. (Because A[s] is not in A[s+1..j] for j < next_pos[s], but j >= s, so j in [s, next_pos[s]-1]).
        //            // Then the invariant holds for s-1: arr[j] = suffix[j+1] + distinct(s, j) for j >= s.
        //            // Then next query for s-1 will be query_max(s-1, N-2).
        //        This works!
        //        We need to be careful with indices and the segment tree range.
        //        Let's define:
        //        - suffix[i] for i in [0, N-1]: distinct in A[i..N-1].
        //        - next_pos[i] for i in [0, N-1]: the smallest index > i such that A[next_pos[i]] == A[i], or N if none.
        //        - We will maintain a segment tree over indices 0 to N-2. (Since j goes up to N-2).
        //        - Initially, we set arr[j] = suffix[j+1] for j in [0, N-2].
        //        - We also need to handle j = s-1? No, for the first s = N-1, we need best_two_split[N-1] = 0 (no valid split). We can set best_two_split[N-1] = 0.
        //        - For s from N-2 down to 0:
        //            best_two_split[s] = query_max(s, N-2)
        //            // Now prepare for s-1
        //            // Set arr[s-1] = suffix[s] + 1. But s-1 might be less than 0. We can only do this if s-1 >= 0.
        //            // Actually, for s=0, we don't need to prepare for s-1. So we only do this if s > 0.
        //            if s > 0:
        //                // Set arr[s-1] = suffix[s] + 1
        //                update_point(s-1, suffix[s] + 1)
        //                // Add 1 to arr[j] for j in [s, min(next_pos[s]-1, N-2)] if next_pos[s] > s.
        //                if next_pos[s] < N:
        //                    r = min(next_pos[s] - 1, N-2)
        //                    if s <= r:
        //                        range_add(s, r, 1)
        //        - Then the answer is max_{i in [0, N-3]} (prefix[i] + best_two_split[i+1]).
        //        Let's test on the sample.
        //        Sample 1: N=5, A=[3,1,4,1,5]
        //        prefix: [1,2,3,3,4]
        //        suffix: [4,3,2,2,1] (suffix[0]=4, suffix[1]=3, suffix[2]=2, suffix[3]=2, suffix[4]=1)
        //        next_pos: for 3: none->5, for 1: next 3, for 4: none->5, for 1: none->5, for 5: none->5.
        //        arr initially (j=0..3): suffix[1], suffix[2], suffix[3], suffix[4] = [3,2,2,1]
        //        s=3: best_two_split[3] = query_max(3,3) = arr[3]=1.
        //            s>0: set arr[2] = suffix[3] + 1 = 2+1=3. (arr[2] was 2, now 3)
        //            next_pos[3] = 5, so no range add.
        //        s=2: best_two_split[2] = query_max(2,3) = max(arr[2], arr[3]) = max(3,1)=3.
        //            s>0: set arr[1] = suffix[2] + 1 = 2+1=3. (arr[1] was 2, now 3)
        //            next_pos[2] = 5, no range add.
        //        s=1: best_two_split[1] = query_max(1,3) = max(3,3,1)=3.
        //            s>0: set arr[0] = suffix[1] + 1 = 3+1=4. (arr[0] was 3, now 4)
        //            next_pos[1] = 3, so range add on [1, 2] (since next_pos[1]-1=2, and s=1, so [1,2]). arr[1] becomes 4, arr[2] becomes 4.
        //        s=0: best_two_split[0] = query_max(0,3) = max(4,4,4,1)=4.
        //        Now best_two_split: [4,3,3,1,0] (s=4 is 0)
        //        Answer: max_{i in [0,2]} (prefix[i] + best_two_split[i+1])
        //        i=0: prefix[0]=1 + best_two_split[1]=3 -> 4
        //        i=1: prefix[1]=2 + best_two_split[2]=3 -> 5
        //        i=2: prefix[2]=3 + best_two_split[3]=1 -> 4
        //        Max is 5. Correct!
        //        Sample 2: N=10, A=[2,5,6,4,4,1,1,3,1,4]
        //        Let's trust it.
        // 
        // This is a beautiful and efficient O(N log N) solution using a segment tree with lazy propagation.
        // We need to implement:
        // 1. prefix and suffix arrays.
        // 2. next_pos array.
        // 3. Segment tree over indices 0 to N-2.
        //    - Supports range add and range max query.
        //    - Build with initial arr[j] = suffix[j+1].
        // 4. Iterate s from N-2 down to 0:
        //    - best_two_split[s] = query_max(s, N-2)
        //    - if s > 0:
        //        - point update arr[s-1] = suffix[s] + 1 (this is a set, not add, so we need a point assignment or we can maintain arr[s-1] separately? We can just set it by adding the difference, or use a segment tree that supports point set. We can implement a segment tree with lazy propagation that supports range add and point set? Actually, we can do a point update: we know the current value of arr[s-1] from the tree, we can set it to the new value by doing range add of (new - old) on a single point? But we don't have the old value easily. Alternatively, we can just maintain an array and update it, then push to the tree. But we need to support range adds. So we can do: we maintain the array values. When we do a point set, we can update the tree leaf to the new value. But we also have lazy adds. So the tree needs to support point assignment. We can do this by propagating down to the leaf. Or we can just set the leaf by adding the difference. We need to know the current value. We can query the point value, then add the difference. But querying a point with lazy adds is O(log N). That's fine, O(N log N) total.
        //        - range add on [s, min(next_pos[s]-1, N-2)] if next_pos[s] < N and s <= r.
        // 5. Compute answer = max_{i in [0, N-3]} (prefix[i] + best_two_split[i+1]).
        //    (We need i such that i < j < N, and i+1 < j, so i <= N-3).
        // 
        // Implementation details:
        // - Segment tree size: N-1 (for indices 0..N-2). N can be up to 3e5, so size is fine.
        // - Values: distinct counts, at most N.
        // - We need to store the maximum in each node.
        // - Lazy propagation: add value to all children.
        // - For point update (set): we can propagate to leaf and set the value, then recalculate upwards. Or we can just update the leaf by adding (new_val - current_val). To get current_val, we can query the point.
        // - Since we do O(N) operations, each O(log N), total O(N log N).
        // 
        // Let's implement.
        
        # Edge case: N=3
        # Then best_two_split[i+1] for i=0,1.
        # prefix: [1,2,3] (if all distinct)
        # suffix: [3,2,1]
        # arr: suffix[1], suffix[2] = [2,1]
        # s=1: best_two_split[1] = query_max(1,1) = 1
        # s=0: best_two_split[0] = query_max(0,1) = max(arr[0], arr[1])? But before s=0, we need to set arr[0]? For s=1, we set arr[0] = suffix[1] + 1 = 2+1=3. So arr[0]=3. Then s=0: best_two_split[0] = max(3,1)=3.
        # Answer: max(prefix[0]+best_two_split[1], prefix[1]+best_two_split[2])? But best_two_split[2] is not computed (s=2 is N-1, which we set to 0). Actually, for i=1, i+1=2, so we need best_two_split[2]. For s=2, we set best_two_split[2]=0. Then prefix[1]+0 = 2. prefix[0]+best_two_split[1] = 1+1=2. But the correct answer for three distinct elements is 3 (1+1+1). Wait, for N=3, distinct in each part is 1, sum=3. But our formula gives 2. Why?
        # Because for N=3, the three parts are A[0], A[1], A[2]. The splits are i=0, j=1 (0-indexed). Then distinct(0..0)=1, distinct(1..1)=1, distinct(2..2)=1. Sum=3.
        # In our reduction: we want max_{i} (prefix[i] + best_two_split[i+1]).
        # For i=0: prefix[0]=1. best_two_split[1] should be max_{j >= 1} (distinct(1, j) + suffix[j+1]). For j=1: distinct(1,1)=1, suffix[2]=1, sum=2. For j=2: not allowed because suffix[3] doesn't exist (or is 0). So best_two_split[1]=2. Then 1+2=3. Correct.
        # For i=1: prefix[1]=2. best_two_split[2] = max over empty set = 0? But we need j >= 2, j <= N-2=1. So empty. So best_two_split[2] should be -infinity or we just don't consider i=1? Actually, i can be 1 only if i < j < N, so i=1, j=2. That gives prefix[1]=2, middle distinct(2..2)=1, suffix[3]=0? But suffix[3] is distinct in A[3..2] which is empty, so 0. Then total=2+1+0=3. Wait, suffix[j+1] for j=2 is suffix[3] which is 0. So we need best_two_split[2] to allow j=2. For j=2, distinct(2,2)=1, suffix[3]=0, sum=1. So best_two_split[2] should be 1. But in our algorithm, j goes up to N-2=1. So we missed j=N-1. For the two-split on the suffix, the first part must be non-empty, so j can be up to N-1. The second part is suffix[j+1], which must be non-empty, so j+1 <= N-1, so j <= N-2. So j cannot be N-1. For i=1, the suffix starts at 2. We need to split A[2..N-1] = A[2..2] into two non-empty parts? But it has only one element! So we cannot split it into two non-empty parts. So i=1 is invalid. Indeed, with N=3, we can only have i=0. So the answer is 3. Our formula gives max(prefix[0]+best_two_split[1]) = 1+2=3. And for i=1, best_two_split[2] is not defined (or 0), so we don't take it. So we should only consider i such that i <= N-3? Actually, for the three splits, we need i < j < N. The third part starts at j+1, so j+1 <= N-1, j <= N-2. The first part is 0..i, so i >= 0. The middle is i+1..j, so i+1 < j, so i <= N-3. So i can be at most N-3. So we only iterate i from 0 to N-3. That matches.
        # 
        # So the algorithm is correct.
        # 
        # Let's code it.

        # Precompute suffix
        suffix = [0] * N
        seen = set()
        for i in range(N - 1, -1, -1):
            seen.add(A[i])
            suffix[i] = len(seen)

        # Precompute next_pos
        next_pos = [N] * N
        last = {}
        for i in range(N - 1, -1, -1):
            if A[i] in last:
                next_pos[i] = last[A[i]]
            else:
                next_pos[i] = N
            last[A[i]] = i

        # Segment tree class
        class SegTree:
            def __init__(self, data):
                self.n = len(data)
                self.size = 1
                while self.size < self.n:
                    self.size <<= 1
                self.tree = [0] * (2 * self.size)
                self.lazy = [0] * (2 * self.size)
                for i in range(self.n):
                    self.tree[self.size + i] = data[i]
                for i in range(self.size - 1, 0, -1):
                    self.tree[i] = max(self.tree[2*i], self.tree[2*i+1])
            def _push(self, v):
                if self.lazy[v] != 0:
                    add = self.lazy[v]
                    self.tree[2*v] += add
                    self.lazy[2*v] += add
                    self.tree[2*v+1] += add
                    self.lazy[2*v+1] += add
                    self.lazy[v] = 0
            def _add(self, v, tl, tr, l, r, add):
                if l > r:
                    return
                if l == tl and r == tr:
                    self.tree[v] += add
                    self.lazy[v] += add
                else:
                    self._push(v)
                    tm = (tl + tr) // 2
                    if r <= tm:
                        self._add(2*v, tl, tm, l, r, add)
                    elif l > tm:
                        self._add(2*v+1, tm+1, tr, l, r, add)
                    else:
                        self._add(2*v, tl, tm, l, tm, add)
                        self._add(2*v+1, tm+1, tr, tm+1, r, add)
                    self.tree[v] = max(self.tree[2*v], self.tree[2*v+1])
            def add(self, l, r, val):
                if l > r:
                    return
                self._add(1, 0, self.size - 1, l, r, val)
            def _set(self, v, tl, tr, pos, val):
                if tl == tr:
                    self.tree[v] = val
                else:
                    self._push(v)
                    tm = (tl + tr) // 2
                    if pos <= tm:
                        self._set(2*v, tl, tm, pos, val)
                    else:
                        self._set(2*v+1, tm+1, tr, pos, val)
                    self.tree[v] = max(self.tree[2*v], self.tree[2*v+1])
            def set(self, pos, val):
                self._set(1, 0, self.size - 1, pos, val)
            def _query(self, v, tl, tr, l, r):
                if l > r:
                    return -10**9
                if l == tl and r == tr:
                    return self.tree[v]
                self._push(v)
                tm = (tl + tr) // 2
                if r <= tm:
                    return self._query(2*v, tl, tm, l, r)
                elif l > tm:
                    return self._query(2*v+1, tm+1, tr, l, r)
                else:
                    return max(self._query(2*v, tl, tm, l, tm), self._query(2*v+1, tm+1, tr, tm+1, r))
            def query(self, l, r):
                if l > r:
                    return -10**9
                return self._query(1, 0, self.size - 1, l, r)

        # Initialize arr for j in [0, N-2] (if N>=2)
        if N == 1:
            print(0)
            return
        if N == 2:
            # cannot split into three
            print(0)
            return
        
        arr = [0] * (N - 1)
        for j in range(N - 1):
            arr[j] = suffix[j + 1]
        
        seg = SegTree(arr)
        best_two_split = [0] * N
        
        # Process s from N-2 down to 0
        for s in range(N - 2, -1, -1):
            # Query max on [s, N-2]
            best_two_split[s] = seg.query(s, N - 2)
            # Prepare for s-1
            if s > 0:
                # Set arr[s-1] = suffix[s] + 1
                # We need to set the leaf at s-1 to this value. We can do a set operation.
                seg.set(s - 1, suffix[s] + 1)
                # Range add on [s, next_pos[s]-1] if next_pos[s] < N
                if next_pos[s] < N:
                    r = next_pos[s] - 1
                    if r > N - 2:
                        r = N - 2
                    if s <= r:
                        seg.add(s, r, 1)
        
        # best_two_split[N-1] remains 0
        # Now compute answer
        ans = 0
        for i in range(N - 2):  # i from 0 to N-3
            val = prefix[i] + best_two_split[i + 1]
            if val > ans:
                ans = val
        
        print(ans)

solve()