
## ideation
The problem asks for the longest downward path (ancestor to descendant) in a rooted tree where all node values are unique. We need to return the maximum total edge length, and among paths achieving that length, the minimum number of nodes.

**Core difficulty:**  
We need to efficiently maintain, during a DFS, the current path from some ancestor to the current node such that all values are distinct. When a duplicate value appears, we must “cut” the path to start after the previous occurrence of that value. This is analogous to the longest subarray with unique elements, but on a tree path.

**Candidate approaches:**
1. **Sliding window on the path using a deque/list and a value-to-position map.**  
   - Keep a list `path_nodes` of nodes currently in the valid unique path (from some ancestor down to the current node).  
   - Keep a dict `value_to_pos` mapping each value to its index in `path_nodes`.  
   - Also maintain `path_start` (the index of the first node of the current valid path).  
   - When entering a node `v` with value `x`:  
     - If `x` not in `value_to_pos`: just append `v`.  
     - Else: let `idx = value_to_pos[x]`. The previous occurrence is at `path_nodes[idx]`. We need to truncate the path to start after `idx`, i.e., set `path_start = idx + 1`. We must remove the entries of all nodes from old `path_start` to `idx` from `value_to_pos`. Then append `v` and set `value_to_pos[x] = len(path_nodes)-1`.  
   - The current valid path is from `path_nodes[path_start]` to `v`. Its length is `cum_len[v] - cum_len[parent_of_front]`, where `parent_of_front` is the node at `path_start-1` (or a dummy with cum_len=0, depth=-1 if `path_start==0`). Node count is `depth[v] - depth[parent_of_front]`.  
   - Update global best length and minimum node count.

2. **Using `last_occ` map storing cumulative length and depth of last occurrence.**  
   - Maintain `window_start_len` and `window_start_depth`.  
   - When entering a node, if its value was seen before with `last_len` and `last_depth`, and `last_len >= window_start_len`, move window start to `last_len` and `last_depth`.  
   - This avoids storing the whole path but requires careful handling of the “parent” of the new start (the child of the previous occurrence). The child’s cumulative length is `last_len + edge_len` where `edge_len` is the edge from the previous node to its child on the current path. This edge length is not directly known unless we store parent edge lengths. We can store `parent_edge_len[node]` and compute the child’s cum_len as `last_len + parent_edge_len[child]`, but we need to know which child. This is messy.

3. **DFS with backtracking and a stack of values.**  
   - Use a stack to keep the current path values. When a duplicate appears, pop until the duplicate is removed. This is similar to approach 1 but using a stack and a set. However, we need to compute path lengths efficiently, so we need cumulative lengths.

**Pitfalls:**
- **Backtracking:** When returning from a recursive call, we must restore the path state (list, `path_start`, and `value_to_pos`). This is tricky if we truncate by moving `path_start` and deleting entries. We need to save the old `path_start` and the list of removed nodes to reinsert them on backtrack. Alternatively, we can avoid deletion by using a “lazy” approach: keep `value_to_pos` but when checking, verify that the stored node is still in the current path (by comparing its depth to the depth of the current front). This avoids needing to delete entries on truncation, and on backtrack we just pop the current node and restore `path_start` to its previous value (which we saved). However, we also need to restore `value_to_pos` for the current node (delete it) and possibly for nodes that were truncated? Actually if we use lazy checks, we don’t delete entries on truncation, so on backtrack we only need to delete the current node’s entry. But we also need to restore `path_start` to the value it had before we entered the child. That is easy: save old `path_start` before modifications, and restore it after backtracking.

- **Root handling:** The root has no parent. For a path starting at the root, the length is `cum_len[v]` and node count is `depth[v]+1`. We can handle this by checking `path_start == 0` and using a dummy parent with cum_len=0, depth=-1.

- **Edge lengths up to 1000, n up to 5e4, so O(n) or O(n log n) is fine.**

**Chosen approach:**  
Use approach 1 with lazy deletion in `value_to_pos` to simplify backtracking. Specifically:
- Maintain `path_nodes` (list of node ids in order from the current valid start to the current node).
- Maintain `path_start` (index in `path_nodes` of the first node of the current valid path).
- Maintain `value_to_pos` mapping value to the node id of its last occurrence in the current path (not necessarily the index). Actually we need to know the index to compute truncation. We can map value to the node id, and also keep an array `node_index` that gives the current index of each node in `path_nodes` (or we can compute it by storing the index in the list). But since `path_nodes` is a list, we can store the index alongside. Simpler: map value to the node id, and when we need to truncate, we need to find the index of that node in `path_nodes`. We can find it by storing a parallel list `path_values` or by searching. But searching is O(n) per duplicate, which is too slow. So we need O(1) access to the index. We can store `value_to_index` mapping value to its index in `path_nodes` (absolute index). But then we have the deletion problem on truncation. However, with lazy deletion, we can store `value_to_index` but when we look up, we check if the stored index is still valid (i.e., >= path_start). If not, we treat it as not present. But we also need to update the stored index to the new occurrence. So we can do:
  - `value_to_index` maps value to the index in `path_nodes` of its last occurrence.
  - When entering node `v` with value `x`:
    - If `x` in `value_to_index` and `value_to_index[x] >= path_start`:
        - Let `idx = value_to_index[x]`. The previous occurrence is at `path_nodes[idx]`. We need to truncate: set `path_start = idx + 1`. (We do NOT delete entries for nodes before `path_start`; they become invalid and will be ignored later because their index < path_start.)
    - Append `v` to `path_nodes` (index = len(path_nodes)).
    - Set `value_to_index[x] = len(path_nodes)-1`.
  - When backtracking from `v`:
    - Remove `v` from `path_nodes` (pop).
    - Delete `value_to_index[x]` (or set to -1).
    - Restore `path_start` to its previous value (saved before entering `v`).

This works because:
- When we truncate, we move `path_start` forward. The old entries for values that are now before `path_start` remain in `value_to_index` but with indices < `path_start`. When we later look up a value, we check `if value in value_to_index and value_to_index[value] >= path_start`. If the stored index is < `path_start`, we ignore it (treat as not present). This avoids the need to delete them.
- On backtrack, we restore `path_start` to the old value, so those entries become valid again? Wait: if we restored `path_start` to a smaller value, then the entries that were previously invalid (index < old path_start) might now be >= new path_start? Actually we need to be careful: when we backtrack from a child, we are returning to the parent. The path state should be exactly as it was before we entered the child. That means:
  - The `path_nodes` list should be the same as before (so we pop the child).
  - `path_start` should be the same as before.
  - `value_to_index` should reflect the values in the path before entering the child.
