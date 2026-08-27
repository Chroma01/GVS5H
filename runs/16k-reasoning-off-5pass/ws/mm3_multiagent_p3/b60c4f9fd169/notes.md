
## ideation
The problem is a constrained edit distance problem: strings of length up to 500,000, but allowed operations K ≤ 20. Computing standard O(N·M) Levenshtein is too slow.

Key observation: In any optimal alignment with edit distance ≤ K, the difference in indices between S and T at any matched pair is at most K. Thus we only need to examine "diagonals" with offset d where -K ≤ d ≤ K. Along each such diagonal, the number of mismatches gives the replacements; insertions and deletions are the parts of S and T that fall outside the overlap. Total distance = (|S| - L) + (|T| - L) + mismatches = |S| + |T| - 2L + mismatches, where L is the length of the diagonal.

There are at most 2K+1 ≤ 41 offsets, each scanned in O(L) time, giving O(K·(|S|+|T|)) which is fast enough. The minimum over all offsets is the answer; if it ≤ K, print "Yes".

Pitfalls:
- Offsets: iterate d from -K to K. For each d, i ranges from max(0, -d) to min(|S|-1, |T|-1-d). L = number of i in that range.
- Use 0-based indexing.
- Need to check if any computed distance ≤ K; we can break early.
- Strings may be long, but scanning is linear and memory is fine.
- K is at most 20, so at most 41 diagonals.

## worker: (none needed)
The solution exploits the constraint K ≤ 20 to limit the search space. In any optimal alignment with edit distance ≤ K, the index difference between matched characters is at most K. Thus we only need to check 2K+1 ≤ 41 diagonals. For each offset d, we count mismatches along the overlapping diagonal and compute the total edit distance as (n - L) + (m - L) + mismatches. The total runtime is O(K·(n+m)) which is efficient for n, m ≤ 500,000. Early termination is used when a valid distance is found. A quick length difference check prunes the impossible case.
