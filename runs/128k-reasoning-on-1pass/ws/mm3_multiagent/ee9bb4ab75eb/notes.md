
## ideation
**Core difficulty**  
For each index `i` we must determine the largest `L` such that among the `n‑1` remaining words there are at least `k` words sharing a common prefix of length `L`.  
A naïve solution would examine every length for every removal (≈ `n·maxLen`) which is far too slow (`n, Σ|words| ≤ 10⁵`). The key is to understand how the count of each prefix changes when exactly one word is removed.

**Candidate approaches**  
1. **Pre‑compute prefix frequencies** – Build a trie (or a hash map of prefixes) and store for every node its occurrence count `cnt`.  
2. **Classify lengths** – For each length `L` compute  
   * `M[L] = max cnt` of any prefix of length `L`.  
   * `C[L] = number of prefixes of length `L` with `cnt = k`.  
   A length is *universal* (works for every removal) if `M[L] ≥ k+1` or (`M[L] = k` and `C[L] ≥ 2`).  
   A length is *special* if `M[L] = k` and `C[L] = 1`; it works for a removal `i` only when the removed word does **not** have that unique prefix.  
3. **Answer per index** – Let `L0` be the maximum universal length. For lengths larger than `L0` we only have the special ones. For each word we build the set `Bad[i]` of special lengths whose unique prefix it possesses. Then the answer for `i` is `max( L0, max{ L ∈ special | L ∉ Bad[i] } )`.  
4. **Special case `k = 1`** – The “longest common prefix of any 1 string’’ is simply the longest word that remains. This can be solved in `O(n)` by finding the maximum word length and checking how many words attain it.  
5. **Complexities** – Building the trie is `O( Σ|words| )`. Computing `M` and `C` is a single pass over the trie (`O( Σ|words| )`). Building all `Bad[i]` also touches each character once (`O( Σ|words| )`). Scanning the special list for each `i` performs at most `|Bad[i]|+1` membership tests, so the total number of tests is `n + Σ|Bad[i]| ≤ n + Σ|words|`. Thus the whole algorithm runs in `O(n + Σ|words|)` time and `O( Σ|words| )` memory.

**Pitfalls / Edge cases**  
* **Insufficient strings after removal** – If `n‑1 < k` every answer must be `0`. This must be handled before any positive `L` is considered.  
* **`k = 1`** – The general formula does not apply; the answer is the longest word that can still be chosen.  
* **Unique prefix condition** – For a special length we must verify that it is the *only* prefix with count `k` at that depth (`M[L] = k` **and** `C[L] = 1`). Otherwise the length is already universal.  
* **Word length vs. prefix length** – A word cannot block a length larger than its own length; the traversal automatically respects this.  
* **Scanning special lengths** – To keep the total work linear, we must break after finding the first special length not in `Bad[i]`. A naïve full scan for every `i` could become `O(n·maxLen)`.  
* **Off‑by‑one in depth** – The trie node’s depth equals the prefix length; ensure indices are consistent when filling `M`, `C`, and `Bad`.  
* **Large alphabet** – The trie uses 26 children per node; with `Σ|words| ≤ 10⁵` the total number of nodes is bounded, so memory is safe.  
* **All words identical** – `M[L] = n` for all `L ≤ minLen`; if `n ≥ k+1` then `L0 = minLen` and no special lengths exist, yielding the correct answer.  
* **All words distinct** – Usually `M[L] < k` for every `L`, so `L0 = 0` and `special` stays empty, giving zeros as expected.
