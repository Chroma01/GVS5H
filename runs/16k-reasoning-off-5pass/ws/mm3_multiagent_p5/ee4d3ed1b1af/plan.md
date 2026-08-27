Split pattern p into three parts: prefix P1 (before first '*'), middle P2 (between the two '*'), and suffix P3 (after second '*'). A substring s[l..r] matches p iff:
1. it starts with P1 (or P1 empty),
2. it ends with P3 (or P3 empty),
3. inside it there is an occurrence of P2 (or P2 empty).

Goal: minimize length = r-l+1. Approach: precompute all starting positions where P1 matches, and all ending positions where P3 matches. For each occurrence of P2 (found via KMP in linear time), find the smallest P1-match that starts ≤ its start, and the smallest P3-match that ends ≥ its end. The answer is min over all P2 occurrences of (P3.end - P1.start + 1). Use KMP for O(n+m) substring search. Handle empty parts as special cases (any position allowed).