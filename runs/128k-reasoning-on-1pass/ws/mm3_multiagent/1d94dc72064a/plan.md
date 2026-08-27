The game can be modeled as each index i having `v_i = A_i - 1` extra moves that become available after the index is first activated. The game ends when the last index is activated, and the player making that move wins. By analyzing small cases and computing Grundy numbers, we observe:

- For `N = 1`, Fennec always wins.
- For `N = 2`, Snuke always wins.
- For odd `N ≥ 3`, Snuke wins if and only if all `A_i` are even (i.e., all `v_i` are odd). Otherwise Fennec wins.
- For even `N ≥ 4`, Snuke wins if and only if the XOR of all `v_i = A_i - 1` is even. Otherwise Fennec wins.

This pattern matches all sample cases and can be implemented in O(N) time.