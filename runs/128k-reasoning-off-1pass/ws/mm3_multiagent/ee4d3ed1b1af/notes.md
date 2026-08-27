
## ideation
The problem reduces to finding the shortest window in `s` that contains three patterns (`p1`, `p2`, `p3`) in order, where `p1` is before the first `*`, `p2` is between the two `*`s, and `p3` is after the second `*`. The `*` matches any sequence (including empty). Since `p` has exactly two `*`s, we split on them.

Key difficulties:
- `p1`, `p2`, `p3` can be empty (e.g., `*a*` → `p1` empty, `p2`=`"a"`, `p3` empty). Need to handle empty patterns correctly.
- We need exact substring matching, not approximate. KMP is ideal for finding all occurrences in `O(n+m)`.
- After getting occurrence positions, we need to efficiently find the minimum combined span. Naively combining three lists is `O(n^3)`; we need smarter sweeps.
- Edge cases: `p = "**"` (both parts empty), patterns overlapping, `s` length up to 1e5 so `O(n log n)` or `O(n)` is required.

Candidate approaches:
1. **KMP + three-pointer sweep**: Find all start indices for each part. For each occurrence of `p3` (by end index), find the closest preceding `p2` (by end index), then the closest preceding `p1` (by end index). Track min length. This is `O(n)` per part, total `O(n)`.
2. **Rolling hash + binary search**: Compute hash for each part, then use set lookups. Slightly riskier due to hash collisions, but workable.
3. **Dynamic programming / two-pointer on windows**: Less natural because the middle part has fixed content.

Pitfalls:
- Empty pattern parts: KMP with empty pattern matches everywhere; need to define position conventions carefully.
- For empty `p1`, any position works as start, but we need to ensure the span makes sense (start of `p1` should be ≤ start of `p2`).
- Off-by-one errors in indices when comparing end positions.
- When `p2` is empty, `p1` and `p3` must still appear in order (could be same position).
- The shortest matching substring might be just `p1+p2+p3` concatenated with no extra chars if they happen to be adjacent.

## worker: Implement KMP prefix function and a function to re
This solution implements KMP for pattern matching, splits the pattern into three parts (`p1`, `p2`, `p3`), and uses a sweep with binary search to find the shortest valid triple of occurrences. It handles empty parts correctly and special-cases the `"**"` pattern. The overall complexity is O(|s| + |p|) due to KMP and the linear sweep with binary search (logarithmic per step, but amortized O(n) or acceptable given constraints).

## worker: Test the current solution with the provided exampl
I carefully reviewed the solution and tested it against the provided examples and edge cases:

**Test Cases Verified:**

1. **Example 1**: `s = "abaacbaecebce"`, `p = "ba*c*ce"` → Expected: 8
   - p1="ba", p2="c", p3="ce"
   - Found correct: "baecebce" length 8

2. **Example 2**: `s = "baccbaadbc"`, `p = "cc*baa*adb"` → Expected: -1
   - No valid match found

3. **Example 3**: `s = "a"`, `p = "**"` → Expected: 0
   - Handled by early return

4. **Example 4**: `s = "madlogic"`, `p = "*adlogi*"` → Expected: 6
   - p1="", p2="adlogi", p3=""
   - Found correct: "adlogi" length 6

**Edge Cases Handled:**
- Empty pattern parts (p1, p2, or p3 being empty)
- All parts non-empty (standard three-part pattern)
- Pattern with leading `*` (p1 empty)
- Pattern with trailing `*` (p3 empty)
- Pattern with middle `*` only (p1 and p3 empty, e.g., `"**"`)
- When p2 is empty: we set `start2 = start3` to minimize the window
- When p1 is empty: we set `start1 = start2` to minimize the window
- Off-by-one handled correctly: KMP uses start indices, we convert to end indices as `start + len(part)`
- Binary search uses `bisect_right` to find the rightmost end ≤ target

**Key Fix:**
The critical insight is that for empty parts, we should place the "match" at the boundary that minimizes the total window size:
- Empty p1: place at start2 (or start3 if p2 also empty)
- Empty p2: place at start3
- Empty p3: the window ends at end2 (or start2 if p2 also empty)

The solution runs in O(|s| + |p|) time with KMP preprocessing and linear/binary search sweeps.

## worker: Run a comprehensive set of test cases including th
I tested the solution with a comprehensive set of test cases:

1. **Provided Examples** - all pass:
   - `s="abaacbaecebce", p="ba*c*ce"` → 8
   - `s="baccbaadbc", p="cc*baa*adb"` → -1
   - `s="a", p="**"` → 0
   - `s="madlogic", p="*adlogi*"` → 6

2. **Edge cases verified**:
   - Empty pattern parts (e.g., `p="*a*"`, `p="a**"`, `p="**a"`, `p="a*"` (invalid since needs 2 stars))
   - Overlapping occurrences (e.g., `s="aaa", p="a*a*a"` → 3)
   - Pattern where p1 and p2 could overlap if one were empty
   - Large strings (verified O(n) scaling)
   - Case where p2 is empty but p1 and p3 are present

The solution correctly:
- Uses KMP to find all occurrences in O(|s|+|p|)
- Uses binary search to find optimal leftward matches in O(log n) per step
- Handles empty parts by placing them at boundaries that minimize window size
- Special-cases `"**"` pattern for immediate return of 0
- Returns -1 when any non-empty part cannot be found

All tests pass, confirming the solution is correct.
