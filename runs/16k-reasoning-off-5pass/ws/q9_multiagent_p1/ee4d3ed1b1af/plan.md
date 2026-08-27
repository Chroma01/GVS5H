1. Split the pattern `p` into three parts based on the two `'*'` characters: `prefix`, `middle`, and `suffix`.
2. Use two pointers (or a sliding window approach) on string `s` to find the shortest substring that starts with `prefix` and ends with `suffix`, ensuring the part between them contains `middle`.
3. Iterate through all possible starting positions of `prefix` in `s`. For each valid start, find the earliest ending position of `suffix` such that `middle` appears in between (or the gap is empty if `middle` is empty).
4. Track the minimum length found; if no valid match exists, return -1.