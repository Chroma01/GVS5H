1. Split the pattern `p` into three parts: `prefix`, `middle`, and `suffix` based on the two `*` characters. The `*` characters themselves are removed.
2. If the pattern has no non-star parts (i.e., `p == "**"`), return 0 immediately.
3. Find all occurrences of `prefix` in `s` and all occurrences of `suffix` in `s`.
4. For each occurrence of `prefix` ending at index `i` (so `s[i-len(prefix)+1:i+1] == prefix`), we need to find the earliest occurrence of `suffix` that starts at or after index `i+1`.
5. Between the end of `prefix` and the start of `suffix`, the `middle` part must match a substring of `s`. So, for each valid pair of prefix end and suffix start, check if `middle` appears as a substring in `s[i+1: suffix_start]`.
6. To optimize, precompute all starting positions of `middle` in `s`. Then for each prefix end index, find the smallest suffix start index such that there exists a `middle` occurrence entirely within `(prefix_end, suffix_start)`.
7. Use binary search or two pointers to efficiently find the best candidates and minimize the total substring length.