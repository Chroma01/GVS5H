- **Reduction:** Row and column flips commute and are involutions, so only their parities matter. For a fixed column-flip mask `c`, each row mask `m` can be left as-is or row-flipped, contributing `min(popcount(m xor c), W - popcount(m xor c))`.
- **Aggregation:** Count frequencies of row masks. The value for column mask `c` is `sum_m freq[m] * K[m xor c]`, where `K[d] = min(popcount(d), W - popcount(d))`. This is an XOR convolution on the hypercube of size `2^W`.
- **FWHT:** Use unnormalized integer FWHT. Forward transform both sides, multiply pointwise, inverse transform with the same butterfly, then divide all results by `N = 2^W`. All arithmetic is exact; intermediate values fit comfortably in Python integers.
- **Kernel transform optimization:** `K` is radial, so its FWHT depends only on the popcount `t` of the transform mask. Instead of building and transforming the full `K` array, compute `Khat[t]` directly by grouping masks by how many bits lie inside and outside the transform mask:
  `Khat[t] = sum_{j,l} (-1)^j C(t,j) C(W-t,l) K[j+l]`.
  This saves one full FWHT and is equivalent to transforming `K[mask]`.
- **Complexity:** `O(H + W * 2^W)` time and `O(2^W)` memory. With `W <= 18`, `N <= 262144`, and only two FWHTs are performed.
- **Implementation details:** Parse each row with `int(bytes, 2)`, precompute popcounts for all masks, and take `min(final_values) // N`. Early return for `W == 1` because the answer is always zero.
- **Pitfalls:** Bit order from `int(s, 2)` is irrelevant because only Hamming distances matter. The inverse transform result is `N` times the true convolution, so division by `N` is required. Final values are nonnegative, but intermediate FWHT values can be negative.
