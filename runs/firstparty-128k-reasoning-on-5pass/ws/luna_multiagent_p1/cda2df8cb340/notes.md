- **Valuation decomposition:** Let \(P_k\) be the sum of \(A_i+A_j\) over all \(i\le j\) such that \(2^k\mid A_i+A_j\). Pairs whose sums have exact 2-adic valuation \(k\) contribute \((P_k-P_{k+1})/2^k\). Summing over all \(k\) gives the required result.

- **Residue grouping:** For modulus \(m=2^k\), a pair sum is divisible by \(m\) exactly when the residues of its elements are \(r\) and \((-r)\bmod m\). Groups are represented by their element count and sum.

- **Distinct residue classes:** If two complementary residue classes have counts and sums \((c_1,s_1)\) and \((c_2,s_2)\), their contribution is \(s_1c_2+s_2c_1\), counting every unordered cross-class pair once.

- **Self-complementary classes:** When \(r=(-r)\bmod m\), all pairs inside the class qualify. Distinct pairs contribute each element once, while a diagonal pair contributes twice its element value. Therefore the total is \((c+1)s\), not \(cs\).

- **Complexity:** There are \(O(\log \max A_i)\) powers of two, and each level takes \(O(N)\) expected time using a dictionary. Total complexity is \(O(N\log \max A_i)\), with \(O(N)\) additional memory.
