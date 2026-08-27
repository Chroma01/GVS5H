- **Marginal costs:** The \(j\)-th unit of product \(i\) costs \(P_i(2j-1)\) additionally. Therefore, the optimal purchase for any fixed number of units consists of taking the globally cheapest marginal costs.
- **Threshold counting:** For an integer threshold \(X\), product \(i\) has
  \[
  q_i=\left\lfloor\frac{\lfloor X/P_i\rfloor+1}{2}\right\rfloor
  \]
  marginal costs at most \(X\). Their total cost is \(P_iq_i^2\).
- **Monotonicity:** \(F(X)=\sum_i P_iq_i^2\) is nondecreasing. Binary search finds the largest `lo` satisfying \(F(lo)\le M\); `hi = lo + 1` is the smallest threshold known to have \(F(hi)>M\).
- **Upper bound:** Use `hi = 2*M*min(P_i)+1`. For the product with minimum price \(p\), this threshold gives at least \(M\) units if \(p>1\), whose cost is \(pM^2>M\), or at least \(M+1\) units if \(p=1\), whose cost is \((M+1)^2>M\). Thus \(F(hi)>M\), including cases where every price exceeds \(2M+1\).
- **Boundary handling:** All marginal costs strictly below `hi` are counted in `units_below` and `cost_below`. A product contributes one marginal cost exactly equal to `hi` precisely when `hi % p == 0` and `hi // p` is odd. These boundary units all have the same cost, so the affordable number is
  \[
  \min(\text{boundary\_units}, (M-\text{cost\_below})//hi).
  \]
- **Complexity:** \(O(N\log(M\min P))\) time and \(O(1)\) extra space aside from the input. Python integers safely handle all intermediate values.
