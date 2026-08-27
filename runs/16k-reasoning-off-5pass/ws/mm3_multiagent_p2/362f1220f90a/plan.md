We need to construct the lexicographically smallest string `word` of length `n + m - 1` over lowercase letters such that for each `i` with `str1[i] == 'T'`, the window `word[i..i+m-1]` equals `str2`, and for each `i` with `str1[i] == 'F'`, that window is **not** equal to `str2`.

Key observation: each character of `str2` (and thus each position of `word`) can be forced by multiple `T` constraints that overlap. The set of positions **forced** to specific letters is the intersection of all `T` windows. Any position not forced must be a letter that is as small as possible lexicographically, but we must also ensure no `F` window accidentally equals `str2`.

Algorithm:
1. Initialize `ans` array of size `L = n + m - 1` with `None` (unassigned).
2. For each `i` where `str1[i] == 'T'`, copy `str2` into `ans[i..i+m-1]`. If a position is already assigned to a different letter, there is a conflict → return `""`.
3. For every position still `None`, tentatively try letters from `'a'` to `'z'`. A position is **blocked** for letter `c` if some `F` index `j` has all its other characters already set equal to `str2` except position `k = j + offset` (where `offset` is the index within `str2`), and setting `ans[k] = c` would make the whole window equal `str2`. Such a position must avoid that particular letter; if it must avoid all 26 letters, return `""`.
4. Otherwise, assign the smallest allowed letter to each `None` position.
5. After all assignments, verify no `F` window equals `str2`; if it does, return `""`.
6. Return the constructed string.

Complexity: `O(n * m + 26 * L)` ≈ `O(n*m)`, which fits `n ≤ 10^4, m ≤ 500`.