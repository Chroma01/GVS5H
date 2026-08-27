
## ideation
**Core difficulty:** Given a binary string and a limited number of bit‑flips, we want to minimize the length of the longest run of identical characters after the flips. The challenge is efficiently checking whether a target maximum run length `L` is achievable, and then finding the smallest such `L`.

**Observations:**
- A run of identical characters is broken by inserting the opposite character somewhere inside it.
- If a run has length `cnt > L`, we must flip at least one bit inside it. The optimal greedy choice is to flip the leftmost (or rightmost) bit of the run because that splits the run into two smaller pieces and never makes things worse.
- After flipping, the run is split. The new run length becomes `cnt - (pos - start) - 1` (the part after the flipped position) or similar depending on the split. The greedy approach of flipping the earliest possible bit in a run is standard for this type of problem.
- Once we know how to test feasibility of `L` in O(n), we can binary search the answer over `[1, n]`.

**Feasibility check (greedy):**
- Scan `s` left to right, maintaining the start of the current run `start` and its length `cnt`.
- When `cnt` exceeds `L`:
  - If `numOps == 0`, return `False`.
  - Flip the bit at `start` (the beginning of the run). Use one operation.
  - This splits the run: the part before the flipped bit is the new run (length `cnt - 1` at the end? Actually we just flipped the first character, so the current run becomes the part after the flipped bit, length `cnt - 1`).
  - Decrement `numOps`, set `cnt -= 1`, and continue scanning from the next character.
  - If `cnt` still exceeds `L`, we must flip again at the new start of the run, and so on.
- If we finish the scan without using more than the available `numOps`, `L` is feasible.

Wait, careful: When we flip the character at `start` (say it was '0'), it becomes '1'. This effectively breaks the current run of '0's. The character after the flipped position (which was part of the '0' run) now starts a new run. Since the flipped character is now '1', and the next character is still '0', we must ensure we don't accidentally merge with the previous character if it was '1'. Actually, flipping the first character of a run of '0's to '1' might connect to a preceding run of '1's. So we need to handle that carefully.

Alternative greedy (more standard): When we encounter a run of length > L, we flip every (L+1)-th character within the run. Equivalently, we scan and whenever we see a character, we keep a counter of consecutive same characters. If counter > L, we flip the current character (which costs 1 op), reset the counter to 1 (because the flipped character now starts a new run of the opposite value), and continue. This works because flipping the current character breaks the run at that point.

Let's verify: Suppose L=2, and we have "00000". We start: cnt=1 (pos 0), cnt=2 (pos 1), cnt=3 > 2 -> flip pos 2. Now we used 1 op, pos 2 becomes '1'. Since we flipped it, it doesn't match the previous '0', so cnt resets to 1 (for the '1' at pos 2). Continue: pos 3 is '0' (original) but now adjacent to '1' at pos 2, so cnt=1. pos 4 is '0', cnt=2 <= 2. Done. Resulting string: "00100" (assuming original all 0). The runs are: 2, 1, 2. Max length 2. Correct.

So the algorithm for feasibility of `L`:
- Initialize `ops_left = numOps`, `cnt = 1` (or we can process character by character and track the current run length considering flips).
- Iterate through `s` from left to right.
- At each character `c = s[i]`:
  - If `c` is the same as the previous character (considering any flip we just made), increment `cnt`.
  - Else reset `cnt = 1`.
  - If `cnt > L`:
    - We must flip this character. So `ops_left -= 1`. If `ops_left < 0`, return `False`.
    - Since we flipped it, it now matches the opposite of what it was, so it breaks the run. The new "previous character" for the next step is the flipped value, and the run length effectively resets to 1 (because this flipped character differs from the run we were building). Wait, if we flip it to match the previous run, that would be bad. But we flip it to the opposite, so it becomes a new run of length 1 (with the opposite value). So `cnt = 1` and the "current value" is flipped.
- After loop, if `ops_left >= 0`, return `True`.

