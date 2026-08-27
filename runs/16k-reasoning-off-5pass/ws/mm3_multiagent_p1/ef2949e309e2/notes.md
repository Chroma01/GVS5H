
## ideation
The problem asks for the number of subsequences of length 5 where the middle element is the unique mode. A brute-force O(n^5) approach is infeasible for n up to 1000. We need an O(n^2) solution.

The standard approach is to iterate over the middle index `m`. For each `m`, we choose 2 elements from the left and 2 from the right. The total pairs is `C(m, 2) * C(n-1-m, 2)`. We subtract pairs where some other value appears at least twice (making the middle not the unique mode).

Using inclusion-exclusion on events A (left duplicate), B (right duplicate), C (cross duplicate) for values `v != nums[m]`:
- `|A|`, `|B|`, `|C|` are computable in O(k) where k is distinct values.
- `|A ∩ B| = S_L * S_R` (independent choices).
- `|A ∩ C|`, `|B ∩ C|`, `|A ∩ B ∩ C|` are also O(k).

This yields an O(n^2) algorithm. We can precompute prefix/suffix frequency maps to get `cL_v` and `cR_v` for each `m` in O(1) per query, or just rebuild maps per `m` since n=1000.

Pitfalls:
- Must exclude `nums[m]` from the "bad" values.
- Modulo 10^9+7.
- Careful with combinations (C(x,2) = 0 if x < 2).

## worker: Implement the O(n^2) solution in Python: for each 
The solution uses an O(n^2) approach with inclusion-exclusion to count valid pairs of (left, right) elements for each middle index `m`.

**Key Insights:**
1. **Total pairs**: For a middle index `m`, we choose 2 elements from the left (`L` indices) and 2 from the right (`R` indices). Total = `C(m, 2) * C(n-1-m, 2)`.
2. **Bad events**: The middle `nums[m]` fails to be the unique mode if any other value `v` appears at least twice in the 4 chosen elements. This occurs if:
   - `A_v`: `v` appears twice in the left
   - `B_v`: `v` appears twice in the right  
   - `C_v`: `v` appears once in both left and right
3. **Inclusion-exclusion**: 
   - `|A|`, `|B|`, `|C|` are computed directly
   - `|A ∩ B| = S_L * S_R` (independent choices: any left duplicate combines with any right duplicate)
   - `|A ∩ C|`, `|B ∩ C|`, `|A ∩ B ∩ C|` require same value `v`, so they are sums over `v`
4. **Efficiency**: We precompute prefix and suffix frequency maps to get `cL_v` and `cR_v` in O(1) per query. For each `m`, we iterate over distinct values present in left or right (at most n), making it O(n) per `m`, total O(n²).

**Pitfalls handled:**
- Excluding `nums[m]` from the "bad" values
- Using modular arithmetic to avoid negative numbers
- Handling small values where combinations return 0
