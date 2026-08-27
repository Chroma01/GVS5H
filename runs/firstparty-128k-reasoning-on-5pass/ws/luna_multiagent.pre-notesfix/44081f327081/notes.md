
## ideation
The core difficulty is avoiding examination of K-element subsets, whose number is enormous. The key reduction is to characterize a possible GCD by its divisors: a value d can be the GCD of a selected subset containing A_i only if A_i is divisible by d and at least K array elements are divisible by d. The actual GCD may be larger than d, but maximizing over all feasible divisors recovers the answer.

The large limits require careful attention to both time and memory. A direct per-element scan of all possible divisors is too slow, while repeatedly factoring values or creating large temporary lists may be costly. Duplicate values should be compressed where possible, and integer-frequency arrays are preferable to hash-heavy structures when the maximum value is only 10^6.

## worker: Develop an efficient Python implementation using f
For a divisor `d`, a selected K-element subset containing `A_i` can have GCD divisible by `d` exactly when:

- `d` divides `A_i`, and
- at least `K` array elements are divisible by `d`.

A multiples sieve computes the number of input elements divisible by every `d`. Processing feasible divisors in descending order assigns each value its largest possible divisor. The complexity is `O(M log M + N)`, with `M = max(A)`, and memory usage is `O(M + N)`.
