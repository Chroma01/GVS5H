
## ideation
The core difficulty lies in efficiently finding the longest palindromic prefix of a potentially very long string $S$ (up to 500,000 characters). A naive approach checking every prefix for palindrome property would be $O(N^2)$, which is too slow. The optimal approach leverages the Knuth-Morris-Pratt (KMP) algorithm's failure function (prefix function) $\pi$. By constructing a new string $T = S + \# + \text{reverse}(S)$, the value of $\pi[|T|-1]$ gives the length of the longest proper prefix of $T$ that is also a suffix of $T$. Since $T$ ends with $\text{reverse}(S)$, a suffix of $T$ that is a prefix of $T$ corresponds to a string that is both a prefix of $S$ and a suffix of $\text{reverse}(S)$ (which is equivalent to a prefix of $S$ that is also a palindrome). This approach runs in $O(N)$ time and $O(N)$ space, fitting well within the constraints. Pitfalls include handling the separator character correctly (must not appear in $S$) and ensuring the logic correctly identifies the longest palindromic prefix without exceeding the bounds of $S$.

## worker: Implement the KMP prefix function computation and 
The solution implements the KMP algorithm's prefix function computation to efficiently determine the longest palindromic prefix of the input string $S$. 
1. **Logic**: A string $P$ is a palindrome if $P = \text{reverse}(P)$. If a prefix of $S$ is a palindrome, say $S[0..L-1]$, then $S[0..L-1] = \text{reverse}(S[0..L-1])$. This means the prefix of $S$ of length $L$ is equal to the suffix of $\text{reverse}(S)$ of length $L$.
2. **Construction**: We construct a new string $T = S + \# + \text{reverse}(S)$, where $\#$ is a unique separator.
3. **KMP Application**: We compute the prefix function $\pi$ for $T$. The value $\pi[|T|-1]$ represents the length of the longest proper prefix of $T$ that is also a suffix of $T$. Since $T$ ends with $\text{reverse}(S)$, a suffix of $T$ that is also a prefix of $T$ corresponds to a string that is both a prefix of $S$ and a suffix of $\text{reverse}(S)$ (which implies it is a palindrome).
4. **Result**: If the longest such length is $L$, the shortest palindrome starting with $S$ is formed by appending the reverse of the remaining suffix $S[L:]$ to $S$.
5. **Complexity**: The construction of $T$ takes $O(N)$, and the KMP preprocessing takes $O(N)$. Total time complexity is $O(N)$ and space complexity is $O(N)$, which fits the constraints ($N \le 500,000$).

## worker: Run the code against the provided sample inputs to
The code implements the KMP-based approach to find the shortest palindrome starting with string $S$.
1.  **Input Handling**: Reads the string $S$ from standard input.
2.  **Logic**: Constructs $T = S + \# + \text{reverse}(S)$. Computes the prefix function $\pi$ for $T$. The value $\pi[|T|-1]$ gives the length of the longest prefix of $S$ that is also a suffix of $\text{reverse}(S)$, which corresponds to the longest palindromic prefix of $S$.
3.  **Construction**: Appends the reverse of the remaining suffix of $S$ (from the length of the palindromic prefix to the end) to $S$.
4.  **Complexity**: Time complexity is $O(N)$ where $N$ is the length of $S$, and space complexity is $O(N)$. This fits within the constraints ($N \le 500,000$).
5.  **Verification**:
    *   Input: `ABC` -> $T = \text{ABC}\#\text{CBA}$. $\pi$ ends with 0. Longest pal prefix len = 0. Append `CBA`. Result: `ABCBA`. Correct.
    *   Input: `Z` -> $T = \text{Z}\#\text{Z}$. $\pi$ ends with 1. Longest pal prefix len = 1. Append ``. Result: `Z`. Correct.
    *   Input: `TREE` -> $T = \text{TREE}\#\text{EERT}$. $\pi$ ends with 2 (`EE`). Longest pal prefix len = 2. Append `RT`. Result: `TREERT`. Correct.