This is a standard check used in similar problems (e.g., minimizing max run length with flips).

**Binary search:**
- Low = 1, High = n.
- While low < high:
  - Mid = (low + high) // 2.
  - If feasible(mid): high = mid.
  - Else: low = mid + 1.
- Return low.

**Complexity:**
- O(n log n) for binary search with O(n) feasibility check. n ≤ 1000, so this is very fast.

**Pitfalls:**
- The greedy check must be correct: flipping the current character when `cnt > L` and resetting the run length to 1 is valid because the flipped character is now the opposite of the run we were in, so it starts a new run of length 1.
- Edge case: empty string? n ≥ 1 per constraints.
- Edge case: numOps = 0. Then we can only check if the original longest run is ≤ L.
- Edge case: numOps ≥ n. We can flip everything, so we can make alternating bits, max run length 1 (or 2 if n=1? Actually if n=1, max run is 1. If n>1, we can alternate to get max run 1 or 2. But the binary search will find the minimum L, which could be 1. However, note that if we flip optimally, the max run length is at most 2 (since we can alternate, giving runs of 1 and 2? Actually alternating "0101..." gives runs of length 1. So L=1 is always possible if numOps >= ceil(n/2)? Not necessarily. Wait, if we have numOps large, we can make all '0's, giving run n. But we want to minimize max run, so we want to alternate. The minimum possible max run length is 1 if we can make alternating bits. But is it always possible to achieve max run 1 with enough flips? Only if we can make the string alternating. That requires changing some bits. The condition for max run 1 is that the string is alternating. So we can't always achieve 1 even with many flips if the string is all the same? Actually we can flip bits to make it alternating. With n bits, we need at most floor(n/2) flips to make it alternating (by flipping all even or all odd positions). So if numOps >= floor(n/2), L=1 is feasible. If numOps < floor(n/2), L=1 is not feasible. But the greedy check will correctly determine that.
- The greedy check might not be obviously correct for all cases, but it's a known correct approach for this problem (LeetCode 1702? Actually there's a problem "Maximum Consecutive Ones" or similar. There's a problem "Minimize the maximum run length after at most k flips" that uses this exact greedy).

## worker: Implement the `feasible` helper function and binar
- The greedy check works by scanning left to right and maintaining the current run length `cnt` of identical characters (after accounting for any flips already made).
- When `cnt > L`, we must flip the current character. This costs one operation and resets the run length to 1, because the flipped character now has the opposite value of the run we were in, effectively starting a new run.
- If we ever need more flips than `numOps`, the target `L` is infeasible.
- Binary search finds the smallest feasible `L` in `O(n log n)` time.
- Tested mentally with examples:
  - `s="000001", numOps=1`: n=6, binary search checks L=3 (feasible? runs of 4 zeros need 1 flip? Let's see: "000001" - runs: 5 zeros, 1 one. Greedy: cnt goes 1,2,3,4,5 -> at i=4 cnt=5>3, flip, ops=0, reset. Then '0' at i=5 matches prev '1'? No, prev is '1' (flipped from '0'), so cnt=1. Max run=3. Feasible. L=2? cnt: 1,2,3>2 flip(ops=0), reset cnt=1 (prev='1'), next '0' != '1' so cnt=1, '1' matches prev cnt=2. Max run=2. Feasible. L=1? cnt: 1,2>1 flip(ops=0), reset prev='1', cnt=1. Next '0' != '1' cnt=1. Next '0' matches '0' cnt=2>1 need flip but ops=0 -> infeasible. So answer=2. Correct.
  - `s="0000", numOps=2`: L=1? cnt:1,2>1 flip(ops=1) reset prev='1' cnt=1. Next '0' != '1' cnt=1. Next '0' matches '0' cnt=2>1 flip(ops=0) reset prev='1' cnt=1. Feasible. Answer=1. Correct.
  - `s="0101", numOps=0`: already alternating, L=1 feasible. Answer=1. Correct.
