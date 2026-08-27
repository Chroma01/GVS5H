1. **Check Feasibility**: First, verify if a valid mapping is possible. For each position `i`, if `S[i] != T[i]`, we must map `S[i]` to `T[i]`. This implies a functional mapping from characters in S to characters in T.
   - If two different characters in S map to the same character in T (e.g., `S[i]='a', T[i]='b'` and `S[j]='c', T[j]='b'`), it's impossible because 'a' and 'c' would both become 'b', losing their distinction. So, the mapping from S-char to T-char must be injective (one-to-one) for distinct S-chars.
   - Also, if `S[i] == T[i]`, no mapping is needed for that position, but if `S[i] != T[i]`, we record `map[S[i]] = T[i]`.
   - Additionally, if a character in T is the target of a mapping, it cannot be a source of a mapping unless it's part of a cycle that can be resolved. Specifically, if we have a cycle in the mapping graph (e.g., 'a'->'b', 'b'->'a'), we need an extra temporary character to break the cycle.

2. **Build Mapping**: Create a dictionary `mapping` where `mapping[s_char] = t_char` for all `s_char` in S that need to change. If we encounter a conflict (a character in S already mapped to a different character in T, or two different characters in S mapping to the same character in T), return -1.

3. **Count Operations**: The number of operations is the number of edges in the mapping graph. However, if there is a cycle in the mapping, we need one extra operation to break the cycle (using a temporary character not involved in the mapping). 
   - Build a directed graph where nodes are characters 'a'-'z' and edges are `s_char -> t_char`.
   - Count the number of edges. If there is a cycle, add 1 to the count.
   - Note: A cycle exists if following the mapping from a node leads back to itself. Since the mapping is a function, each node has out-degree at most 1. We can detect cycles by traversing.

4. **Edge Case**: If S and T are already identical, output 0.