If we used lazy deletion, when we entered the child, we might have moved `path_start` forward (truncated). That truncation removed some nodes from the valid path. When we backtrack, we need to restore `path_start` to its previous value, and also restore `value_to_index` to the state it had before truncation. But we didn't delete the entries for the truncated nodes; they are still there with their old indices. However, after we pop the child, the path is back to the parent. The truncated nodes are no longer in the path (they were removed because of the duplicate). But when we backtrack, we are effectively undoing the entire step of entering the child. That includes undoing the truncation. So we need to restore `path_start` to the value it had before we entered the child. That is easy: we saved `old_path_start`. But we also need to ensure that `value_to_index` for the truncated nodes is not considered. Since we are restoring `path_start` to a smaller value, the truncated nodes' indices might now be >= `path_start`? Let's see: before entering child, `path_start` was some value `S0`. The path_nodes list had length `L0`. The child is appended, making length `L0+1`. During processing of the child, we might have truncated: set `path_start = idx + 1`, where `idx` was the index of the duplicate. `idx` could be >= `S0`. So new `path_start` is `idx+1`, which is > `S0`. The truncated nodes are those with indices from `S0` to `idx`. Their entries in `value_to_index` remain with those indices. When we backtrack, we want to restore `path_start` to `S0`. Then those truncated nodes' indices are >= `S0`? Actually `idx` >= `S0`, so `idx+1 > S0`. The truncated nodes have indices in `[S0, idx]`. After restoring `path_start = S0`, these indices are >= `S0`, so they would be considered valid again! That's wrong because they were removed from the path. So we cannot simply restore `path_start` without also invalidating those entries. We need to actually delete the entries for the truncated nodes on backtrack, or we need to store them and re-delete them.

Thus the lazy deletion approach requires that on backtrack, we also delete the entries for the nodes that were truncated. That means we need to know which nodes were truncated. We can save the list of truncated nodes (or their values) when we truncate, and on backtrack, delete their entries from `value_to_index`. That is doable: when we truncate, we iterate from old `path_start` to `idx` and collect the values (or node ids) to delete later. But we also need to restore `path_start` to the old value. So we can save `old_path_start` and `truncated_values` (a list of values to delete on backtrack). Then on backtrack, we delete those values from `value_to_index` and restore `path_start`. This is O(k) per truncation, where k is the number of nodes removed. Since each node is truncated at most once (when it is removed from the path), total work is O(n). So it's acceptable.

Alternatively, we can avoid the need to restore `value_to_index` by using a different data structure: a stack of values and a set. But we need to compute path lengths, so we need cumulative lengths. We can maintain a stack of nodes (the current path from root to current node). But we need to maintain uniqueness. We can use a set of values in the current path. When we go down, we push the node and its value. If the value is already in the set, we need to pop nodes from the stack until we remove that value. This is similar to the sliding window but using a stack and set. The stack would contain the nodes from the root down to the current node, but with duplicates removed by popping. However, this stack would not necessarily start at the root; it would start at the node after the last occurrence of the duplicate. The length of the path is the sum of edge lengths of the nodes in the stack. We can compute that by maintaining cumulative lengths for each node in the stack. But we need to know the parent of the first node in the stack to compute the sum. The first node in the stack is the child of the previous occurrence. Its parent is the node that was popped (the previous occurrence). So we can compute the sum as `cum_len[current] - cum_len[parent_of_first]`. The parent_of_first is the node that was popped last (the duplicate). So we need to know that node's cum_len. We can get it from the stack before popping? Actually when we pop, we know the node being popped. So we can compute the new path length after popping.

This approach might be simpler: we maintain a stack `path_stack` of nodes representing the current valid unique path from some ancestor to the current node. We also maintain a set `path_values` of the values in the stack. When we go to a child `v`:
- Push `v` onto `path_stack`.
- If `nums[v]` is in `path_values`:
    - We need to pop nodes from `path_stack` until we remove the previous occurrence of `nums[v]`. Let `prev_node` be the node in the stack with that value. We pop nodes from the stack until we pop `prev_node` (inclusive). After popping, the new top of the stack (if any) is the child of `prev_node`? Actually after popping `prev_node`, the next node in the stack is the child of `prev_node` along the path to `v`? Let's see: The stack before pushing `v` contains the unique path from some ancestor to the parent of `v`. When we push `v`, if its value is already in the stack, that means there is some node `prev_node` in the stack with the same value. Since the stack is a simple path from an ancestor down to the parent, `prev_node` is somewhere in that path. To make the path from an ancestor to `v` have unique values, we must remove `prev_node` and all nodes before it (ancestors) because they are before the duplicate? Actually we need to start after `prev_node`. So we should pop nodes from the stack until we have removed `prev_node`. That means we pop all nodes from the top down to and including `prev_node`. After popping, the new stack contains the nodes from the child of `prev_node` down to the parent of `v`. Then we push `v`. The resulting stack is the unique path from the child of `prev_node` to `v`. The length of this path is `cum_len[v] - cum_len[prev_node]` (since `prev_node` is the parent of the new first node). The node count is `depth[v] - depth[prev_node]`.
- If `nums[v]` not in `path_values`, we just push and add to set.
- After processing, we update the best answer with the current path (the entire stack). The path length is `cum_len[current] - cum_len[parent_of_first]`, where `parent_of_first` is the node that was popped last (the duplicate) or None if the stack starts at root. Node count is `depth[current] - depth[parent_of_first]` (or `depth[current]+1` if parent is None).
- When backtracking, we pop `v` from the stack and remove its value from the set. If we had popped some nodes due to duplicate, we need to push them back? Actually when we backtrack from `v`, we are returning to its parent. The stack should be exactly as it was before we entered `v`. That means we need to undo the pops and the push. We can do that by remembering the state before entering `v`: we can save the stack length and the set. But we also need to know which nodes were popped. We can save the list of popped nodes (or their values) and push them back. This is similar to the previous approach.

Given the complexity, the approach with `path_nodes` list and `path_start` pointer, plus saving truncated nodes for backtrack, seems manageable.

Let's design the algorithm step by step:

