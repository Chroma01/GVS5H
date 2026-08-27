
## ideation
- Core difficulty: we cannot enumerate permutations (`n <= 100`), and valid counts can exceed `1e15`, so we need capped DP counting plus lexicographic k-th construction.
- Key insight: after a prefix, the number of valid completions depends only on `(odds_left, evens_left, last_parity)`, not on which specific values remain. Actual values matter only when scanning candidates in ascending order during construction.
- Lexicographic blocks: when the next candidate value `x` is fixed, all permutations with that prefix form one block whose size is the DP completion count after choosing `x`. Skip/subtract whole blocks until `k` falls inside one.
- Counts have closed forms (`n` even: `2*(n/2)!^2`; `n` odd: `((n+1)/2)!*((n-1)/2)!`), but DP is safer and directly supports construction.
- Pitfalls: `k` is 1-based; return `[]` if `k > total`; cap DP values at `k` to avoid huge integers; handle first position with “no previous parity”; skip used numbers and wrong-parity candidates; be careful when one parity pool is exhausted.

## worker: Implement the complete solution: capped memoized D
- **Counting DP**: `count(odds, evens, last)` returns the number of valid completions given the remaining parity pools and the parity of the previous element (`0` = none/start, `1` = odd, `2` = even). Transitions only go to the opposite parity pool. The count depends only on pool sizes, not on which specific values remain — this is the key insight that makes the state space O(n²·3).
- **Capping**: all counts are clamped at the original `k`. This keeps integers small (k up to 1e15, but true counts can be astronomically larger, e.g. 2·(50!)²). Capping at the original k is safe throughout construction because the running k never exceeds the original k, so `min(actual, CAP) >= k_running` iff `actual >= k_running`.
- **Feasibility check**: compute the total from the initial state; if it's (capped) less than k, the true total is less than k, so return `[]`.
- **Construction**: greedily scan candidates 1..n in ascending order, skipping used values and same-parity candidates. Each candidate defines a lexicographic block of size `count(...)`; subtract blocks while `k > block`, otherwise fix the candidate and continue. Dead-end candidates have block size 0 and are harmlessly skipped.
- **Verified against examples**: n=4,k=6 → [3,4,1,2]; n=3,k=2 → [3,2,1]; n=2,k=3 → [].
- **Complexity**: O(n²) DP states with O(1) transitions; construction does O(n²) lookups. Recursion depth ≤ n = 100, well within limits.
