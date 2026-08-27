- **Reduction count:** A positive value `x` needs `k` operations to reach zero when `4^(k-1) <= x < 4^k`. Costs are therefore `1` on `[1, 3]`, `2` on `[4, 15]`, `3` on `[16, 63]`, and so on.

- **Prefix sum:** `prefix_cost(n)` sums the costs of all values in `[1, n]` by processing geometric intervals `[4^(k-1), 4^k - 1]`. Each query is answered by subtracting two prefix sums.

- **Combining reductions:** One operation performs one reduction on two array elements, so the minimum number of operations is `ceil(total_reductions / 2)`, implemented as `(total_reductions + 1) // 2`.

- **Correctness of pairing:** The largest reduction chain can always be paired with reductions from other elements in the interval. Since every query contains at least two values (`l < r`), any odd final reduction can be paired with an already-zero element.

- **Verified outputs:**  
  `[[1, 2], [2, 4]]` returns `3`.  
  `[[2, 6]]` returns `4`.  
  `[3, 4]` has total cost `3`, so returns `2`.  
  `[4, 5]` has total cost `4`, so returns `2`.

- **Boundary values:** Costs are correctly assigned as `cost(1)=1`, `cost(3)=1`, `cost(4)=2`, `cost(15)=2`, `cost(16)=3`, and `cost(64)=4`.

- **Complexity:** Each query takes `O(log_4 r)` time and `O(1)` extra space. Python integers safely handle the aggregate answer.
