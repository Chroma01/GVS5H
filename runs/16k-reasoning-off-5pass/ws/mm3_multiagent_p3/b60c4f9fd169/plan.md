The problem asks whether we can transform string S into T using at most K edit operations (insert, delete, replace), with K ≤ 20 but |S|, |T| ≤ 500,000.

Standard edit distance (Levenshtein) can be computed in O(|S|·|T|) which is too slow. However, with K ≤ 20, we only care about positions where S and T align with at most K differences. The classic technique is to align S and T using an offset: the optimal alignment in the edit distance algorithm has |i - j| ≤ K. We can iterate over all offsets d where -K ≤ d ≤ K, where we compare S[i] with T[i+d], and count the number of mismatches along the diagonal.

More precisely, for each offset d = j - i (where j is index in T, i in S), we need i ≥ 0 and j = i + d ≥ 0, so i ranges from max(0, -d) to min(|S|-1, |T|-1-d). Along this diagonal, we compare S[i] with T[i+d]; the number of mismatches is the number of replacements needed if we align along this offset. The total edit distance for that offset is (|S| - L) + (|T| - L) + mismatches, where L is the length of the diagonal (number of positions compared). This equals |S| + |T| - 2*L + mismatches.

We compute the edit distance for each valid offset in O(|S| + |T|) total (each character is compared at most once per offset, but since K ≤ 20, there are at most 2K+1 ≤ 41 offsets, giving O(K·(N+M)) which is fine for N, M up to 500,000).

If the minimum edit distance ≤ K, output "Yes", else "No".