**Data structures:**
- `adj`: adjacency list with (neighbor, edge_length).
- `cum_len`: array of size n, cumulative edge length from root.
- `depth`: array of size n, depth (number of edges from root).
- `path_nodes`: list of node ids currently in the valid path (from some ancestor to current node). This list is append-only; we never remove from the middle, only move `path_start` forward.
- `path_start`: integer, index in `path_nodes` of the first node of the current valid path.
- `value_to_index`: dict mapping value to the index in `path_nodes` of its last occurrence. (We will use lazy deletion: when checking, we verify `index >= path_start`.)

**DFS function:** `dfs(u, parent)`:
- For each child (v, w) of u where v != parent:
  - Compute `cum_len[v] = cum_len[u] + w`
  - `depth[v] = depth[u] + 1`
  - Save `old_path_start = path_start`
  - Save `truncated_nodes = []` (list of values to delete from `value_to_index` on backtrack)
  - Append `v` to `path_nodes` (index = len(path_nodes))
  - If `nums[v]` in `value_to_index` and `value_to_index[nums[v]] >= path_start`:
        - `idx = value_to_index[nums[v]]`
        - `prev_node = path_nodes[idx]`
        - For i in range(path_start, idx+1):
            truncated_nodes.append(nums[path_nodes[i]])
        - `path_start = idx + 1`
  - Set `value_to_index[nums[v]] = len(path_nodes) - 1`
  - Now compute candidate path:
        - If `path_start == 0`:
            parent_cum_len = 0
            parent_depth = -1
        - else:
            parent_node = path_nodes[path_start - 1]
            parent_cum_len = cum_len[parent_node]
            parent_depth = depth[parent_node]
        - path_length = cum_len[v] - parent_cum_len
        - node_count = depth[v] - parent_depth
        - Update best.
  - Recursively call `dfs(v, u)`
  - **Backtrack:**
        - Pop `v` from `path_nodes` (remove last element)
        - Delete `value_to_index[nums[v]]` (or set to -1)
        - For each val in truncated_nodes:
            del value_to_index[val]
        - `path_start = old_path_start`

**Initial call:** `dfs(0, -1)` after setting `cum_len[0] = 0`, `depth[0] = 0`, `path_nodes = [0]`, `path_start = 0`, `value_to_index[nums[0]] = 0`. Then evaluate the root as a candidate: path_length = 0, node_count = 1. Update best.

**Complexities:** O(n) time and O(n) space.

**Potential issues:**
- The `truncated_nodes` list might be large, but total size across all recursive calls is O(n) because each node is truncated at most once.
- We need to be careful with the order: we save `old_path_start` before any modifications. We also need to save the list of nodes to truncate before we change `path_start`. Actually we can compute truncated_nodes after we know `idx`. We iterate from `path_start` to `idx` inclusive and collect their values. This is O(k) per truncation.
- On backtrack, we delete those values from `value_to_index`. But we also need to ensure that we don't delete a value that might have been overwritten by a later occurrence? Actually we are deleting the entries for the nodes that were removed from the path. Those entries are still in `value_to_index` with their old indices. Since we are restoring `path_start` to `old_path_start`, those nodes are no longer in the path, so we should delete their entries. However, what if one of those values was also present in a node that is still in the path? That can't happen because the path is a simple chain: if a value appears twice, the earlier occurrence is removed, and the later occurrence remains. So the value is still represented by the later occurrence. So deleting the entry for the earlier occurrence is safe because the later occurrence has its own entry (which we set when we appended the later node). But wait: when we truncated, we removed the earlier occurrence and all nodes before it. The later occurrence (the current node) is still in the path and we set its entry. So the value is now represented by the current node. So deleting the entry for the earlier occurrence is fine. However, what about other values that were in the truncated nodes? They are no longer in the path, so their entries should be deleted. But could one of those values have been overwritten by a later occurrence? No, because the truncated nodes are all before the current node in the path, and the current node is the only new addition. The values in the truncated nodes are unique within the path (since the path was unique before truncation). So each value appears exactly once in the truncated segment. So deleting their entries is safe.

- Edge case: when `idx` is the last index before appending? Actually we append `v` first, then check for duplicate. If the duplicate is the current node's value, then `value_to_index` might point to some previous index. We truncate to `idx+1`. The current node is at the new end. So the truncated nodes are from old `path_start` to `idx`. The current node is not truncated. So its entry is set after truncation. Good.

- We also need to handle the case where the duplicate value is not in the current path (i.e., `value_to_index` has an entry but its index < `path_start`). In that case, we ignore it and just set the new entry. So we don't truncate. That's correct.

**Testing with examples:**
Example 1:
edges = [[0,1,2],[1,2,3],[1,3,5],[1,4,4],[2,5,6]], nums = [2,1,2,1,3,1]
Tree:
0(2) -1(1) -2(2) -5(1)
          |3(1)
          |4(3)
Wait, edges: 0-1 (2), 1-2 (3), 1-3 (5), 1-4 (4), 2-5 (6).
So root 0 (value 2). Children: 1 (value 1). 1's children: 2 (value 2), 3 (value 1), 4 (value 3). 2's child: 5 (value 1).
We need longest special path. Let's simulate:
- Start at root 0: path_nodes=[0], path_start=0, value_to_index={2:0}. Candidate: length=0, nodes=1.
- Go to child 1 (edge 2): cum_len[1]=2, depth=1. Append 1: path_nodes=[0,1]. value 1 not in map. Set value_to_index[1]=1. path_start=0. Candidate: parent_cum_len=0, parent_depth=-1. length=2-0=2, nodes=1-(-1)=2. Update best: length=2, nodes=2.
- Go to child 2 (edge 3): cum_len[2]=5, depth=2. Append 2: path_nodes=[0,1,2]. value 2 is in map at index 0. idx=0. Truncate: path_start = 1. truncated_nodes = [value of node 0 = 2]. Delete value_to_index[2]? Actually we will delete on backtrack, but for now we just move path_start. Set value_to_index[2]=2 (new index). Now path_start=1, path_nodes[1]=1, path_nodes[2]=2. Candidate: parent_node = path_nodes[0] = 0. parent_cum_len=0, parent_depth=0? Wait depth[0]=0. So parent_depth=0. length = cum_len[2] - 0 = 5. node_count = depth[2] - depth[0] = 2-0=2. So path from root? Actually path_start=1, so front is node 1. Its parent is node 0. So path is 1->2. Length = edge 1-2 = 3? But cum_len[2]=5, cum_len[0]=0, so 5. That's sum of edges 0-1 (2) and 1-2 (3) = 5. Node count = depth[2]-depth[0]=2, which is nodes 1 and 2. That's correct. Update best: length=5, nodes=2.
- Go to child 5 (edge 6): cum_len[5]=11, depth=3. Append 5: path_nodes=[0,1,2,5]. value 1 is in map at index 1. idx=1. Truncate: path_start = 2. truncated_nodes = [value of node 1 = 1]. Set value_to_index[1]=3. Now path_start=2, path_nodes[2]=2, path_nodes[3]=5. Candidate: parent_node = path_nodes[1] = 1. parent_cum_len = cum_len[1]=2, parent_depth=1. length = 11-2=9. node_count = 3-1=2. Path is 2->5, length 6? Wait edge 2-5 is 6, but cum_len[5]=11, cum_len[2]=5, difference=6. Node count = depth[5]-depth[2]=3-2=1? That would be 1 node? Let's compute: depth[5]=3, depth[2]=2, so 3-2=1. But path is 2->5, which has 2 nodes. Our formula gives node_count = depth[v] - depth[parent_of_front]. parent_of_front is node 1 (depth 1). So depth[5] - depth[1] = 3-1=2. Yes, correct. So length=6, nodes=2. Update best: length=6, nodes=2.
- Backtrack from 5, then from 2, etc. Eventually we get best length 6, nodes 2. Matches example.

