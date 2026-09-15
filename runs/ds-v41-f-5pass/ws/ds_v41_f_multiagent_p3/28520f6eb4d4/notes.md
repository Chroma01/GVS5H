- **Visibility reduction:** Building i is visible iff its top point is visible. If the top is blocked by a previous building j, any lower point on i is also blocked by j, because the line to a lower point lies strictly below the line to the top at x_j. Hence only tops matter.
- **Slope condition:** From P=(0,h), the line to top of building i has slope s_i = (H_i - h) / X_i. Building i is visible iff s_i > s_j for all j < i.
- **All visible:** All buildings are visible iff s_1 < s_2 < ... < s_N, equivalently s_i > s_{i-1} for every adjacent pair i-1, i.
- **Adjacent pair threshold:** For pair (i-1, i), s_i - s_{i-1} is an increasing linear function of h. It equals zero at
  h_i = (H_{i-1} * X_i - H_i * X_{i-1}) / (X_i - X_{i-1}).
  For h <= h_i, the pair violates strict increase, so building i is blocked.
- **Answer formula:** Not all buildings are visible iff h <= max_i h_i. Therefore the maximum height from which not all are visible is M = max_i h_i.
  - If M < 0, then at h = 0 all buildings are visible; output -1.
  - If M >= 0, output M (including M = 0, where touching counts as blocked).
  - For N = 1, there are no adjacent pairs; output -1.
- **Precision:** Compare candidate fractions exactly using integer cross multiplication: num * best_den > best_num * den, with positive denominators. Values fit easily in Python ints (up to ~1e36 products).
- **Output:** Convert the winning fraction to float and print with 18 decimal places. Float relative error is ~1e-16, well within the 1e-9 tolerance.
- **Edge cases:** M < 0 => -1 (Sample 2). M = 0 => 0.000... (Sample 3). M > 0 => exact threshold (Samples 1 and 4). Touching at the top of a previous building counts as intersection, so strict inequality is correct (confirmed by Sample 1 at h = 1.5).
- **Complexity:** O(N) time, O(N) memory. N up to 2e5.
