We need S = sum over all completions B (replace each 0 in A with any 1..p-1) of B^p mod p. By Fermat's little theorem, for any B with entries in Z/pZ, B^p ≡ B (mod p) (Frobenius endomorphism) when p is prime. So S ≡ sum_B B (mod p). 

We must compute T = sum_B B, an N×N matrix, where each zero in A can be filled with any of (p-1) values in {1,...,p-1}, and each nonzero entry is fixed. The sum T_{i,j} = (number of completions) * (contribution depending on zeros). 

Number of completions: Z = (p-1)^K, where K = number of zeros. A specific cell (i,j):
- If A_{i,j} ≠ 0, its contribution appears in every completion → contributes A_{i,j} * Z.
- If A_{i,j} = 0, we sum over all choices x∈{1,...,p-1} of x, multiplied by the number of ways to fill the other K-1 zeros. The sum of x from 1 to p-1 is (p-1)p/2. Contribution: (p-1)p/2 * (p-1)^(K-1).

Since p may not divide (p-1), compute modulo p:
- Z = (p-1)^K mod p. By FLT, (p-1)^p ≡ 1, and p is prime; note p-1 ≡ -1 (mod p), so Z ≡ (-1)^K (mod p).
- (p-1)p/2 * (p-1)^(K-1): factor p kills it modulo p → contribution ≡ 0 (mod p).

So the final answer is simply T_{i,j} ≡ A_{i,j} * (-1)^K (mod p) for nonzero A_{i,j}, and 0 for zero entries (since the "zero" entry was originally 0, and summing all B_{i,j} over completions gives 0 mod p).

Algorithm:
- Read N, p, matrix A.
- Count K = number of zero entries.
- Compute s = 1 if K even, else -1 (mod p); equivalent to s = (-1)^K mod p. In Python modulo: s = p-1 if K%2 else 1.
- For each i,j: if A[i][j] != 0: print (A[i][j] * s) % p else print 0.

Proof sketch: For each cell (i,j) the total over B is Z * A_{i,j} for nonzero, else (p-1)p/2 * Z/(p-1) = Z * p/2. Mod p the second is 0 and Z ≡ (-1)^K.