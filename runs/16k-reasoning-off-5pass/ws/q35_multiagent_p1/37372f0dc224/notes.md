
## ideation
The problem asks for the shortest palindrome that has a given string $S$ as its prefix. This is equivalent to finding the shortest string $P$ such that $P$ is a palindrome and $S$ is a prefix of $P$. This means $P = S + \text{suffix}$, where $\text{suffix}$ is the reverse of some prefix of $S$. To minimize the length of $P$, we need to minimize the length of the added suffix. This is achieved by finding the longest palindromic suffix of $S$. If the longest palindromic suffix of $S$ has length $L$, then the first $n-L$ characters of $S$ (where $n$ is the length of $S$) are not part of this palindrome and must be reversed and appended to $S$ to complete the palindrome.

The core difficulty is efficiently finding the longest palindromic suffix of $S$. A naive check for each suffix would be $O(n^2)$, which is too slow for $n=500,000$. The plan suggests using the KMP algorithm's prefix function on the string $T = S + \# + \text{reverse}(S)$.

Let's verify this approach:
1. Construct $T = S + \# + S^R$, where $S^R$ is the reverse of $S$. The '#' is a separator not present in $S$ to prevent matching across the boundary in a way that doesn't correspond to a suffix of $S$ matching a prefix of $S^R$.
2. Compute the prefix function (pi array) for $T$. The prefix function $\pi[i]$ is the length of the longest proper prefix of $T[0 \dots i]$ that is also a suffix of $T[0 \dots i]$.
3. The last value in the prefix function array, $\pi[|T|-1]$, gives the length of the longest prefix of $T$ that is also a suffix of $T$.
4. Since $T$ ends with $S^R$, a suffix of $T$ corresponds to a prefix of $S^R$. A prefix of $T$ corresponds to a prefix of $S$ (because of the separator '#', the match cannot extend into the $S^R$ part as a prefix of $T$ unless it's entirely within the $S$ part or crosses the separator, but the separator prevents invalid matches). Specifically, the longest prefix of $T$ that is a suffix of $T$ is the longest string that is both a prefix of $S$ and a suffix of $S^R$.
5. A string that is a prefix of $S$ and a suffix of $S^R$ is equivalent to a suffix of $S$ that is a palindrome. Why? Let the string be $W$. $W$ is a prefix of $S$ and $W$ is a suffix of $S^R$. Since $S^R$ is the reverse of $S$, a suffix of $S^R$ is the reverse of a prefix of $S$. So $W = (\text{prefix of } S)^R$. But $W$ is also a prefix of $S$. Thus, $W$ is a prefix of $S$ and $W = (\text{some prefix of } S)^R$. This implies $W^R$ is a prefix of $S$. Wait, let's rephrase.
   Let $W$ be the string found. $W$ is a prefix of $S$. $W$ is a suffix of $S^R$.
   Let $S = w_1 w_2 \dots w_n$. $S^R = w_n w_{n-1} \dots w_1$.
   A suffix of $S^R$ of length $k$ is $w_k w_{k-1} \dots w_1$? No, suffix of $S^R$ of length $k$ is the last $k$ chars of $S^R$, which are $w_k \dots w_1$ reversed? No.
   $S^R = w_n w_{n-1} \dots w_1$.
   Suffix of length $k$ of $S^R$ is $w_k w_{k-1} \dots w_1$? No, it's $w_k \dots w_1$ if we index from 1?
   Let's use 0-indexing. $S = s_0 s_1 \dots s_{n-1}$. $S^R = s_{n-1} s_{n-2} \dots s_0$.
   Suffix of $S^R$ of length $k$ is $s_{k-1} s_{k-2} \dots s_0$.
   This string is the reverse of the prefix $s_0 \dots s_{k-1}$ of $S$.
   So, if $W$ is a suffix of $S^R$ of length $k$, then $W = (s_0 \dots s_{k-1})^R$.
   The condition is that $W$ is also a prefix of $S$. So $(s_0 \dots s_{k-1})^R = s_0 \dots s_{k-1}$.
   This means the prefix $s_0 \dots s_{k-1}$ is a palindrome.
   Wait, this finds the longest palindromic *prefix* of $S$, not suffix.
   
   Let's re-read the standard trick.
   To find the longest palindromic *suffix* of $S$:
   We want the longest suffix of $S$ that is a palindrome.
   Let the suffix be $S[i \dots n-1]$. It is a palindrome if $S[i \dots n-1] = (S[i \dots n-1])^R$.
   $(S[i \dots n-1])^R$ is a prefix of $S^R$.
   So we want the longest suffix of $S$ that matches a prefix of $S^R$.
   This is exactly what the KMP approach on $S + \# + S^R$ finds?
   Let's check.
   $T = S + \# + S^R$.
   $\pi[|T|-1]$ is the length of the longest prefix of $T$ that is a suffix of $T$.
   Prefix of $T$ is a prefix of $S$ (due to separator).
   Suffix of $T$ is a suffix of $S^R$.
   So it finds the longest string $W$ such that $W$ is a prefix of $S$ and $W$ is a suffix of $S^R$.
   As derived above, $W$ being a suffix of $S^R$ means $W = (\text{prefix of } S)^R$.
   And $W$ being a prefix of $S$ means $W = \text{prefix of } S$.
   So $(\text{prefix of } S)^R = \text{prefix of } S$.
   This finds the longest palindromic *prefix* of $S$.
   
   This is the opposite of what we want. We want the longest palindromic *suffix*.
   
   To find the longest palindromic *suffix* of $S$:
   We want the longest suffix of $S$ that is a palindrome.
   Let this suffix be $V$. $V$ is a suffix of $S$. $V$ is a palindrome, so $V = V^R$.
   $V^R$ is a prefix of $S^R$.
   So $V$ is a suffix of $S$ and $V$ is a prefix of $S^R$.
   This means we want the longest string $V$ that is a suffix of $S$ and a prefix of $S^R$.
   
   Consider the string $U = S^R + \# + S$.
   Compute the prefix function for $U$.
   The last value $\pi[|U|-1]$ is the length of the longest prefix of $U$ that is a suffix of $U$.
   Prefix of $U$ is a prefix of $S^R$.
   Suffix of $U$ is a suffix of $S$.
   So it finds the longest string $V$ that is a prefix of $S^R$ and a suffix of $S$.
   Since $V$ is a prefix of $S^R$, $V^R$ is a suffix of $S$.
   Since $V$ is a suffix of $S$, $V$ is a suffix of $S$.
   So $V$ is a suffix of $S$ and $V$ is a prefix of $S^R$.
   Does this imply $V$ is a palindrome?
   $V$ is a prefix of $S^R \implies V = (s_{n-k} \dots s_{n-1})^R$? No.
   $S^R = s_{n-1} s_{n-2} \dots s_0$.
   Prefix of length $k$ of $S^R$ is $s_{n-1} s_{n-2} \dots s_{n-k}$.
   Suffix of length $k$ of $S$ is $s_{n-k} \dots s_{n-1}$.
   So if $V$ is both, then $s_{n-1} \dots s_{n-k} = s_{n-k} \dots s_{n-1}$.
   This means the substring $s_{n-k} \dots s_{n-1}$ is a palindrome.
   Yes! This is the longest palindromic suffix of $S$.
   
   So the correct construction is $T = S^R + \# + S$.
   Then the length of the longest palindromic suffix is $\pi[|T|-1]$.
   Let this length be $L$.
   The part of $S$ that is not covered by this palindromic suffix is $S[0 : n-L]$.
   We reverse this part and append it to $S$.
   
   Example: S = "ABC"
   $S^R$ = "CBA"
   $T$ = "CBA#ABC"
   Prefix function for "CBA#ABC":
   C: 0
   CB: 0
   CBA: 0
   CBA#: 0
   CBA#A: 0 (A != C)
   CBA#AB: 0
   CBA#ABC: 0? No.
   Let's trace carefully.
   pi[0] = 0 ('C')
   pi[1] = 0 ('CB')
   pi[2] = 0 ('CBA')
   pi[3] = 0 ('CBA#')
   pi[4] = 0 ('CBA#A') - 'A' != 'C'
   pi[5] = 0 ('CBA#AB') - 'B' != 'C'
   pi[6] = 0 ('CBA#ABC') - 'C' == 'C', so pi[6] = 1?
   Wait. pi[i] is length of longest proper prefix of T[0..i] that is also a suffix of T[0..i].
   T[0..6] = "CBA#ABC"
   Prefixes: C, CB, CBA, CBA#, CBA#A, CBA#AB, CBA#ABC
   Suffixes: C, BC, ABC, #ABC, A#ABC, BA#ABC, CBA#ABC
   Common proper prefix/suffix: "C" is a prefix and a suffix. Length 1.
   So L = 1.
   Longest palindromic suffix of "ABC" is "C" (length 1). Correct.
   Part to reverse: S[0 : 3-1] = S[0:2] = "AB".
   Reverse: "BA".
   Result: "ABC" + "BA" = "ABCBA". Correct.
   
   Example: S = "TREE"
   $S^R$ = "EERT"
   $T$ = "EERT#TREE"
   We want longest palindromic suffix of "TREE".
   Suffixes: "E", "EE", "REE", "TREE".
   Palindromes: "E" (yes), "EE" (yes), "REE" (no), "TREE" (no).
   Longest is "EE", length 2.
   
   Let's check T = "EERT#TREE"
   pi array:
   E: 0
   EE: 1 (E)
   EER: 0
   EERT: 0
   EERT#: 0
   EERT#T: 0
   EERT#TR: 0
   EERT#TRE: 0
   EERT#TREE: 1? 'E' matches 'E'.
   So L = 1? But we expected 2.
   
   Let's re-evaluate.
   Suffix of S is "EE".
   Prefix of $S^R$ is "EE".
   So $V$ = "EE".
   Is "EE" a prefix of $S^R$? $S^R$ = "EERT". Prefix "EE" is "EE". Yes.
   Is "EE" a suffix of S? S = "TREE". Suffix "EE" is "EE". Yes.
   So the match should be length 2.
   
   Let's re-calculate pi for "EERT#TREE".
   i=0: 'E', pi=0
   i=1: 'EE', pi=1 (prefix 'E' == suffix 'E')
   i=2: 'EER', pi=0
   i=3: 'EERT', pi=0
   i=4: 'EERT#', pi=0
   i=5: 'EERT#T', pi=0
   i=6: 'EERT#TR', pi=0
   i=7: 'EERT#TRE', pi=0?
      Prefixes: E, EE, EER, EERT, EERT#, EERT#T, EERT#TR, EERT#TRE
      Suffixes: E, RE, TRE, #TRE, T#TRE, RT#TRE, ERT#TRE, EERT#TRE
      Match: 'E' is prefix and suffix. Length 1.
   i=8: 'EERT#TREE', pi=?
      Prefixes: ..., EERT#TRE, EERT#TREE
      Suffixes: E, EE, TREE, #TREE, T#TREE, RT#TREE, ERT#TREE, EERT#TREE
      Match: 'E' (len 1), 'EE' (len 2).
      Is 'EE' a prefix? Yes, T[0..1] = 'EE'.
      Is 'EE' a suffix? Yes, T[7..8] = 'EE'.
      So pi[8] = 2.
      
   So L = 2.
   Part to reverse: S[0 : 4-2] = S[0:2] = "TR".
   Reverse: "RT".
   Result: "TREE" + "RT" = "TREERT". Correct.

   So the plan is:
   1. Read S.
   2. Construct T = reverse(S) + '#' + S.
   3. Compute prefix function for T.
   4. L = pi[-1].
   5. Result = S + reverse(S[0 : n-L]).

## worker: Implement the KMP prefix function calculation.
The problem asks for the shortest palindrome that has $S$ as its prefix. This is equivalent to finding the longest palindromic suffix of $S$. If the longest palindromic suffix has length $L$, then the first $n-L$ characters of $S$ are not part of this palindrome and must be reversed and appended to $S$ to complete the palindrome.

To efficiently find the longest palindromic suffix of $S$, we use the KMP algorithm's prefix function. We construct a string $T = S^R + \# + S$, where $S^R$ is the reverse of $S$ and $\#$ is a separator. The prefix function $\pi[i]$ for $T$ gives the length of the longest proper prefix of $T[0 \dots i]$ that is also a suffix of $T[0 \dots i]$. The value $\pi[|T|-1]$ gives the length of the longest prefix of $T$ that is also a suffix of $T$. Since $T$ starts with $S^R$ and ends with $S$, this corresponds to the longest string that is both a prefix of $S^R$ and a suffix of $S$. A string that is a prefix of $S^R$ and a suffix of $S$ is exactly a palindromic suffix of $S$.

The time complexity is $O(n)$ where $n$ is the length of $S$, due to the linear time construction of the prefix function. The space complexity is also $O(n)$.
