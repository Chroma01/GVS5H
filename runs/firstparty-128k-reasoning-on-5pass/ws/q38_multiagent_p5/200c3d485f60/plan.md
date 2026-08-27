Model each array by its `n - 1` adjacent edges, marking exactly `k` edges as equal and the rest as unequal.  
For any fixed choice of `k` equal edges, the array is split into `n - k` contiguous runs, and adjacent runs must have different values.  
The number of valid value assignments for a fixed run partition is `m` choices for the first run and `m - 1` choices for each later run, giving `m * (m - 1)^(n - k - 1)`.  
Since the equal-edge positions can be chosen independently, multiply by `C(n - 1, k)`.  
Compute the binomial coefficient modulo `10^9 + 7` using factorials and inverse factorials, and use fast modular exponentiation for the power.  
The `m = 1` case is handled naturally by treating `0^0` as `1` when `k = n - 1`.