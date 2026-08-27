- **Marginal costs:** For a product with price \(P_i\), buying the \((x+1)\)-st unit increases the cost from \(P_i x^2\) to \(P_i(x+1)^2\), so its marginal cost is \(P_i(2x+1)\). The marginal costs for each product are therefore an increasing sequence.
- **Optimality:** Any minimum-cost purchase of a fixed number of units consists of taking the globally cheapest marginal costs. Thus, for an integer threshold \(T\), taking every marginal cost at most \(T\) gives a valid prefix for every product and the minimum-cost set containing that many units.
- **Counting units:** The number of marginal costs of product \(i\) not exceeding \(T\) is
  \[
  q_i(T)=\left\lfloor\frac{\lfloor T/P_i\rfloor+1}{2}\right\rfloor.
  \]
  The corresponding purchase cost is \(\sum_i P_i q_i(T)^2\).
- **Threshold search:** This cost is monotone in \(T\). Binary search finds the largest feasible threshold \(T\). The upper bound is made infeasible using \(P_{\min}\): let \(x=\lfloor\sqrt{\lfloor M/P_{\min}\rfloor}\rfloor+1\), then \(P_{\min}x^2>M\), so threshold \(P_{\min}(2x-1)\) is infeasible.
- **Tie handling:** After all marginal costs at most \(T\) are selected, every next available marginal has cost exactly \(T+1\). Let \(E\) be their count and \(R\) the remaining budget. Add \(\min(E,\lfloor R/(T+1)\rfloor)\) of them. Since \(T\) is maximal feasible, no later marginal can be used after this.
- **Complexity:** Each threshold check is \(O(N)\), and the binary search uses \(O(\log V)\) checks, giving \(O(N\log V)\) time and \(O(1)\) auxiliary space. Python integers safely handle all intermediate values.
