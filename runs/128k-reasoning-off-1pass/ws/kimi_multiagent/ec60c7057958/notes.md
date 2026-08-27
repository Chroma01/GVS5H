
## ideation
The core difficulty is that n can be up to 100, so we cannot enumerate permutations. We need to construct the k-th lexicographic alternating permutation directly using combinatorial counting, similar to the standard "k-th permutation" problem but with a parity constraint.

Key observations:
- An alternating permutation requires adjacent elements to differ in parity. Once the first element's parity is chosen, the parity pattern of the entire permutation is fixed (e.g., odd, even, odd, even, ... or even, odd, even, odd, ...).
- The number of odd numbers in [1..n] is ceil(n/2), and even numbers is floor(n/2). For a valid alternating permutation to exist at all, the counts of odd and even numbers must be compatible with an alternating arrangement: |odd_count - even_count| ≤ 1, which is always true for consecutive integers 1..n. Specifically:
  - If n is even: odd_count == even_count == n/2, both starting parities work.
  - If n is odd: odd_count = even_count + 1, so the pattern must start and end with odd.
- Given a fixed prefix, the remaining positions have fixed required parities. The number of ways to fill them is (number of remaining odds)! × (number of remaining evens)!, provided the counts of remaining odds/evens exactly match the number of remaining slots of each parity; otherwise 0.
- Lexicographic order means we iterate candidate values for the next position in increasing order, count valid completions for each candidate, and subtract from k until we find the block containing k.

Pitfalls:
- k can be up to 10^15, but total counts can be astronomically larger (e.g., 50! × 50! ≈ 10^128). Python handles big integers natively, but we can cap counts at k (or some threshold) for efficiency — though with n ≤ 100, factorials are cheap anyway.
- Must use 1-indexed k carefully (k-th permutation, k ≥ 1).
- When n is odd, the first element must be odd; candidates of even parity at position 0 yield 0 completions and are skipped naturally by the counting function.
- Factorial precomputation up to 100 is trivial.
- Edge case: if k exceeds total count, return [].

Algorithm outline:
1. Precompute factorials fact[0..n].
2. Define count(odd_rem, even_rem, next_parity, slots_rem): determines required parity slots; if mismatch, return 0; else return fact[odd_rem] * fact[even_rem].
3. Greedily build the permutation: maintain used set, remaining odd/even counts, and required parity for the next position (None for the first position, meaning either parity allowed — but constrained by counts).
4. For each position, iterate candidate values v from 1..n not used, check parity compatibility, compute completions, and either skip (k -= completions) or select (append v, update state).
5. If at any point no candidate works or k > total, return [].

Complexity: O(n^2) candidate checks with O(1) counting each — trivially fast for n = 100.

## worker: Implement the complete solution: precompute factor
- **Approach**: Greedy position-by-position construction using combinatorial counting (like the classic k-th permutation, with a parity constraint).
- **Counting**: Once the parity of the next position is fixed, the parity pattern of all remaining slots is determined. The remaining slots demand exact counts of odd/even numbers; if the remaining pool matches, completions = `odd_rem! * even_rem!`, else 0.
- **First position**: `next_parity=None` sums over both possible starting parities. For odd n, even-start patterns automatically yield 0 because counts won't match (odd count = even count + 1 forces odd start).
- **k-out-of-range**: Checked upfront via total count; also guarded inside the loop (`found` flag).
- **Verification against examples**:
  - n=4, k=6 → builds [3,4,1,2] ✓
  - n=3, k=2 → [3,2,1] ✓ (n odd forces odd start; [1,2,3] first, then [3,2,1])
  - n=2, k=3 → total = 2 < 3 → [] ✓
  - n=1, k=1 → [1]; n=1, k=2 → [] ✓
- **Complexity**: O(n²) candidate iterations, each O(1) counting with precomputed factorials. Big integers handled natively by Python (counts can reach ~50!·50!, far exceeding 10^15, which is fine).
