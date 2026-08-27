
## ideation
The problem asks for the k-th lexicographically smallest alternating permutation of {1..n} where adjacent elements have opposite parity. n ≤ 100, k ≤ 10^15.

**Core difficulty**: Efficiently counting how many alternating permutations start with a given prefix, without enumerating all permutations (which could be huge). We need a combinatorial counting method to skip blocks of permutations.

**Key observations**:
1. An alternating permutation must start with either an odd or an even number. This determines the parity pattern for all subsequent positions.
2. For a fixed parity pattern (e.g., odd-even-odd-...), the remaining numbers are split into two pools: odds and evens. The number of ways to fill the remaining positions is simply `o! * e!` where `o` and `e` are the counts of remaining odds and evens, provided the pattern requires exactly `o` odds and `e` evens. If the required counts don't match the available counts, the count is 0.
3. Lexicographic order means we try the smallest unused number first at each position. For each candidate, we compute the number of valid completions. If `k > count`, we subtract and try the next candidate. Otherwise, we fix the candidate and move to the next position.

**Candidate approaches**:
- **Brute force**: Generate all alternating permutations, sort them, pick the k-th. Too slow for n=100.
- **Greedy with combinatorial counting**: At each position, iterate over unused numbers in sorted order, compute the number of completions for each, and skip blocks. This is the standard approach for k-th permutation problems.
- **Precompute factorials**: Since n ≤ 100, factorials fit in standard integers, but k can be up to 10^15, so we cap counts at some value > 10^15 (e.g., 10^18) to avoid overflow and unnecessary computation.

## worker: Implement the factorial precomputation with cappin
The solution implements the standard "k-th lexicographic permutation with constraints" pattern:
1. Precomputes factorials up to n=100, capping at INF=10^18 to handle large k (up to 10^15) without overflow.
2. The `count_ways(o, e, start_parity)` helper computes the number of valid completions given remaining counts and the parity of the next position to fill. It checks that the required number of odd/even positions matches the available counts, then returns `o! * e!` (capped).
3. First determines whether the k-th permutation starts with an odd or even number by comparing k to the count of odd-starting permutations.
4. Then greedily constructs the permutation: at each position, iterates over unused numbers in sorted order that match the required parity, computes the count of completions for each, and skips entire blocks when k exceeds the count.

## worker: Test the solution with the provided examples and e
The solution correctly implements the k-th lexicographic alternating permutation using a greedy approach with combinatorial counting. Key points:

1. **Factorial precomputation** with capping at INF=10^18 to handle k up to 10^15 without overflow.

2. **`count_ways(o, e, start_parity)`** computes the number of valid completions given remaining odd/even counts and the parity required at the next position. It checks that the required number of each parity matches the available counts, then returns `o! * e!`.

3. **Block-skipping logic**: For each candidate at the current position, compute the number of completions. If k > count, subtract and skip. Otherwise, fix the choice and continue.

4. **Tested with**:
   - All three provided examples (correct)
   - Edge case n=1 (k=1 returns [1], k=2 returns [])
   - k=1 for n=10 (returns smallest permutation)
   - k equal to total count (returns last permutation)
   - Brute-force verification for n=4 and n=5 against all valid permutations

All tests pass, including brute-force verification against generated lists for small n.
