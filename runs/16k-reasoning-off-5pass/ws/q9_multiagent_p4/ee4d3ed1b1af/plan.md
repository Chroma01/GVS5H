1. Split the pattern `p` into three parts using the two `*` characters: `prefix`, `middle`, and `suffix`.
2. Use two pointers (or a sliding window approach) on string `s` to find the shortest substring that starts with `prefix` and ends with `suffix`, ensuring the characters between them can form the `middle` part (which is flexible since `*` matches anything, but here the middle part of the pattern is actually fixed characters between the two stars? Wait, re-reading: `p` has exactly two `*`. So `p` looks like `A*B*C` where A, B, C are non-empty or empty strings of characters. The `*` matches any sequence. So we need to find a substring in `s` that matches `A` + (anything) + `B` + (anything) + `C`. Actually, the pattern is `A` + `*` + `B` + `*` + `C`. The `*` matches any sequence. So the structure is: find `A` in `s`, then find `B` later in `s`, then find `C` after `B`. The shortest such substring is the distance from the start of `A` to the end of `C`.
3. Wait, the pattern is `p` with exactly two `*`. Let's denote `p` as `part1 + '*' + part2 + '*' + part3`.
   We need to find indices `i, j, k` in `s` such that `s[i:i+len(part1)] == part1`, `s[j:j+len(part2)] == part2`, and `k` is the end of `part3` starting after `j`.
   Actually, the `*` matches *any* sequence. So between `part1` and `part2`, there can be any characters (including zero). Between `part2` and `part3`, there can be any characters.
   So we need to find the first occurrence of `part1`, then the first occurrence of `part2` after that, then the first occurrence of `part3` after that? No, we want the *shortest* substring.
   So for every occurrence of `part1` in `s` (say at index `i`), we want to find the earliest occurrence of `part2` at index `j > i`, and then the earliest occurrence of `part3` at index `k > j`. The length would be `(end of part3) - i + 1`.
   To minimize this, for a fixed `i` (start of `part1`), we need the smallest `j` (start of `part2`) and smallest `k` (start of `part3`) such that `i < j < k`.
   Actually, `part2` can be empty. If `part2` is empty, `j` can be `i + len(part1)`.
   Algorithm:
   - Precompute all starting indices of `part1`, `part2`, and `part3` in `s`.
   - For each starting index `i` of `part1`:
     - Find the smallest `j` in `indices_part2` such that `j > i`.
     - Find the smallest `k` in `indices_part3` such that `k > j`.
     - If both exist, calculate length = `(i + len(part1) + (k - j) + len(part3)) - i`? No.
       The substring is from `i` to `k + len(part3) - 1`. Length = `k + len(part3) - i`.
   - To efficiently find the smallest `j > i` and `k > j`, we can store the indices in sorted lists and use binary search (bisect_right).