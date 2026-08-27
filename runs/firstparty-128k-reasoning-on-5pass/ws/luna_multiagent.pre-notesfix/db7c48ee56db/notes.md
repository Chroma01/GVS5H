
## ideation
The core difficulty is that the sequence can be very large, so considering all subsets is normally impossible. However, the condition \(\binom{N}{K}\le 10^6\) guarantees that the number of valid selections is manageable. The useful reduction is to choose whichever is smaller: the \(K\) selected elements or the \(N-K\) omitted elements.

Let \(T\) be the XOR of every element, and let \(r=\min(K,N-K)\). If \(K\le N-K\), enumerate each \(K\)-element subset directly. If \(K>N-K\), enumerate each \(r=N-K\)-element omitted subset; its corresponding chosen-set XOR is \(T\oplus\text{omitted\_xor}\). The maximum over these values is the answer.

Several implementation concerns matter:
- The elements are distinct by position, even when values are duplicated.
- XOR accumulation should be based on indices or selected positions, not unique values.
- The complement transformation must use the XOR of all elements exactly once.
- The enumeration count is bounded, but repeatedly recomputing a subset XOR from scratch may add an unnecessary factor of \(r\).
- Since values are below \(2^{60}\), ordinary Python integers handle all XOR operations safely.

## worker: Implement the complete Python solution using \(r=\
Enumerate subsets of size `r = min(K, N-K)`, whose count equals `C(N, K)` and is at most `10^6`.

- If `r = K`, the XOR of the chosen elements is enumerated directly.
- If `r = N-K`, enumerate omitted subsets. The chosen XOR is `total_xor ^ omitted_xor`.
- `itertools.combinations` treats equal values at different positions as distinct choices.
- The `r = 0` case is naturally handled by `combinations(..., 0)`, producing one empty subset with XOR `0`.
