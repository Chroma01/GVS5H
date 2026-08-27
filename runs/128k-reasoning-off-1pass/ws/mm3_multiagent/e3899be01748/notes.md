
## ideation
The problem requires counting substrings whose integer value is divisible by its non-zero last digit. Since the last digit is at most 9, we can treat each possible last digit independently. For each ending position `j`, the divisor is fixed, and we need to count starting positions `i ≤ j` such that the substring value is 0 mod that digit.

Key observations:
- For `d=1,2,5`: any substring ending with `d` is automatically divisible (since the last digit guarantees divisibility, and higher powers of 10 contribute multiples of `d`). So we just add `j+1` for each such ending position.
- For `d=3,9`: `10 ≡ 1 (mod d)`, so the value mod `d` is the sum of digits mod `d`. We can use prefix sums of digits modulo `d` and a frequency array to count matching prefixes in O(1) per position.
- For `d=6`: since the last digit is 6, the number is even; divisibility by 6 is equivalent to divisibility by 3. So we can reuse the prefix-sum mod 3 method.
- For `d=4`: `10^2 ≡ 0 (mod 4)`. For substrings of length ≥ 3, only the last two digits matter. We can check the two-digit suffix and add `j-1` for all longer substrings if valid, plus handle lengths 1 and 2 explicitly.
- For `d=8`: `10^3 ≡ 0 (mod 8)`. For substrings of length ≥ 4, only the last three digits matter. Similarly, we check the three-digit suffix and add `j-1` for length ≥ 3 if valid, plus handle lengths 1 and 2.
- For `d=7`: `10^6 ≡ 1 (mod 7)`, so powers of 10 mod 7 cycle with period 6. We maintain a 2D frequency array `cnt[i_mod_6][prefix_value_mod_7]`. For each ending position `j`, we query all six possible starting-position residue classes using the precomputed inverse of `10^k mod 7` to find the required prefix value. This is O(1) per position.

All methods are O(n) with small constant factors and O(1) extra space.
