- **Contribution decomposition:** For a permutation, a value \(x\) contributes \(x \cdot 10^L\), where \(L\) is the total number of decimal digits among values placed after \(x\).

- **Fixing one value:** Fix \(x\), and choose exactly a subset \(B\) of the other \(N-1\) values as the suffix after \(x\). If \(|B|=k\), there are \(k!(N-1-k)!\) permutations with exactly this suffix set. Thus its aggregate multiplier is \(\sum_{k=0}^{N-1} k!(N-1-k)![z^k]G(z)\), where \(G(z)\) encodes choices of suffix values weighted by powers of ten.

- **Generating polynomial:** Group values by digit length \(d\). Let \(c_d\) be the count of values of length \(d\), and let \(a_d=10^d\). Then \(F(z)=\prod_d(1+a_dz)^{c_d}\). If fixed value \(x\) has digit length \(d\), its excluded polynomial is \(G_d(z)=F(z)/(1+a_dz)\). The coefficient \([z^k]G_d\) is the sum of \(10^{\text{total suffix digits}}\) over all size-\(k\) suffix subsets excluding \(x\).

- **Computing \(F\) efficiently:** Direct multiplication is too slow. Let \(Q(z)=\prod_d(1+a_dz)\), using one factor per distinct digit-length class, and \(P(z)=\sum_d c_da_d\prod_{e\ne d}(1+a_ez)\). Logarithmic differentiation gives \(Q(z)F'(z)=P(z)F(z)\). Comparing coefficient \(z^{n-1}\) yields an order-\(D\) recurrence for \(F_n\), computable in \(O(ND)\). Here \(D\le 6\).

- **Computing excluded polynomials:** For each class with factor \(1+az\), polynomial division is the recurrence \(G_0=1\), \(G_k=F_k-aG_{k-1}\). This computes all coefficients of one excluded polynomial in \(O(N)\). Repeating for all digit lengths costs \(O(ND)\).

- **Final aggregation:** All values in the same digit-length class have the same multiplier. Multiply that multiplier by the arithmetic-series sum of all values in the class, then sum over classes modulo 998244353.

- **Complexity:** Time \(O(ND)\), memory \(O(N)\), where \(D\le 6\). Modular inverses through \(N\) exist because \(N<998244353\).
