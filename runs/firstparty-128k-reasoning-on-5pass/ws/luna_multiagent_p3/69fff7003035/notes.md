- **Integral representation:** For a fixed element \(i\), assign every element an independent random real priority. Conditional on \(i\)'s priority being \(t\), each other element \(j\) is after \(i\) independently with probability \(t\). Thus the expected positional multiplier of \(i\) is
  \[
  C_i=\int_0^1\prod_{j\ne i}\bigl((1-t)+10^{d_j}t\bigr)\,dt.
  \]
  Multiplying by \(N!\) converts the expectation to the sum over all permutations.

- **Grouping:** Elements with the same decimal length \(d\) contribute the identical linear factor \(1+(10^d-1)t\). For a group of size \(c\), its polynomial is \((1+(10^d-1)t)^c\), whose coefficients are generated using binomial coefficients modulo \(998244353\).

- **Polynomial product:** Multiply all group polynomials with NTT-based convolution. There are at most six decimal-length groups for \(N\le 2\cdot10^5\), so the total complexity is \(O(N\log N)\).

- **Exclusion:** If \(F(t)=\prod_j(1+a_jt)\), then for a group parameter \(a\), the quotient \(Q(t)=F(t)/(1+at)\) satisfies \(q_0=1\) and \(q_k=F_k-aq_{k-1}\). Therefore \(C_i=\sum_k q_k/(k+1)\), computed in \(O(N)\) per distinct digit length.

- **Final weighting:** All elements in one digit-length group share the same \(C_i\). Their values are summed arithmetically, then multiplied by the common integral and by \(N!\).

- **Checks:** For \(N=3\), \(F(t)=(1+9t)^3\), the exclusion integral is \(37\), and \(6(1+2+3)37=1332\). For \(N=1\), the quotient is \(1\), yielding answer \(1\).
