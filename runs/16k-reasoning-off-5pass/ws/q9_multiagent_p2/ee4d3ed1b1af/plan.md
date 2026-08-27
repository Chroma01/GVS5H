1. Split the pattern `p` by the two `'*'` characters to extract the three fixed segments: `prefix`, `middle`, and `suffix`.
2. Use a sliding window approach on string `s` to find the shortest substring that starts with `prefix` and ends with `suffix`, ensuring the distance between them allows for the `middle` segment to be skipped (since `*` matches anything).
3. Iterate through all possible start positions of `prefix` in `s`. For each valid start, find the earliest occurrence of `suffix` that appears after the `prefix` ends.
4. Calculate the length of the substring from the start of `prefix` to the end of `suffix` and track the minimum length found.
5. If no valid combination is found, return -1; otherwise, return the minimum length.