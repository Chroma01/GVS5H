1. To find the shortest palindrome with prefix S, we need to find the longest palindromic suffix of S.
2. If the longest palindromic suffix of S starts at index i, then the prefix S[0:i] needs to be reversed and appended to S to form the shortest palindrome.
3. We can use the KMP algorithm's failure function (prefix function) on the string T = S + '#' + reverse(S) to efficiently find the longest prefix of reverse(S) that matches a suffix of S.
4. The length of this match tells us the length of the longest palindromic suffix of S.
5. Let L be the length of the longest palindromic suffix. Then the part of S that is not part of this palindrome is S[0 : n-L], which we reverse and append to S.