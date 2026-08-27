
## ideation
The core difficulty is enforcing that every final character run has length at least 3 while minimizing the sum of per-position conversion costs, then resolving ties by the lexicographically smallest reconstructed string. Since changing a character repeatedly has minimum cost equal to the alphabetic distance, the target cost at position i for letter c is abs(caption[i] - c). A target is impossible when n < 3.

The state must distinguish whether the current run has length 1, length 2, or at least 3. A run may continue with the same letter from any of these states, but it may switch to a different letter only after reaching length at least 3. Efficiently handling transitions between all 26 letters and reconstructing the lexicographically smallest optimum are the main implementation concerns.

Tie-breaking cannot be handled safely by choosing a locally smallest letter without considering future feasibility and cost. It should be incorporated through predecessor comparisons, suffix-optimal DP, or a carefully ordered reconstruction.

## worker: Develop and implement a suffix dynamic program ove
The DP tracks the current run length category: exactly 1, exactly 2, or at least 3. A run may change characters only from the third category.

For completed runs, switching to another character is optimized using the smallest and second-smallest transition values, giving `O(26n)` time. The DP uses `O(26n)` memory.

After computing optimal suffix costs, reconstruction greedily selects the smallest character that preserves the optimal total cost, ensuring lexicographic minimality among all minimum-cost captions.

## worker: Fix the suffix-DP boundary bug by computing states
The suffix DP tracks whether the current run has length 1, 2, or at least 3. Runs shorter than 3 are forced to continue, while completed runs may either continue or switch characters.

The DP is computed through position `n - 1`, which is essential for correctly handling the final character. Switching transitions are optimized using the smallest and second-smallest values among all candidate next characters, giving `O(26n)` time and `O(26n)` memory.

After calculating the minimum cost, reconstruction greedily chooses the smallest character that preserves the optimal suffix cost, guaranteeing lexicographic minimality among all minimum-cost captions.

## worker: Run the implementation against all three examples 
The implementation passes the provided examples:

- `"cdcd"` → `"cccc"`
- `"aca"` → `"aaa"`
- `"bc"` → `""`

Additional edge cases also behave correctly, including:

- `"aaa"` → `"aaa"`
- `"aza"` → `"aaa"`
- `"aabbb"` → `"bbbbb"`

The suffix DP correctly distinguishes runs of lengths 1, 2, and at least 3. Reconstruction checks characters in increasing alphabetic order and only accepts transitions preserving the optimal DP cost, so the resulting answer is lexicographically smallest among all minimum-cost answers.

Time complexity is `O(26n)` and memory complexity is `O(26n)`.
