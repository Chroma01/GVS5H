- **Canonical events:** Every mandatory mismatch is flipped exactly once. Extra useful operations can only be temporary pairs on indices with \(A_i=B_i=1\): flip \(1\to0\), then later \(0\to1\). Temporary pairs on zero bits are never beneficial.
- **Event ordering:** If a flip changes the weighted active sum by \(\Delta\), swapping adjacent events shows the smaller \(\Delta\) should occur first. Therefore all negative changes come first, ordered by decreasing magnitude, followed by positive changes ordered by increasing magnitude.
- **Optional selection:** Replacing a selected optional pair of cost \(y\) with an unselected pair of larger cost \(x\) never increases any intermediate state: removing \(x\) lowers the state more, and restoring it ends at the same state. Thus it suffices to test prefixes of optional costs sorted descending.
- **Cost formula:** For negative magnitudes \(x_i\) in descending order and positive magnitudes \(y_i\) in ascending order,
  \[
  \text{cost}=(q+r)S-W_- - rT_-+W_+,
  \]
  where \(S\) is the initial weighted sum, \(T_-\) is the total negative magnitude, and each weighted sum uses the event's coefficient in the resulting schedule.
- **Bug in the previous code:** It both performed an \(O(N)\) list construction inside every optional iteration, causing \(O(N^2)\) time, and incorrectly increased all existing negative coefficients when inserting an optional negative event. Only existing negative magnitudes greater than the inserted value increase their coefficients. For positive events, only existing magnitudes less than the inserted value increase.
- **Complexity:** Prefix sums and binary searches make every optional insertion \(O(\log N)\), for total \(O(N\log N)\) time and \(O(N)\) memory.
