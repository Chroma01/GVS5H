
## ideation
The core difficulty lies in efficiently calculating the minimum operations for a fixed target frequency $k$. The operations allow changing a character to the next letter, which creates a dependency chain from 'a' to 'z'. Specifically, excess counts of a character can be "pushed" to the next character via change operations (cost 1 per character, same as deletion), or deleted. Deficient counts must be filled via insertion (cost 1 per character).

The key insight is that for a fixed target frequency $k$, we can process characters from 'a' to 'z' greedily:
1. Maintain a running count of "pushed" characters from the previous letter.
2. For each character $c$ (from 'a' to 'z'):
   - Let `current_count` be the initial count of $c$ plus any pushed from $c-1$.
   - If `current_count` > $k$: We must reduce the count to $k$. The excess `current_count - k` can be changed to $c+1$ (pushed) or deleted. Since changing costs 1 and deleting costs 1, and changing might help the next character, we push the excess to the next character. The cost is `current_count - k`.
   - If `current_count` <= $k$: We need to reach $k$. We insert `k - current_count` characters. Cost is `k - current_count`. No excess to push.
   - Note: If we are at 'z' and have excess, we cannot push further, so we must delete the excess. The cost calculation `current_count - k` still holds as deletions.
3. Sum the costs for all characters.
4. Iterate $k$ from 1 to $n$ (length of $s$) and take the minimum cost. Also consider $k=0$ (delete all, cost $n$).

Complexity: $O(26 \cdot n)$, which is acceptable given $n \le 2 \cdot 10^4$.

Pitfalls:
- Forgetting that 'z' cannot push to anything, so excess at 'z' is deleted. The logic `max(0, current_count - k)` handles this correctly as deletions.
- The "push" only happens if `current_count > k`. If `current_count <= k`, we insert, so no push.
- Initial counts should be computed once.

## worker: Implement the solution by first counting character
The solution iterates over all possible target frequencies $k$ from 1 to $n$ (the length of the string). For each $k$, it calculates the minimum operations required to make all characters in the string appear exactly $k$ times. 

The calculation for a fixed $k$ is done greedily from 'a' to 'z':
1. Maintain a `pushed` variable that tracks the number of characters moved from the previous character to the current one via "change to next letter" operations.
2. For each character, compute `current_count = initial_count + pushed`.
3. If `current_count > k`, the excess `current_count - k` characters must be operated on. Each such operation (either changing to next letter or deleting) costs 1. The excess is pushed to the next character.
4. If `current_count <= k`, we need to insert `k - current_count` characters to reach the target frequency. This costs `k - current_count`. No characters are pushed to the next character.
5. Sum the costs for all 26 characters.
6. The minimum cost across all $k$ values is the answer. We also initialize `min_ops` to $n$ (the cost of deleting all characters, corresponding to an empty string which is trivially "good").

Complexity: $O(26 \cdot n)$, which is efficient for $n \le 2 \cdot 10^4$.