Example 2:
edges = [[1,0,8]], nums = [2,2]
Tree: 0-1, root 0. Both values 2.
- Root 0: candidate length 0, nodes 1.
- Child 1: cum_len[1]=8, depth=1. Append 1: value 2 in map at index 0. idx=0. Truncate: path_start=1. truncated_nodes=[2]. Set value_to_index[2]=1. Candidate: parent_node = path_nodes[0]=0. parent_cum_len=0, parent_depth=0. length=8-0=8, node_count=1-0=1. So path is just node 1? Actually path_start=1, front is node 1, parent is node 0. So path is node 1 alone. Length=8, nodes=1. But the longest special path should be length 0? Wait, the problem says: "The longest special paths are 0 and 1, both having a length of 0." Because the path from 0 to 1 has duplicate values, so it's not special. The only special paths are single nodes. So the maximum length is 0. Our algorithm gave length 8 for path 1 alone? That's wrong because path 1 alone is special (single node, length 0). But we computed length 8 because we used cum_len[1] - cum_len[0] = 8. But the path from 1 alone should have length 0, not 8. The issue is: when the path consists of a single node, the length is 0, not the edge length from its parent. In our candidate computation, we used parent_cum_len = cum_len[parent_of_front]. If the front is node 1, its parent is node 0. The path from node 1 to itself is length 0. But we computed cum_len[1] - cum_len[0] = 8, which is the edge length from 0 to 1. That's incorrect because the path does not include the edge from 0 to 1; it starts at node 1. So our formula for length is wrong when the path is just a single node? Let's re-evaluate.

