
## ideation
The problem: find the shortest palindrome having S as a prefix. Key insight: if the longest palindromic prefix of S has length k, then the answer is S + reverse(S[k:]). This is optimal because any palindrome with S as prefix must have its first k characters mirrored; the longest palindromic prefix minimizes the appended part.

Core difficulty: computing the longest palindromic prefix efficiently for |S| up to 500,000 — needs O(n) time and reasonable memory in Python.

Candidate approach: Build T = S + '#' + reverse(S) and compute the KMP prefix function (failure function) over T. The final value pi[-1] equals the longest prefix of S that is also a suffix of reverse(S), which is exactly the longest palindromic prefix of S. The '#' separator prevents matches longer than n.

Pitfalls:
- Must include a separator character not in the alphabet (uppercase letters only, so '#' works) to avoid overlap giving k > n.
- Python speed: use a list of ints for pi, local variable references, avoid slicing overhead in loops; reading input via sys.stdin.
- Memory: T has length 2n+1 (~1e6+1 chars), pi list of same length — fine.
- Edge cases: n=1 (answer is S itself); S already a palindrome (k=n, append nothing).
- Output could be up to ~2n characters (~1e6), use sys.stdout.write.

## worker: Implement solve() in Python: read S from stdin, co
- The shortest palindrome with S as a prefix is S + reverse(S[k:]), where k is the length of the longest palindromic prefix of S. Any palindrome having S as a prefix must mirror the non-palindromic tail, so maximizing the palindromic prefix minimizes the appended characters.
- To find k, compute the KMP prefix function over T = S + '#' + reverse(S). pi[-1] is the longest prefix of S that is also a suffix of reverse(S), i.e., the longest palindromic prefix. The '#' separator (not in the uppercase alphabet) guarantees k ≤ n.
- Complexity: O(n) time, O(n) memory with an integer list; n ≤ 5·10^5 so T has ~10^6+1 characters — fine in Python.
- Sample checks:
  - S=ABC: T=ABC#CBA, pi[-1]=1 (prefix "A" = suffix "A" of "CBA") → answer ABC + "BC"[::-1] = ABCBA. ✓
  - S=Z: T=Z#Z, pi[-1]=1 → answer Z. ✓
  - S=TREE: T=TREE#EERT, pi[-1]=1 ("T") → answer TREE + "REE"[::-1] = TREERT. ✓
- Edge cases: n=1 → k=1, output S. S already a palindrome (e.g., "ABA") → k=n, output S unchanged.
