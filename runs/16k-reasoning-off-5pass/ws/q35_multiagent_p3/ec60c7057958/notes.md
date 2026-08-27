
## ideation
The core difficulty is that $n$ can be up to 100, which makes generating all permutations via backtracking infeasible due to the exponential number of permutations. The constraint $k \le 10^{15}$ suggests that we need an approach that is polynomial in $n$, likely involving combinatorics to skip over blocks of permutations.

The problem asks for the $k$-th lexicographically smallest "alternating permutation" where no two adjacent elements have the same parity. This is a specific type of permutation.

Key observations:
1. **Parity Structure**: In any alternating permutation of $[1, n]$, the parities of the elements at each position are fixed up to two possibilities:
   - Pattern A: Even, Odd, Even, Odd, ...
   - Pattern B: Odd, Even, Odd, Even, ...
   The number of even numbers ($E$) and odd numbers ($O$) in $[1, n]$ are determined by $n$:
   - $E = \lfloor n/2 \rfloor$
   - $O = \lceil n/2 \rceil$
   
   For a valid alternating permutation to exist:
   - If $n$ is even, $E = O = n/2$. Both patterns are possible.
   - If $n$ is odd, $O = E + 1$. Only Pattern B (starting with Odd) is possible because we have one more odd number. Pattern A would require starting with Even and ending with Even, which needs $E = O + 1$, impossible here.
   - If $n=1$, only one permutation [1] exists, which is Odd.

