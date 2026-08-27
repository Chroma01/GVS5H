1. Read the input string $S$ and determine its length $N$.
2. Construct a new string $T$ by concatenating the reverse of $S$, a unique separator (e.g., `#`), and $S$ itself. This allows us to use the KMP algorithm to find the longest prefix of $S^R$ that matches a suffix of $S$.
3. Compute the KMP prefix function (pi array) for $T$. The last value in this array gives the length $L$ of the longest palindromic suffix of $S$.
4. The shortest palindrome is formed by appending the reverse of the non-palindromic prefix $S[0 \dots N-L-1]$ to $S$.
5. Print the resulting string. The overall time and space complexity will be $O(N)$, which fits well within the constraints.