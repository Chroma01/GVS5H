
## ideation
The core difficulty is efficiently counting valid subsequences for each candidate middle element. The key insight is that for a middle element `nums[i]` to be the unique mode, it must appear at least twice in the subsequence. Cases where it appears 3, 4, or 5 times are always valid. Cases where it appears exactly twice require that the other three elements are distinct. 

We can iterate over each element as the middle element, maintaining frequency maps for the left and right parts. For each middle element, we calculate:
1. Valid counts for cases where the middle element appears 3, 4, or 5 times (always valid).
2. Valid counts for cases where the middle element appears exactly twice, which requires the other three elements to be distinct. This is computed by iterating over distinct values in the left/right non-middle parts and using combinatorics to count valid pairs.

The overall complexity is O(n^2) due to iterating over each element and then over distinct values in the frequency maps (which is at most O(n) per element).

## worker: Implement a helper function for combinations (n ch
The solution iterates over each element as the potential middle element of the subsequence. For each candidate, it maintains frequency maps for the left and right parts. It then considers two main cases:
1. The middle element appears 3 or more times in the subsequence (which is always valid for unique mode).
2. The middle element appears exactly twice, which requires the other three elements to be distinct. This is handled by calculating total ways and subtracting invalid ways where the three non-middle elements are not distinct.

The combinatorics are precomputed using factorials and modular inverses for efficiency. The overall complexity is O(n^2) due to the nested loops over distinct values in the frequency maps for each candidate.
