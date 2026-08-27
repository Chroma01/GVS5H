We need to count substrings where the numeric value is divisible by the non-zero last digit. Since length can be 10^5, enumerating all O(n^2) substrings is impossible. Instead, we fix the ending position and try to find all starting positions that produce substrings divisible by the last digit. For each ending index j, let d = s[j] (1–9). We need to find i ≤ j such that the number represented by s[i..j] (mod d) is 0. Maintaining a running prefix sum modulo d allows checking each i in O(1), but iterating over all i per j would still be O(n^2).

Observe that we only need to know, for each possible prefix remainder r in [0, d-1], how many earlier prefix positions have that remainder. While the set of remainders can be up to d (≤9), we can store a dictionary of size d for each ending position. By updating this dictionary as we scan j from 0 to n-1, we can count matches in O(d) per step, where d ≤ 9. Hence total time O(9·n) = O(n). Space O(n) (or O(9) per step) suffices.

Algorithm:
1. Convert string to list of ints.
2. Initialise answer = 0.
3. For each digit d from 1 to 9:
   - Keep a dictionary `cnt` of remainders seen so far for current d.
   - Keep running value `val = 0`, `pow10 = 1` (10^k mod d) as we extend substring to the right.
   - Iterate j from 0 to n-1:
     - Update `val = (val + int(s[j]) * pow10) % d`.
     - If `val == 0`, the substring from 0..j is divisible by d → add 1 to answer (since empty prefix contributes remainder 0 only when j==0? Actually `cnt[0]` handles it; we initialise `cnt[0] = 1`.)
     - Add `cnt[val]` to answer (number of earlier prefixes with same remainder).
     - Increment `cnt[val]`.
     - Update `pow10 = (pow10 * 10) % d`.
4. Return answer.

This counts all substrings whose last digit is d and which are divisible by d. Single‑digit substrings with d are automatically counted (they have remainder 0). Leading zeros are allowed; the construction works because the value is built left‑to‑right, handling zeros naturally.