2. **Counting Permutations for a Fixed Parity Pattern**:
   Once the parity pattern is fixed (e.g., positions 0, 2, 4... must be even and positions 1, 3, 5... must be odd), the problem reduces to:
   - Assigning the available even numbers to the even positions.
   - Assigning the available odd numbers to the odd positions.
   - The assignment must be such that the resulting sequence is lexicographically ordered.
   
   Actually, the lexicographical order is determined by the actual values. We can use a "factorial number system" like approach but adapted for two independent sets (evens and odds).
   
   Let's define a function `count_ways(n_even, n_odd)` which returns the number of ways to arrange $n\_even$ even numbers and $n\_odd$ odd numbers into a sequence of length $n\_even + n\_odd$ such that the parities alternate according to a fixed pattern. 
   
   Wait, the parity pattern is fixed for the entire permutation. So, if we fix the pattern (say, starting with Odd), then:
   - Positions 0, 2, 4, ... (odd indices in 0-based indexing for the pattern "Odd, Even, Odd...") will take odd numbers.
   - Positions 1, 3, 5, ... will take even numbers.
   
   The number of such permutations is simply $O! \times E!$ if the pattern is valid (i.e., the count of odd positions equals $O$ and even positions equals $E$). 
   
   However, we need to find the $k$-th lexicographical permutation. We can construct the permutation digit by digit.
   
   At each step (position $i$ from 0 to $n-1$):
   - Determine the required parity for position $i$ based on the chosen pattern.
   - Iterate through the available numbers of the correct parity in increasing order.
   - For each candidate number, calculate how many valid completions exist if we pick that number.
   - Subtract that count from $k$. If $k$ becomes less than or equal to 0, we pick that number and proceed to the next position with the remaining numbers.
   
   The number of completions for the remaining positions, given that we have $rem\_odd$ odd numbers and $rem\_even$ even numbers left to place, is simply $rem\_odd! \times rem\_even!$. This is because once the parity pattern is fixed, the choices for odd positions and even positions are independent.
   
   Algorithm:
   1. Determine the possible patterns.
      - If $n$ is odd, only Pattern B (starts with Odd) is valid.
      - If $n$ is even, both Pattern A (starts with Even) and Pattern B (starts with Odd) are valid.
   2. Calculate the total number of alternating permutations for each valid pattern.
      - For a fixed pattern, count = $O! \times E!$.
   3. If $n$ is even, check if $k$ falls within the range of Pattern A permutations. If so, use Pattern A. Otherwise, subtract count of Pattern A from $k$ and use Pattern B.
      - Note: Pattern A permutations are lexicographically smaller than Pattern B permutations? Not necessarily. We need to be careful. Actually, the lexicographical order mixes permutations from both patterns. We cannot simply separate them by pattern and then pick.
      
   Correction: The lexicographical order is global. We cannot just decide the pattern first. We must build the permutation digit by digit, and at each step, consider candidates from both parities if they are allowed by the alternating constraint.
   
   Revised Approach:
   We build the permutation from left to right.
   State: `used` array (or set) to track used numbers.
   At position $i$:
   - The parity of the number at position $i$ is determined by the parity of the number at position $i-1$ (if $i>0$). Specifically, it must be different.
   - For $i=0$, we can try both even and odd numbers? No, we must try all available numbers in increasing order that satisfy the alternating constraint with the previous element. For $i=0$, there is no previous element, so we try all available numbers? But the constraint is only on adjacent elements. So for $i=0$, any number can be chosen? 
   
   Actually, the definition is "no two adjacent elements are both odd or both even". This means $perm[i]$ and $perm[i+1]$ must have different parity.
   
   So, at each position $i$, the parity of $perm[i]$ is constrained by $perm[i-1]$. 
   - If $i=0$, no constraint from previous. But the choice at $i=0$ determines the parity for $i=1$.
   
   We can iterate through candidate numbers for position $i$ in increasing order. For each candidate, we check if it has the correct parity (different from $perm[i-1]$ if $i>0$). 
   Then, we calculate the number of valid completions for the remaining positions given the current choice.
   
   How to calculate the number of valid completions?
   Let $rem\_odd$ be the count of unused odd numbers, $rem\_even$ be the count of unused even numbers.
   Let $len\_rem = n - 1 - i$ be the number of positions left to fill.
   The next position $i+1$ must have parity different from $perm[i]$.
   Let $p$ be the parity of $perm[i]$. Then position $i+1$ must have parity $1-p$.
   The sequence of parities for the remaining positions is fixed once $perm[i]$ is chosen.
   Let $req\_odd$ be the number of odd numbers needed in the remaining positions.
   Let $req\_even$ be the number of even numbers needed in the remaining positions.
   
   If $req\_odd > rem\_odd$ or $req\_even > rem\_even$, then 0 completions.
   Otherwise, the number of completions is $req\_odd! \times req\_even!$? 
   
   No, this is only true if the positions for odd and even numbers are fixed and independent. They are. Once the parity of each remaining position is fixed, we just need to assign the remaining odd numbers to the odd positions and even numbers to the even positions. The number of ways is indeed $rem\_odd! \times rem\_even!$ only if the number of odd positions remaining equals $rem\_odd$ and even positions remaining equals $rem\_even$. 
   
   Actually, yes. If the parity pattern for the rest of the positions is fixed, then we must use exactly the number of odd/even numbers that match the count of odd/even positions remaining. If the counts don't match, it's 0. If they do match, the number of ways is $rem\_odd! \times rem\_even!$.
   
   So, the algorithm:
   1. Precompute factorials up to $n$.
   2. Initialize `used` array, `result` list.
   3. For each position $i$ from 0 to $n-1$:
      - Determine the required parity for position $i$:
        - If $i==0$, we don't have a previous parity constraint. But we will try candidates in increasing order. The candidate's parity will determine the next required parity.
        - If $i>0$, the parity must be different from `result[-1]`.
      - Get the list of available numbers with the correct parity (if $i>0$), or all available numbers (if $i==0$). Sort them.
      - For each candidate $c$ in sorted order:
        - If $i>0$ and parity($c$) == parity($result[-1]$), skip.
        - Temporarily choose $c$.
        - Calculate the number of valid completions for the remaining $n-1-i$ positions.
          - Let $rem\_odd$ = count of unused odd numbers (excluding $c$ if $c$ is odd).
          - Let $rem\_even$ = count of unused even numbers (excluding $c$ if $c$ is even).
          - Determine the parity sequence for the remaining positions. The first remaining position is $i+1$. Its parity must be different from $c$.
          - Count how many odd and even positions are in the remaining slots.
            - Let $pos$ start from $i+1$ to $n-1$.
            - $req\_odd = 0, req\_even = 0$.
            - For $j$ from $i+1$ to $n-1$:
              - If $j == i+1$, parity must be different from $c$.
              - Else, parity must be different from the parity of the number at $j-1$.
            - Actually, the parity sequence is fixed: it alternates.
            - So, if $c$ is even, then $i+1$ must be odd, $i+2$ even, etc.
            - Count $req\_odd$ and $req\_even$ based on this fixed sequence.
          - If $req\_odd == rem\_odd$ and $req\_even == rem\_even$, then count = $fact[rem\_odd] \times fact[rem\_even]$.
          - Else, count = 0.
        - If $k \le count$:
          - Append $c$ to result.
          - Mark $c$ as used.
          - Break inner loop (proceed to next position).
        - Else:
          - $k -= count$.
      - If no candidate was chosen, return [] (should not happen if $k$ is valid).
   4. Return result.

   Pitfalls:
   - $n$ up to 100, so factorials can be huge. But $k \le 10^{15}$, so we can cap the factorial values at $10^{15} + 7$ to avoid big integer overhead, though Python handles big ints well.
   - Correctly counting $req\_odd$ and $req\_even$ for the remaining positions.
   - Handling $i=0$ correctly: try all available numbers in increasing order.

   Complexity: $O(n^2)$ because for each of $n$ positions, we iterate through at most $n$ candidates, and for each candidate, we do $O(n)$ work to count required odds/evens (or $O(1)$ if we precompute or update incrementally).

## worker: Implement the solution with the digit-by-digit con
The solution uses a digit-by-digit construction approach. For each position in the permutation, it iterates through candidate numbers in increasing order. For each candidate, it calculates the number of valid alternating permutations that can be formed with the remaining numbers. This count is computed by checking if the remaining counts of odd and even numbers match the required counts for the fixed parity pattern of the remaining positions. If they match, the number of ways is the product of the factorials of the remaining odd and even counts. If $k$ is less than or equal to this count, the candidate is chosen; otherwise, $k$ is reduced by the count and the next candidate is considered. This approach runs in $O(n^2)$ time, which is efficient for $n \le 100$.
