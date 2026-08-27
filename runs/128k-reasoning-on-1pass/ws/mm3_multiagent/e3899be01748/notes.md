
## ideation
The problem asks for the number of substrings whose integer value is divisible by its non‑zero last digit.  
For a substring `s[l..r]` (inclusive) with length `L = r-l+1` and last digit `d = s[r]` we have  

```
X = pref[r+1] – pref[l]·10^L
```

where `pref[i]` is the integer value of the prefix `s[0..i‑1]`.  
The condition `X % d == 0` is equivalent to  

```
pref[r+1] ≡ pref[l]·10^L   (mod d)
```

For a fixed digit `d (1…9)` the factor `10^L (mod d)` repeats with a very small period (period ≤ 6, pre‑period ≤ 9).  
We keep, for the current right end `r`, a small set of buckets that store the remainders of all prefixes `pref[l]` that are at a certain distance `r-l` from `r`.  
When `r` moves one step to the right all distances increase by one, which is simulated by rotating the buckets and inserting the new prefix `pref[r]`.

Because `d ≤ 9` each bucket can be stored as a list of `d` counters (the counts of each remainder).  
For a bucket with factor `f` we need the remainders `a` with `a·f % d == pref[r+1]`.  
Since `d` is tiny we can pre‑compute, for every possible factor `f` and every possible target remainder `t`, the list of `a` that satisfy the congruence (`need[f][t]`).  
The algorithm runs in `O(n)` time (≈ 200 simple operations per character) and `O(1)` extra memory.

## worker: Implement the precomputation for each digit `d` (1
The solution uses a precomputation for each digit `d` (1 … 9) of the sequence of powers of 10 modulo `d`. Because `d` is at most 9, this sequence has a short preperiod (`p0`) and period (`p`). The precomputed data includes:
- `total[d] = p0 + p`
- `factor[d][i] = 10^{i+1} mod d` for `i = 0 .. total[d]-1`
- `need[d][f][t]`: all residues `a` such that `(a * f) % d == t`.

The main algorithm iterates over the string, maintaining for each `d` a circular buffer of buckets (size `total[d]`). Each bucket stores, for a given distance from the current right end, how many prefixes have each possible remainder modulo `d`. When moving to the next character, the buffer is rotated (simulating the increase of all distances by one) and the new prefix remainder is inserted into the distance‑0 bucket. For a character with last digit `d`, we examine all distances, and using the precomputed `factor` and `need` tables we count the matching prefixes in O(total[d] * d) time. The whole process runs in O(n) with a small constant factor.

## worker: **Precompute data for each digit d = 1..9** – comp
The solution uses the mathematical reformulation:

For a substring `s[l..r]` with last digit `d = s[r]` (non‑zero) and length `L = r-l+1`,
the condition `value(s[l..r]) % d == 0` is equivalent to  
`pref[r+1] ≡ pref[l] * 10^L (mod d)`, where `pref[i]` is the integer value of the prefix `s[0..i-1]`.

For each digit `d (1..9)`, the sequence `10^L mod d` has a very short preperiod (`p0 ≤ 2`) and period (`p ≤ 6`).  
We maintain, for the current right end `r`, a set of buckets that store the remainders of all prefixes `pref[l]` grouped by the factor `10^L mod d`.  
When `r` moves one step to the right, all distances `L` increase by one, which is simulated by rotating a circular buffer and shifting a small preperiod array.

Because `d ≤ 9`, each bucket can be stored as an array of `d` counters.  
For a bucket with factor `f`, we need the remainders `a` such that `(a * f) % d == pref[r+1] % d`.  
These are precomputed in `need[d][f][t]`.

The algorithm runs in `O(n)` time (≈ 200 simple operations per character) and `O(1)` extra memory.
