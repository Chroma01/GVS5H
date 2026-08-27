
## ideation
- **Core difficulty** – Count numbers in `[l, r]` ( 1 ≤ l ≤ r < 10⁹) for which the product of the decimal digits is divisible by the sum of the digits. Direct enumeration is impossible (up to 10⁹ numbers).  
- **Key observations**  
  1. If a digit `0` appears, the product becomes `0` and is divisible by any positive sum → the number is automatically beautiful. This greatly simplifies the condition.  
  2. For numbers without any `0`, the product’s prime factors can only be `2, 3, 5, 7`.  
  3. The sum of digits is at most `9 × 9 = 81`. For each possible sum we can pre‑compute the required prime exponents (`2,3,5,7`). If the sum contains any other prime factor, the condition can never be satisfied.  
  4. The problem therefore reduces to a **digit DP** that tracks the current digit position, whether we are still tight to the bound, whether the number has started (to handle leading zeros), the current digit sum, and the exponents of the product.  
  5. When a zero digit is placed after the number has started we can stop tracking the product and simply count all possible suffixes (the result is always beautiful). A tiny auxiliary DP can count those suffixes efficiently (10^(remaining) when not tight, otherwise enumerate).  
- **Pitfalls to watch for**  
  - Excluding the number `0` itself (no positive integer).  
  - Correctly handling leading zeros: the DP must allow the “started” flag to stay false while the prefix is zero, and only start counting when a non‑zero digit appears.  
  - Off‑by‑one in the interval: answer = `count(r) – count(l‑1)`.  
  - Summations that are impossible (e.g., 77 = 7·11) must be marked as `None` in the need‑table so the DP returns 0 for such sums.  
  - Keeping the exponent ranges within plausible limits (e2 ≤ 27, e3 ≤ 18, e5 ≤ 9, e7 ≤ 9) to keep the state space small.  
  - When a zero digit is encountered, we must not continue updating the product exponents; we switch to the zero‑suffix DP.  
  - Memoisation depth is at most the number of digits (≤ 9), so recursion is safe, but we still use `lru_cache` for clarity.
