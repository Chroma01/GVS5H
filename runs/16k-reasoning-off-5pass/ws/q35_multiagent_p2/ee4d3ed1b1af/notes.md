
## ideation
The problem asks for the shortest substring in `s` that matches a pattern `p` with exactly two `*` wildcards. The pattern can be split into three parts: `prefix`, `middle`, and `suffix`. The matching substring must start with `prefix`, end with `suffix`, and contain `middle` as a contiguous substring somewhere in between.

Key steps:
1. Split `p` into `prefix`, `middle`, and `suffix` by splitting on `*`.
2. If `prefix` or `suffix` is empty, handle edge cases (e.g., if both are empty, the answer is 0 if `middle` is empty, otherwise we need to find `middle` in `s`).
3. Find all starting indices of `prefix` in `s` and all ending indices of `suffix` in `s`.
4. For efficiency, we can:
   - Precompute all starting positions of `middle` in `s`.
   - For each occurrence of `prefix` at index `i`, we need to find the smallest `j` (end of `suffix`) such that:
     - The substring from `i` to `j + len(suffix) - 1` is valid.
     - The middle part `s[i + len(prefix) : j + len(suffix) - len(middle) + 1]` contains `middle`.
   - Actually, a better approach: 
     - Let `L = i + len(prefix)` be the start of the middle section.
     - Let `R = j` be the end of the suffix (exclusive for the suffix start).
     - We need to find if `middle` occurs in `s[L : R]` (i.e., starting at some index `k` where `L <= k` and `k + len(middle) <= R`).
     - We can precompute a list of all starting positions of `middle` in `s`. Then for a given `L` and `R`, we check if there's an occurrence starting at `k` such that `L <= k` and `k + len(middle) <= R`.
     - To optimize, for each `L`, we can find the smallest `R` such that there exists an occurrence of `middle` starting at `k >= L` and ending at `k + len(middle) - 1 < R`. This means `R > k + len(middle) - 1`. So the minimal `R` for a given `k` is `k + len(middle)`. But `R` must also be the start of a suffix occurrence.
     - So: 
       1. Find all start indices of `prefix`: `prefix_starts`.
       2. Find all start indices of `suffix`: `suffix_starts`.
       3. Find all start indices of `middle`: `middle_starts`.
       4. For each `i` in `prefix_starts`:
          - Let `L = i + len(prefix)`.
          - We need to find the smallest `j` in `suffix_starts` such that `j >= L` and there exists a `k` in `middle_starts` with `L <= k` and `k + len(middle) <= j`.
          - This is equivalent to: `j >= k + len(middle)` for some `k >= L`.
          - So for a fixed `i`, we want the smallest `j` in `suffix_starts` such that `j >= min_{k in middle_starts, k >= L} (k + len(middle))`.
          - Let `min_end = min({k + len(middle) for k in middle_starts if k >= L})`. If no such `k`, skip.
          - Then we need the smallest `j` in `suffix_starts` such that `j >= min_end`.
          - We can use binary search (bisect_left) on `suffix_starts` to find the smallest `j >= min_end`.
          - Then the candidate substring length is `j + len(suffix) - i`.
       5. Take the minimum over all valid `i`.

Pitfalls:
- Empty strings for prefix, middle, or suffix.
- Not handling the case where no match is found.
- Efficiency: Using naive search for prefix/suffix/middle might be slow, but with `s.length <= 10^5`, using `str.find` in a loop or precomputing all occurrences is acceptable if done efficiently. Precomputing all occurrences of `middle` can be done by scanning `s` once. Similarly for prefix and suffix.

Let's implement accordingly.

## worker: [todo] Parse the pattern `p` to extract `prefix`, 
The solution splits the pattern `p` into three parts: `prefix`, `middle`, and `suffix`. It then finds all starting indices of these parts in `s`. For each occurrence of `prefix` at index `i`, it determines the earliest occurrence of `middle` that starts at or after `i + len(prefix)`. Then it finds the earliest occurrence of `suffix` that starts at or after the end of that `middle` occurrence. The length of the substring from `i` to the end of the `suffix` is computed and the minimum over all valid combinations is returned. Edge cases where `prefix`, `middle`, or `suffix` are empty are handled naturally by the `find_all_occurrences` helper and the binary search logic. The time complexity is O(n) for finding occurrences and O(m log n) for the binary searches, where m is the number of prefix occurrences, which is acceptable given the constraints.
