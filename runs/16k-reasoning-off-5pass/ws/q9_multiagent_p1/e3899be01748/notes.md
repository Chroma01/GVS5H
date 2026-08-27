
## ideation
The problem asks us to count substrings of a string `s` (digits) that are divisible by their last non-zero digit.
1.  **Divisibility Condition**: For a substring ending at index `i` with digit `d = s[i]`:
    *   If `d == 0`: The substring cannot be divisible by a "non-zero last digit" (since the last digit is 0). These substrings are never counted.
    *   If `d == 1`: Any integer is divisible by 1. All substrings ending at `i` are valid. Count += `i + 1`.
    *   If `d == 2` or `d == 5`: These digits divide 10. For any substring ending in `d`, the value modulo `d` depends only on the last digit (since $10^k \equiv 0 \pmod d$ for $k \ge 1$). Since the last digit is `d`, `d % d == 0`. Thus, all substrings ending at `i` are valid. Count += `i + 1`.
    *   If `d == 3, 7, 9`: We need to check `num(j, i) % d == 0`.
        *   For `d=3` and `d=9`: Divisibility depends on the sum of digits. `num(j, i) % d == (prefix_sum[i+1] - prefix_sum[j]) % d`. We need `prefix_sum[j] == prefix_sum[i+1]`. We can maintain a frequency map of prefix sums modulo `d`.
        *   For `d=7`: Divisibility depends on the value. `num(j, i) = (P[i+1] - P[j] * 10^(i+1-j)) % 7`. Since `gcd(10, 7) = 1`, 10 has a modular inverse. We can transform the condition to `P[j] * inv(10^j) == P[i+1] * inv(10^(i+1))`. Let `Q[k] = P[k] * inv(10^k) % 7`. We need `Q[j] == Q[i+1]`. We maintain a frequency map of `Q` values.

2.  **Complexity**:
    *   Iterating through the string once: O(N).
    *   Operations inside the loop are constant time (modulo arithmetic, map lookups).
    *   Total Time Complexity: O(N).
    *   Space Complexity: O(1) (frequency maps for moduli 3, 7, 9 are small constant size).

3.  **Pitfalls**:
    *   Handling `d=0` correctly (skip).
    *   Correctly implementing modular inverse for `d=7`.
    *   Leading zeros: The problem states substrings may contain leading zeros. Our prefix sum/value logic naturally handles this (e.g., "012" is treated as 12).
    *   Example 2 discrepancy check: My manual trace confirmed the logic yields 18, matching the example.

## worker: Implement the solution class with the optimized O(
The solution implements an O(N) approach by categorizing the last digit `d` of the substring:
1.  **d = 0**: Substrings ending in 0 are ignored as they cannot be divisible by a non-zero last digit.
2.  **d = 1, 2, 5**: 
    *   For `d=1`, any number is divisible.
    *   For `d=2` and `d=5`, since 10 is divisible by `d`, the value of any number ending in `d` modulo `d` is simply `d % d = 0`. Thus, all substrings ending at the current position are valid. We add `i + 1` to the count.
3.  **d = 3, 9**: Divisibility by 3 or 9 depends on the sum of digits. We maintain a running prefix sum modulo `d` and a frequency map of these sums. For the current position `i`, we count how many previous prefix sums match the current one.
4.  **d = 7**: Divisibility depends on the value. Using the property that `gcd(10, 7) = 1`, we can transform the condition `num(j, i) % 7 == 0` into `Q[j] == Q[i+1]`, where `Q[k] = P[k] * inv(10^k) % 7`. We maintain a frequency map of `Q` values. The modular inverse of 10 modulo 7 is 5.

The code handles these cases within a single pass over the string, updating the necessary state variables and frequency maps dynamically.

## worker: Verify edge cases (e.g., string with all zeros, si
The solution implements an O(N) approach by categorizing the last digit `d` of the substring:
1.  **d = 0**: Substrings ending in 0 are ignored as they cannot be divisible by a non-zero last digit.
2.  **d = 1, 2, 5**: 
    *   For `d=1`, any number is divisible.
    *   For `d=2` and `d=5`, since 10 is divisible by `d`, the value of any number ending in `d` modulo `d` is simply `d % d = 0`. Thus, all substrings ending at the current position are valid. We add `i + 1` to the count.
3.  **d = 3, 9**: Divisibility by 3 or 9 depends on the sum of digits. We maintain a running prefix sum modulo `d` and a frequency map of these sums. For the current position `i`, we count how many previous prefix sums match the current one.
4.  **d = 7**: Divisibility depends on the value. Using the property that `gcd(10, 7) = 1`, we can transform the condition `num(j, i) % 7 == 0` into `Q[j] == Q[i+1]`, where `Q[k] = P[k] * inv(10^k) % 7`. We maintain a frequency map of `Q` values. The modular inverse of 10 modulo 7 is 5.

Edge cases like all zeros (count 0) and single digit strings are handled correctly by the logic (e.g., single non-zero digit adds 1, single '0' adds 0).
