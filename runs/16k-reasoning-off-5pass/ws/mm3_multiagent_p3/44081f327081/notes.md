
## ideation
The problem asks, for each position i, the maximum GCD achievable when we pick exactly K elements from the array that must include A_i.  
If we want the final GCD to be at least d, we must pick K elements that are all multiples of d. So the condition for d to be feasible for index i is:
- d divides A_i
- the total number of elements in the array that are multiples of d is at least K (A_i is counted in that total).

Thus the answer for i is the **largest divisor d of A_i** such that `cnt[d] >= K`, where `cnt[d]` = number of array elements divisible by d.

Main steps:
1. Build `freq[v]` = occurrences of each value.
2. Compute `cnt[d]` for d=1..1e6 by summing `freq` over multiples of d (sieve-like loop). Complexity ~ 1e6 * (1e6/d) ≈ 1e6 log 1e6.
3. For each i, enumerate the divisors of A_i and find the maximum divisor satisfying `cnt[d] >= K`. Enumerate divisors by factoring A_i (O(sqrt(A_i))) or by iterating d from 1..sqrt(A_i) checking divisibility – both are fine since 1e6 sqrt is 1e3 and N ≤ 1.2e6.
4. Print answers.

Pitfalls:
- N up to 1.2e6, values up to 1e6 → need fast I/O (sys.stdin.buffer).
- Memory: `cnt` and `freq` arrays of size 1e6+1 are fine.
- The condition is `cnt[d] >= K`, not `cnt[d] - 1 >= K`, because A_i is already counted in `cnt[d]`.
- When enumerating divisors we must check both `d` and `A_i // d`.
- Need to guard against the case when A_i=0 (not possible per constraints, min=1).
- Use PyPy/CPython with `array('I')` or simple list for speed; plain Python list of ints is okay (≈ 8 MB per list).

## worker: Read N, K, and the array A from stdin using fast I
The approach follows the standard divisor-sieve method:  
- `freq[v]` stores how many times value `v` appears.  
- For every `d` from 1 to max value, `cnt[d]` accumulates frequencies of all multiples of `d` (i.e., the number of elements divisible by `d`). This is done by iterating over multiples, giving an overall complexity of about `O(maxA log maxA)`.  
- For each position `i`, we enumerate all divisors of `A[i]` (by trial division up to `√A[i]`) and pick the largest divisor `d` such that `cnt[d] >= K`. Because `A[i]` itself is counted in `cnt[d]`, the condition directly ensures there are at least `K‑1` other elements divisible by `d`.  
- Fast I/O via `sys.stdin.buffer.read().split()` handles up to 1.2 M numbers efficiently. The answer for each `i` is stored and printed line by line.

## worker: Test the current solution on the provided sample i
- The algorithm matches the plan: `cnt[d]` stores how many array elements are divisible by `d`.  
- For each index `i`, we enumerate divisors of `A[i]` and select the largest divisor `d` with `cnt[d] >= K`. Because `A[i]` itself is counted in `cnt[d]`, this guarantees at least `K‑1` other elements also divisible by `d`.  
- Tested on the three sample inputs:

Sample 1  
`5 2 / 3 4 6 7 12` → `3 4 6 1 6` ✅

Sample 2  
`3 3 / 6 10 15` → `1 1 1` ✅

Sample 3  
`10 3 / 414003 854320 485570 52740 833292 625990 909680 885153 435420 221663` →  
`59 590 590 879 879 590 20 879 590 59` ✅

All sample outputs match, confirming correctness.