We said: path_length = cum_len[v] - cum_len[parent_of_front]. If the path is just node v (i.e., front is v and parent_of_front is v's parent), then the path from v to v has length 0. But cum_len[v] - cum_len[parent] is the edge length from parent to v, which is not 0. So our formula is incorrect for the case where the path consists of a single node. Actually, the path from the front node to v is a sequence of nodes. If front == v, then the path is just v, length 0. In that case, parent_of_front is the parent of v, but we should not subtract the edge from parent to v. The correct length is 0. So we need to handle the case where the path has only one node.

In our candidate computation, we have:
- front = path_nodes[path_start]
- v = current node (which is path_nodes[-1])
If front == v, then the path is just v. The length should be 0. The node count should be 1.
Our formula: path_length = cum_len[v] - cum_len[parent_of_front]. If front == v, then parent_of_front is the parent of v. So cum_len[v] - cum_len[parent] = edge length from parent to v, which is not 0. So we need to adjust.

When does front == v? That happens when the path consists of a single node. This occurs when the current node's value is a duplicate of the previous occurrence, and we truncate such that the new front is the current node? Let's see: In example 2, at node 1, we truncated to path_start=1. The path_nodes list is [0,1]. path_start=1, so front = path_nodes[1] = 1. v = 1. So front == v. The path is just node 1. The length should be 0. But our formula gave 8.

So we need to compute path_length correctly. The path from front to v includes edges between consecutive nodes in the path. If front == v, there are no edges, length 0. If front != v, then the path includes edges from front to its child, etc., up to v. The sum of edge lengths is cum_len[v] - cum_len[parent_of_front]. But if front == v, then parent_of_front is the parent of v, and cum_len[v] - cum_len[parent] is the edge from parent to v, which is not part of the path. So we need to subtract that edge only if front != v? Actually, if front == v, the path is just v, so we should not subtract any edge. So the correct formula is:
- If front == v: path_length = 0, node_count = 1.
- Else: path_length = cum_len[v] - cum_len[parent_of_front], node_count = depth[v] - depth[parent_of_front].

But wait, is it possible that front == v but the path is longer? No, if front == v, the path is just v. So we can check if path_start == len(path_nodes) - 1. That is, the front is the last element. In that case, the path is a single node.

In example 2, path_start=1, len(path_nodes)=2, so path_start == len(path_nodes)-1, so front == v. So we should set length=0, nodes=1.

In example 1, at node 5, path_start=2, len(path_nodes)=4, so path_start != len(path_nodes)-1 (2 != 3). So front != v. Then length = cum_len[5] - cum_len[parent_of_front] = 11 - cum_len[1]=2 = 9? Wait, we computed earlier as 6. Let's recalc: cum_len[5]=11, parent_of_front = node 1, cum_len[1]=2, so 11-2=9. But the path from node 2 to node 5 is just edge 2-5 length 6. Why did we get 9? Because parent_of_front is node 1, but the path from node 2 to node 5 does not include node 1. The front is node 2. Its parent is node 1. So cum_len[5] - cum_len[1] includes edges 1-2 and 2-5. That's 3+6=9. But the path from node 2 to node 5 should only include edge 2-5, length 6. So our formula is still wrong! We are subtracting cum_len[parent_of_front] which is the cum_len of the parent of the front, but the path starts at the front, not at its parent. The sum of edge lengths from front to v is cum_len[v] - cum_len[front] + (edge from front to its child? Actually, the edges in the path are those between consecutive nodes. The first edge is from front to its child on the path to v. That child's cum_len is cum_len[front] + edge(front, child). So the sum of edges from front to v is cum_len[v] - cum_len[front]. Because cum_len[v] includes all edges from root to v, and cum_len[front] includes edges from root to front. The difference is the sum of edges from front to v. So the correct formula is:
- path_length = cum_len[v] - cum_len[front]
- node_count = depth[v] - depth[front] + 1

Let's test:
- Example 1, node 5: front = path_nodes[2] = 2. cum_len[5]=11, cum_len[2]=5, difference=6. depth[5]=3, depth[2]=2, node_count = 3-2+1=2. Correct.
- Example 1, node 2: front = path_nodes[1] = 1. cum_len[2]=5, cum_len[1]=2, difference=3. depth[2]=2, depth[1]=1, node_count=2-1+1=2. But the path from 1 to 2 is length 3, nodes 2. However, earlier we had a candidate for node 2 with length 5? Wait, we computed earlier: for node 2, after truncation, path_start=1, front=1. So length = cum_len[2] - cum_len[1] = 5-2=3. But earlier we said length=5? Let's re-check example 1 simulation:
At node 2: we appended 2, then truncated because value 2 duplicate. path_start became 1. front = path_nodes[1] = 1. So length = cum_len[2] - cum_len[1] = 5-2=3. Node count = depth[2]-depth[1]+1 = 2-1+1=2. So path is 1->2, length 3, nodes 2. But earlier I thought length=5. That was a mistake. The correct candidate for node 2 is length 3. But the best path is length 6 from 2->5. So that's fine.
- Example 2, node 1: front = path_nodes[1] = 1. cum_len[1]=8, cum_len[1]=8, difference=0. depth[1]=1, depth[1]=1, node_count=1-1+1=1. So length=0, nodes=1. Correct.
- Root: front = path_nodes[0] = 0. cum_len[0]=0, cum_len[0]=0, difference=0. node_count=0-0+1=1. Correct.

So the correct formulas are:
- front = path_nodes[path_start]
- path_length = cum_len[v] - cum_len[front]
- node_count = depth[v] - depth[front] + 1

This is much simpler and avoids the parent_of_front confusion. We don't need to compute parent_of_front at all. We just need the front node's cum_len and depth.

Thus the algorithm simplifies:
- At each node v (including root), after updating the path, compute:
    front = path_nodes[path_start]
    path_length = cum_len[v] - cum_len[front]
    node_count = depth[v] - depth[front] + 1
- Update best.

Now we need to ensure that the path from front to v is indeed the current valid path. Since we maintain `path_nodes` and `path_start` such that the sublist from `path_start` to the end contains nodes with unique values and forms a downward path from an ancestor (the front) to the current node v. This is true by construction.

**Backtracking:** We still need to save `old_path_start` and `truncated_nodes` to restore on backtrack.

**Implementation details:**
- We'll use recursion with `sys.setrecursionlimit`.
- We'll store `cum_len` and `depth` as lists of size n.
- We'll use a list for `path_nodes`.
- We'll use a dict for `value_to_index`.

**Potential issue:** When we truncate, we move `path_start` to `idx+1`. The nodes from old `path_start` to `idx` are no longer in the path. We need to delete their entries from `value_to_index` on backtrack. But we also need to ensure that during the recursion, those entries are not considered. Since we check `index >= path_start`, they are ignored. So it's fine.

**Edge case:** What if the duplicate value appears at the very beginning of the path? For example, path_start=0, and the duplicate is at index 0. Then we set path_start=1. The truncated node is the root. That's fine.

**Testing with example 1 again with corrected formulas:**
- Root 0: front=0, length=0, nodes=1.
- Node 1: front=0, length=2-0=2, nodes=1-0+1=2.
- Node 2: after truncation, path_start=1, front=1, length=5-2=3, nodes=2-1+1=2.
- Node 5: after truncation, path_start=2, front=2, length=11-5=6, nodes=3-2+1=2.
- Node 3: from node 1, child 3 (value 1). cum_len[3]=7, depth=2. Append 3: value 1 in map at index 1. idx=1. Truncate: path_start=2. truncated_nodes=[value of node 1 = 1]. Set value_to_index[1]=3. Now path_nodes=[0,1,2,5? Wait, we are at node 3, not 5. Actually after node 2, we backtrack to node 1, then go to child 3. So path_nodes before entering 3: after backtracking from 2, we restored path_nodes to [0,1] (since we popped 2 and restored path_start to 0? Actually after node 2, we backtrack: we popped 2, deleted truncated_nodes (value 2), restored path_start to old_path_start (which was 0). So path_nodes=[0,1], path_start=0, value_to_index={2:0,1:1}. Now go to child 3: cum_len[3]=7, depth=2. Append 3: path_nodes=[0,1,3]. value 1 in map at index 1. idx=1. Truncate: path_start=2. truncated_nodes=[value of node 1 = 1]. Set value_to_index[1]=2. Now front = path_nodes[2]=3. length = cum_len[3] - cum_len[3] = 0? Wait cum_len[3]=7, cum_len[3]=7, so 0. nodes = depth[3]-depth[3]+1=1. So path is just node 3, length 0. That's correct because path 1->3 has duplicate 1? Actually path from 1 to 3: values 1 and 1, duplicate, so not special. The only special path ending at 3 is just node 3. So length 0.
- Node 4: from node 1, child 4 (value 3). cum_len[4]=6, depth=2. Append 4: path_nodes=[0,1,4]. value 3 not in map. Set value_to_index[3]=2. front=0, length=6-0=6, nodes=2-0+1=3. Path 0->1->4, length 6, nodes 3. But example says longest special paths are 2->5 and 0->1->4, both length 6, and minimum nodes is 2. Our node count for 0->1->4 is 3, but example says minimum nodes is 2. Wait, example says: "The longest special paths are 2 -> 5 and 0 -> 1 -> 4, both having a length of 6. The minimum number of nodes across all longest special paths is 2." So path 0->1->4 has 3 nodes, but they say minimum nodes is 2. That implies that the path 2->5 has 2 nodes and length 6, and that is the minimum node count among all longest paths. So our computed node count for 0->1->4 is 3, which is correct. The best length is 6, and among paths with length 6, the minimum node count is 2 (from 2->5). So our algorithm should update best_len=6, best_nodes=2 when we see 2->5, and then when we see 0->1->4 with length 6 and nodes 3, we should not update because nodes > 2. So final answer [6,2]. That matches.

So the corrected formulas work.

**Final algorithm steps:**
1. Build adjacency list.
2. Initialize arrays: cum_len[0]=0, depth[0]=0.
3. Initialize path_nodes = [0], path_start = 0, value_to_index = {nums[0]: 0}.
4. Initialize best_len = 0, best_nodes = 1.
5. Evaluate root: front = path_nodes[0]; path_length = 0; node_count = 1; update best.
6. DFS from root:
   For each child (v, w):
     - cum_len[v] = cum_len[u] + w
     - depth[v] = depth[u] + 1
     - Save old_path_start = path_start
     - Save truncated_nodes = []
     - Append v to path_nodes
     - If nums[v] in value_to_index and value_to_index[nums[v]] >= path_start:
         idx = value_to_index[nums[v]]
         For i in range(path_start, idx+1):
             truncated_nodes.append(nums[path_nodes[i]])
         path_start = idx + 1
     - value_to_index[nums[v]] = len(path_nodes) - 1
     - Compute candidate:
         front = path_nodes[path_start]
         path_length = cum_len[v] - cum_len[front]
         node_count = depth[v] - depth[front] + 1
         Update best.
     - Recursively dfs(v, u)
     - Backtrack:
         Pop v from path_nodes
         del value_to_index[nums[v]]
         For val in truncated_nodes:
             del value_to_index[val]
         path_start = old_path_start

**Complexities:** O(n) time, O(n) space.

**Potential pitfalls:**
- The truncated_nodes list might contain duplicates? No, because the path from path_start to idx has unique values (since it was a valid path before truncation). So each value appears once.
- When we delete truncated_nodes on backtrack, we must ensure we delete the correct entries. Since we saved the values, we can just `del value_to_index[val]`. But what if a value in truncated_nodes was overwritten by a later occurrence? As argued, it cannot be because the truncated nodes are all before the current node, and the current node is the only new addition. The values in truncated nodes are unique and not present elsewhere in the path (since the path was unique). So deleting them is safe.
- However, there is a subtle case: what if the truncated segment includes the node that was the previous occurrence of the current value? That node's value is the same as the current node's value. We are deleting that value from the map. But we also set `value_to_index[nums[v]]` to the new index. So after truncation, the map has the new index for that value. On backtrack, we delete the new index (when we pop v) and also delete the old index (from truncated_nodes). So the map becomes empty for that value, which is correct because after backtracking, the path is restored to before entering v, and the value is not present (since the previous occurrence was removed and the current node is removed). So it's fine.

- Another subtle case: what if the duplicate value appears multiple times in the path? For example, path has values A, B, A, C. When we encounter the second A, we truncate to after the first A. The truncated nodes are A and B? Actually the first A is at index 0, B at 1. We truncate to idx+1=1. So truncated_nodes = [A, B]. We delete A and B. Then we append C. The map now has A (new index) and C. That's correct.

- We need to ensure that when we compute truncated_nodes, we iterate from `path_start` to `idx` inclusive. This is O(k). Since each node is truncated at most once, total O(n).

**Alternative simpler approach:** Use a stack and a set, and compute length as sum of edge lengths in the stack. But we need to compute sum quickly. We can maintain cumulative lengths for each node in the stack. The stack would be the current valid path. When we pop nodes due to duplicate, we can compute the new length as cum_len[current] - cum_len[parent_of_first]. But we need to know the parent of the first node in the stack. That is the node that was popped last (the duplicate). So we can keep track of that. This might be simpler to implement without the need to save truncated_nodes for backtrack? Let's explore:

Maintain:
- `stack`: list of nodes (the current valid path from some ancestor to current node). The first node in the stack is the start of the path.
- `value_set`: set of values in the stack.
- `cum_len` and `depth` arrays.

When entering child v:
- Push v onto stack.
- If nums[v] in value_set:
    - We need to pop nodes from stack until we remove the previous occurrence of nums[v]. Let `prev_node` be the node in the stack with that value. We pop nodes from the stack until we pop `prev_node` (inclusive). After popping, the new top of the stack (if any) is the child of `prev_node`? Actually after popping `prev_node`, the next node in the stack is the node that was after `prev_node` in the original path. That node is the child of `prev_node` along the path to v. So the new stack contains nodes from that child down to the parent of v. Then we push v. The resulting stack is the unique path from that child to v.
- Update value_set: add nums[v], and remove values of popped nodes.
- The current path is the entire stack. Its length is the sum of edge lengths of the edges between consecutive nodes in the stack. We can compute that as: if the stack has only one node, length=0. If more than one, the first edge is from stack[0] to stack[1]. The sum of edges is cum_len[stack[-1]] - cum_len[parent_of_stack[0]]. But parent_of_stack[0] is the node that was popped last (the duplicate) or None if stack[0] is root. We can get that by storing the popped node. Alternatively, we can compute the sum by iterating over the stack, but that's O(stack size) per node, too slow.
- We can compute the sum as: let `first = stack[0]`. If `first` is the root, then the sum is cum_len[stack[-1]] (since root cum_len=0). If `first` is not root, then the sum is cum_len[stack[-1]] - cum_len[parent_of_first]. The parent_of_first is the node that was the previous occurrence (the duplicate) that we popped. We can save that node when we pop. So we need to know the parent of the first node in the stack. That is exactly the node that was popped last (the duplicate). So we can store `last_popped` as the node that was popped due to the duplicate. If no duplicate occurred, `last_popped` is None (or the parent of the root, which we can treat as None).
- Then path_length = cum_len[current] - cum_len[last_popped] if last_popped is not None, else cum_len[current].
- Node count = len(stack).

This seems simpler because we don't need to maintain `path_start` and `value_to_index`. We just maintain a stack and a set. When we backtrack, we pop the current node and remove its value from the set. If we had popped some nodes due to duplicate, we need to push them back? Actually when we backtrack from v, we need to restore the stack to the state it had before entering v. That means we need to undo the pops and the push. We can do that by remembering the state before entering v: we can save the stack length and the set. But we also need to restore the popped nodes. We can save the list of popped nodes (or their values) and push them back. This is similar to the previous approach but with a stack instead of a list with a start pointer. The advantage is that we don't need to manage `path_start` and `value_to_index`. However, we still need to save the popped nodes for backtrack. So it's not much simpler.

Given that the first approach with `path_nodes` and `path_start` is already clear, we can proceed with that.

**One more optimization:** Instead of saving `truncated_nodes` as a list of values, we can save the range of indices and on backtrack iterate again to delete. But that would require re-iterating, which is fine since each node is deleted once. However, we need to know the values to delete from the dict. We can just iterate from old_path_start to idx and delete. But we need to know old_path_start and idx. We can save them. On backtrack, we can do:
    for i in range(old_path_start, idx+1):
        del value_to_index[nums[path_nodes[i]]]
But we also need to restore path_start. So we can save old_path_start and idx. Then on backtrack, we iterate and delete. This avoids storing a separate list. But we need to ensure that the indices are still valid (they are, since we haven't popped anything from path_nodes yet). Actually we pop v after the recursion, but before that we restore. So we can do:
    Save old_path_start and idx (if truncation happened, else idx = old_path_start - 1 or something).
But we need to know if truncation happened. We can save a flag or just save the new_path_start. Actually we can save old_path_start and new_path_start. If new_path_start > old_path_start, then truncation happened. The truncated range is from old_path_start to new_path_start-1. So we can iterate that range and delete. This is clean.

So in the DFS:
    old_path_start = path_start
    truncated = False
    if duplicate and idx >= path_start:
        new_path_start = idx + 1
        for i in range(path_start, new_path_start):
            del value_to_index[nums[path_nodes[i]]]
        path_start = new_path_start
        truncated = True
    # ... recursion ...
    # backtrack:
    if truncated:
        for i in range(old_path_start, path_start):
            del value_to_index[nums[path_nodes[i]]]
    path_start = old_path_start
    pop v
    del value_to_index[nums[v]]

But careful: when we delete on backtrack, we are deleting the entries for the nodes that were truncated. However, those nodes are still in `path_nodes` (since we haven't popped them). Their indices are from old_path_start to path_start-1. But after we restore path_start to old_path_start, those nodes are back in the path. So we need to re-insert their entries into `value_to_index`. Wait, we deleted them on truncation, and now on backtrack we are deleting them again? That's wrong. We need to restore them. So we should not delete them on truncation; we should only delete them on backtrack? Actually we need to ensure that during the recursion, those entries are not considered. So we must delete them (or invalidate them) when we truncate. Then on backtrack, we need to restore them (re-insert them into `value_to_index`). So we need to save them and re-insert. So it's better to save the list of values to delete on truncation, and on backtrack, re-insert them. Or we can use the lazy approach: don't delete on truncation, but check `index >= path_start`. Then on backtrack, we don't need to re-insert because they are still there. But as we saw, if we don't delete on truncation, then on backtrack when we restore path_start to old_path_start, those entries become valid again, which is correct because they are back in the path. So the lazy approach works without needing to delete on truncation. However, we must ensure that during the recursion, we don't accidentally use those entries. Since we check `index >= path_start`, they are ignored. So we can simply not delete on truncation. Then on backtrack, we just restore path_start and pop v. We don't need to delete or re-insert anything for the truncated nodes. But wait: what about the entry for the duplicate value? We set `value_to_index[nums[v]]` to the new index. That overwrites the old index. So the old index is lost. On backtrack, we delete the new index (when we pop v). The old index is not restored. But after backtracking, the path is restored to before entering v, which includes the old occurrence of that value. So we need to restore the old index. So we must save the old index and restore it on backtrack. So we need to save the previous value and index for the duplicate value.

Thus, with lazy deletion, we need to handle the duplicate value specially: when we encounter a duplicate, we overwrite the entry. On backtrack, we need to restore the old entry. So we can save `old_value_index` (the previous index for that value) and on backtrack set `value_to_index[nums[v]] = old_value_index`. But we also need to restore the truncated nodes' entries? Actually if we didn't delete them, they are still there with their old indices. After backtracking, path_start is restored to old_path_start, so those indices are >= path_start, so they become valid again. So we don't need to restore them. However, we must ensure that during the recursion, we didn't accidentally use them. Since we check `index >= path_start`, they are ignored. So it's fine.

But there is a catch: when we truncate, we move path_start forward. The truncated nodes' indices are now < path_start. Their entries are still in `value_to_index` with those indices. If later in the same recursion (e.g., deeper in the tree), we encounter a value that was in the truncated nodes, we will look it up and find an index < path_start, so we ignore it. That's correct. On backtrack, we restore path_start, so those entries become valid again. So the lazy approach works without needing to delete or restore truncated nodes' entries. The only thing we need to restore on backtrack is the entry for the duplicate value (the one we overwrote). So we can save `old_index_for_value` = `value_to_index[nums[v]]` before overwriting. On backtrack, set `value_to_index[nums[v]] = old_index_for_value`.

But wait: what if the duplicate value was not in the current path (i.e., its index < path_start)? Then we don't truncate, we just overwrite. On backtrack, we need to restore the old index. That's fine.

So the lazy approach with saving the old index for the overwritten value is sufficient. We don't need to delete truncated nodes' entries. This simplifies backtracking greatly.

Let's refine the algorithm with lazy deletion and saving the old index:

**DFS(u, parent):**
- For each child (v, w):
    - cum_len[v] = cum_len[u] + w
    - depth[v] = depth[u] + 1
    - old_path_start = path_start
    - old_index = -1
    - if nums[v] in value_to_index:
        old_index = value_to_index[nums[v]]
    - Append v to path_nodes (index = len(path_nodes))
    - if nums[v] in value_to_index and value_to_index[nums[v]] >= path_start:
        idx = value_to_index[nums[v]]
        path_start = idx + 1
    - value_to_index[nums[v]] = len(path_nodes) - 1
    - Compute candidate:
        front = path_nodes[path_start]
        path_length = cum_len[v] - cum_len[front]
        node_count = depth[v] - depth[front] + 1
        Update best.
    - dfs(v, u)
    - Backtrack:
        - Pop v from path_nodes
        - if old_index != -1:
            value_to_index[nums[v]] = old_index
        - else:
            del value_to_index[nums[v]]
        - path_start = old_path_start

This is clean. We don't need to delete truncated nodes' entries. The only potential issue is that `value_to_index` might contain entries for values that are not in the current path (because they were truncated). But we always check `index >= path_start` before using an entry. So it's safe.

**Testing with example 1:**
- Root: path_nodes=[0], path_start=0, value_to_index={2:0}. best: length=0, nodes=1.
- Node 1: old_path_start=0, old_index=-1 (value 1 not in map). Append 1: path_nodes=[0,1]. value 1 not in map, so no truncation. value_to_index[1]=1. front=0, length=2, nodes=2. Update best: length=2, nodes=2.
- Node 2: old_path_start=0, old_index=0 (value 2 in map at 0). Append 2: path_nodes=[0,1,2]. Check: value_to_index[2]=0 >= path_start=0, so truncate: idx=0, path_start=1. value_to_index[2]=2. front=path_nodes[1]=1, length=5-2=3, nodes=2-1+1=2. Update best: length=3, nodes=2 (but best is 2, so no update).
- Recurse into 5: old_path_start=1, old_index=1 (value 1 in map at 1). Append 5: path_nodes=[0,1,2,5]. Check: value_to_index[1]=1 >= path_start=1, so truncate: idx=1, path_start=2. value_to_index[1]=3. front=path_nodes[2]=2, length=11-5=6, nodes=3-2+1=2. Update best: length=6, nodes=2.
- Backtrack from 5: pop 5, old_index=1, so set value_to_index[1]=1. path_start=1.
- Backtrack from 2: pop 2, old_index=0, so set value_to_index[2]=0. path_start=0.
- Node 3: old_path_start=0, old_index=1 (value 1 in map at 1). Append 3: path_nodes=[0,1,3]. Check: value_to_index[1]=1 >= path_start=0, so truncate: idx=1, path_start=2. value_to_index[1]=2. front=path_nodes[2]=3, length=7-7=0, nodes=1. Update best: length=0? No, best is 6.
- Backtrack from 3: pop 3, old_index=1, set value_to_index[1]=1. path_start=0.
- Node 4: old_path_start=0, old_index=-1 (value 3 not in map). Append 4: path_nodes=[0,1,4]. No truncation. value_to_index[3]=2. front=0, length=6, nodes=3. Update best: length=6, nodes=2 (since nodes=3 > 2, no update).
- Backtrack from 4: pop 4, old_index=-1, del value_to_index[3]. path_start=0.
- Backtrack from 1: pop 1, old_index=-1, del value_to_index[1]. path_start=0.
- End. best_len=6, best_nodes=2. Correct.

**Testing example 2:**
- Root 0: path_nodes=[0], path_start=0, value_to_index={2:0}. best: length=0, nodes=1.
- Node 1: old_path_start=0, old_index=0 (value 2 in map at 0). Append 1: path_nodes=[0,1]. Check: value_to_index[2]=0 >= path_start=0, so truncate: idx=0, path_start=1. value_to_index[2]=1. front=path_nodes[1]=1, length=8-8=0, nodes=1. Update best: length=0, nodes=1 (equal length, nodes=1, so no update because best_nodes=1 already).
- Backtrack: pop 1, old_index=0, set value_to_index[2]=0. path_start=0.
- End. best_len=0, best_nodes=1. Correct.

**Edge case:** What if the root has a duplicate value with itself? Not possible since it's the only occurrence.

**Complexity:** O(n) time and space.

**Implementation details:**
- Use `sys.setrecursionlimit(10**6)`.
- Build adjacency list as list of lists of (neighbor, length).
- Use iterative DFS to avoid recursion limit? Recursion depth up to 5e4, which might be okay with increased limit. But to be safe, we can use recursion.

**Potential issue:** The `value_to_index` dict might have stale entries for values that are not in the current path. But we always check `index >= path_start`. However, when we restore `old_index` on backtrack, we set it to the old index. That old index might be < path_start? Actually after backtracking, path_start is restored to old_path_start. The old index we saved was the index before we entered the child. That index was valid at that time (>= old_path_start). So after restoring, it will be >= old_path_start, so it's valid. Good.

**One more check:** When we truncate, we set `path_start = idx + 1`. The node at `idx` is the previous occurrence. Its value is the same as the current node's value. We overwrite `value_to_index[nums[v]]` with the new index. So the old index is lost. We saved it in `old_index`. On backtrack, we restore it. So the map is consistent.

**What about values that appear multiple times in the path?** For example, values A, B, A, C. When we encounter the second A, we truncate to after the first A. The truncated nodes are A and B. Their entries remain in `value_to_index` with indices < path_start. They are ignored. On backtrack from C, we restore path_start and the old index for A. The entries for A and B are still there with their old indices. After restoring path_start, they become valid again. So the path is restored correctly.

**Conclusion:** This algorithm is correct and efficient.

Now we need to write the solution in the required format.

**Code structure:**
```python
from typing import List
import sys

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
        
        cum_len = [0] * n
        depth = [0] * n
        
        path_nodes = []
        path_start = 0
        value_to_index = {}
        
        best_len = 0
        best_nodes = 1
        
        sys.setrecursionlimit(10**6)
        
        def dfs(u, parent):
            nonlocal best_len, best_nodes, path_start
            for v, w in adj[u]:
                if v == parent:
                    continue
                cum_len[v] = cum_len[u] + w
                depth[v] = depth[u] + 1
                
                old_path_start = path_start
                old_index = -1
                if nums[v] in value_to_index:
                    old_index = value_to_index[nums[v]]
                
                path_nodes.append(v)
                if nums[v] in value_to_index and value_to_index[nums[v]] >= path_start:
                    idx = value_to_index[nums[v]]
                    path_start = idx + 1
                value_to_index[nums[v]] = len(path_nodes) - 1
                
                # Evaluate current path
                front = path_nodes[path_start]
                path_length = cum_len[v] - cum_len[front]
                node_count = depth[v] - depth[front] + 1
                if path_length > best_len or (path_length == best_len and node_count < best_nodes):
                    best_len = path_length
                    best_nodes = node_count
                
                dfs(v, u)

## worker: Complete the backtracking code after the recursive
The solution uses a depth-first search from the root while maintaining a sliding window of the current path. The `path_nodes` list holds the nodes in the current valid path (from some ancestor down to the current node), and `path_start` is the index of the first node in that valid segment. The `value_to_index` dictionary maps each value to its index in `path_nodes` (lazy: we check if the stored index is still within the current valid path by comparing it to `path_start`). When a duplicate value is encountered, we move `path_start` to just after the previous occurrence, effectively truncating the path. The cumulative edge length from the front node to the current node gives the path length, and the difference in depths plus one gives the number of nodes. We update the best length and minimum node count for that length. Backtracking restores the previous `path_start` and the old index for the overwritten value.

The algorithm runs in O(n) time and O(n) space, suitable for n up to 5×10⁴.
