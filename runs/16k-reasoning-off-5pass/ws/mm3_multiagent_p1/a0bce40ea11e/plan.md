We need S = sum_{B} B^p (mod p) where B ranges over all matrices obtained by replacing zeros of A with any value in {1,…,p−1}. Since p is prime, by Fermat's little theorem x^p ≡ x (mod p) for any integer x. Thus B^p ≡ B (mod p) for every B, and S ≡ sum_{B} B (mod p).

Let the set of zero positions be Z. For any position (i,j):
- If A_{i,j} ≠ 0, its contribution to the sum is (p−1)^K · A_{i,j} (since this entry is fixed across all B).
- If A_{i,j} = 0, its contribution to the sum is sum_{x=1}^{p−1} x · (p−1)^{K−1} = (p−1)^{K−1} · (p−1)p/2.

All computations are done modulo p. The factor (p−1)^K ≡ (−1)^K (mod p). For p=2, the special case when p−1=1 still holds: sum_{x=1}^{1} x = 1, and the same formula (p−1)^{K−1}·p/2 works because 2 divides p.

Algorithm:
1. Read N, p, matrix A.
2. Count K = number of zeros.
3. For each cell (i,j):
   - If non-zero: val = A[i][j] · ((−1)^K mod p) mod p.
   - If zero: val = ((p−1)·(p/2) mod p) · ((−1)^{K−1} mod p) mod p. Precompute t = (p−1)·inv2 mod p where inv2 = (p+1)/2, then val = t · (−1)^{K−1} mod p.
4. Output the N×N result matrix.

Complexity: O(N^2).