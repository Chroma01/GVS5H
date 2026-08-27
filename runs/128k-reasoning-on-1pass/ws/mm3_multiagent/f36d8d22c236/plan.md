We are given two strings `S` and `T` of length `N`.  
The operation replaces every occurrence of a chosen letter `x` with another letter `y`.  
We need the minimum number of operations to turn `S` into `T`, or report `-1` if impossible.

**Key observations**
- All occurrences of a letter behave identically, so for each letter `c` appearing in `S` there must be a single target letter `t(c)` that all its positions become. If not, impossible.
- The mapping `t: U → V` (where `U` = letters in `S`, `V` = target letters) defines a directed graph on the set `L = U ∪ V`.  
- In this graph, a connected component is either:
  * a tree rooted at a sink (a letter not in `U`), or
  * a tree rooted at a fixed point `c` with `t(c)=c`, or
  * a directed cycle of length ≥ 2 (no sink, no fixed point).
- The cost (minimum operations) for a component is:
  * `size_of_U` if it is a tree with an external sink,
  * `size_of_U - 1` if it is a tree with a fixed point,
  * `size_of_U + 1` if it is a cycle (needs a temporary node).
- Let `f` be the number of fixed points in `U` (self‑loops).  
  Let `C` be the number of cycle components (length ≥ 2).  
  The base cost (with enough temporary letters) is `|U| - f + C`.
- There are only 26 letters. Letters **not** in `L` are free temporaries (cost 0 extra).  
  If there are fewer free temporaries than cycles (`C > 26 - |L|`), each missing temporary adds one extra operation (we must use a letter from `L` as temporary and later restore it).