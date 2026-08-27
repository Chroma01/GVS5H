
## ideation
The core difficulty is computing whether the Levenshtein edit distance is at most a small threshold \(K\) for strings whose lengths may be as large as 500,000. A full dynamic-programming table is too expensive, so the algorithm must exploit the small threshold and avoid processing states that cannot possibly lead to an answer within \(K\) edits. The length difference gives an immediate necessary-condition rejection. Any bounded-distance method must also handle insertions and deletions correctly, including cases where the optimal alignment shifts substantially.

## worker: Derive and implement a correct banded Levenshtein 
The dynamic-programming state is the Levenshtein distance for prefixes `S[:i]` and `T[:j]`. Any state with `|i-j| > K` already requires more than `K` insertions/deletions, so it cannot contribute to a solution of cost at most `K`.

Only the band `|i-j| <= K` is maintained. Two rolling arrays store consecutive rows, using offsets because each row has a potentially different band start. The algorithm runs in `O(K * max(|S|, |T|))` time and `O(K)` memory.
