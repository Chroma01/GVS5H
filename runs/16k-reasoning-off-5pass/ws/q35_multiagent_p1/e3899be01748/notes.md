
## ideation
The core difficulty lies in efficiently counting substrings ending at each position that are divisible by their last non-zero digit without checking all $O(N^2)$ substrings. A brute-force approach is too slow for $N=10^5$.

The key insight is to iterate through each possible non-zero last digit $d \in \{1, \dots, 9\}$ separately. For a fixed $d$, we only care about substrings ending at indices $j$ where $s[j] == d$. For such a substring $s[i..j]$, we need $int(s[i..j]) \equiv 0 \pmod d$.

We can maintain the state of remainders for all substrings ending at the previous position. Specifically, for a fixed $d$, let `freq[r]` be the count of starting indices $i$ (for substrings ending at the current position's predecessor) such that the value of the substring modulo $d$ is $r$. When moving from position $j-1$ to $j$, the value of any substring $s[i..j-1]$ becomes $s[i..j-1] \times 10 + s[j]$. Therefore, the new remainder for substring $s[i..j]$ (where $i < j$) is $(old\_rem \times 10 + s[j]) \pmod d$. Since we are only interested in cases where the last digit is $d$, we specifically look at positions where $s[j] == d$. At these positions, the term $s[j] \pmod d$ is 0, so the new remainder is simply $(old\_rem \times 10) \pmod d$.

The algorithm is:
1. Initialize `total = 0`.
2. For each digit $d$ from 1 to 9:
    a. Initialize a frequency array `freq` of size $d$ with zeros. This tracks the counts of remainders for substrings ending at the previous index.
    b. Iterate through the string $s$ with index $j$ from 0 to $n-1$:
        i. Update the frequency array: Create a new frequency array `new_freq` where `new_freq[(r * 10) % d] = freq[r]` for all $r$. This accounts for appending $s[j]$ to all previous substrings. Note: The actual value added is $s[j]$, but since we only check divisibility when $s[j] == d$, and $d \equiv 0 \pmod d$, the term $s[j] \pmod d$ is 0. So the transition is just multiplication by 10 modulo $d$.
        ii. If $s[j] == str(d)$:
            - The substrings ending at $j$ with start index $i < j$ have remainders given by `new_freq`. We add `new_freq[0]` to `total` because these substrings are divisible by $d$.
            - The single-digit substring $s[j..j]$ has value $d$, which is divisible by $d$. Add 1 to `total`.
        iii. Set `freq = new_freq`.
3. Return `total`.

Complexity: $9 \times N \times 9$ operations, which is $O(N)$. This fits within the constraints.

Pitfalls:
- Forgetting that the single-digit substring $s[j..j]$ is always divisible by $s[j]$ if $s[j] \neq 0$.
- Incorrectly updating the frequency array. The update must happen for every character to maintain the state for future positions, even if the current character is not $d$.
- Using the wrong modulus or not handling the modulo arithmetic correctly.

## worker: (none)
The solution iterates over each possible non-zero last digit `d` from 1 to 9. For each `d`, it maintains a frequency array `freq` where `freq[r]` is the count of substrings ending at the previous index that have a remainder `r` when divided by `d`. 

For each character `s[j]` in the string:
1. It updates the frequency array to reflect the new remainders when `s[j]` is appended to all previous substrings. The new remainder is `(old_rem * 10 + int(s[j])) % d`.
2. If `s[j]` equals `d`, then:
   - All substrings ending at `j` (with start index `i < j`) that have a remainder of 0 modulo `d` are divisible by `d`. We add `new_freq[0]` to the total count.
   - The single-digit substring `s[j..j]` (which is just `d`) is always divisible by `d`, so we add 1 to the total count.
3. The frequency array is updated for the next iteration.

This approach runs in $O(9 \cdot N \cdot 9) = O(N)$ time, which is efficient for $N \le 10^5$.
