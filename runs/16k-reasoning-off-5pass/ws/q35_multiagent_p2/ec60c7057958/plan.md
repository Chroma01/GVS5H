1. Count the number of odd (o) and even (e) numbers in the range [1, n].
2. Use dynamic programming to precompute the number of valid alternating permutations for remaining positions, given the count of remaining odd and even numbers and the parity of the last placed number. The state is `dp[remaining_odd][remaining_even][last_parity]`.
3. Construct the result permutation digit by digit (or number by number). For each position, iterate through available numbers in increasing order. For each candidate, calculate how many valid permutations start with that candidate.
4. If the count of permutations starting with the current candidate is less than k, subtract that count from k and try the next candidate.
5. If the count is greater than or equal to k, place the current candidate, update the state (decrement odd/even counts, update last parity), and move to the next position.
6. If at any point k exceeds the total number of valid permutations, return an empty list.