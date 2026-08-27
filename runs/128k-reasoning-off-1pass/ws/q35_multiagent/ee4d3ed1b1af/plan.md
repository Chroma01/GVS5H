1. Split the pattern `p` into three parts: prefix, middle, and suffix, separated by the two `*` characters.
2. If the prefix is empty and the suffix is empty (i.e., `p` is `**`), the shortest match is the empty string, so return 0.
3. Find all occurrences of the prefix in `s` and all occurrences of the suffix in `s`.
4. For each valid pair of prefix end index and suffix start index (where prefix ends before suffix starts), check if the middle part (between the two `*`) can be found in the substring between them.
5. To optimize, iterate through possible prefix positions and for each, find the earliest suffix position that allows the middle part to fit, then verify if the middle part exists in the gap. Use KMP or built-in string search for efficiency.
6. Track the minimum length of such valid substrings. If no valid substring is found, return -1.