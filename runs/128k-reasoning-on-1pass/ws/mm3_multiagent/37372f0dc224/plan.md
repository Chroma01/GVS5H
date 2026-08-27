To obtain the shortest palindrome that has `S` as a prefix we only need to append characters to the right of `S`.  
Let `L` be the length of the longest suffix of `S` that is already a palindrome.  
Appending the reverse of the preceding part `S[0:len(S)-L]` yields a palindrome and no shorter extension is possible.  
`L` can be found as the longest string that is simultaneously a suffix of `S` and a prefix of `reverse(S)`.  
This is exactly the longest border between `reverse(S)` and `S`, which can be computed in linear time with the KMP prefix‑function on the string `reverse(S) + '#' + S`.  
The final answer is `S + reverse(S[:n-L])`.