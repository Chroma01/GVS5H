
## ideation
**Core difficulty:**  
We need to consider *downward* (ancestor→descendant) paths only, not arbitrary paths. The path must have all distinct node values. We want to maximize total edge length sum, and among those max-length paths, minimize the number of nodes.

**Observations:**  
- Because it's a tree rooted at 0, any downward path is a contiguous segment of the current DFS stack (root → current node).
- Maintaining a stack of (node, cumulative distance from root) is natural.
- To enforce uniqueness of values along the current path, we need to know the most recent position (stack index) where each value appeared. If we see a duplicate, we must pop the stack back to just after the previous occurrence (i.e., set `start = last_occurrence + 1`).
- After adjusting `start`, the current path from `start` to current node is guaranteed to have unique values.
- The length of this path is `dist[top] - dist[start-1]` (or `dist[top] - dist[start]` depending on indexing). Node count is `top - start + 1`.
- We update global best: if length > best_len, update best_len and best_nodes = current node count; if length == best_len, update best_nodes = min(best_nodes, current node count).

**Pitfalls:**  
- Edge lengths are on edges, not nodes. The root has no incoming edge, so its cumulative distance is 0.
- When we pop back due to a duplicate, we must also clean up the `last_occurrence` map for values that are no longer on the path. However, we can avoid explicit cleanup by recomputing `start` and only considering values from `start` onward. But we need `last_occurrence` to reflect the *current* path (after truncation). So when we truncate, we must remove entries for popped nodes. Simplest: when we pop nodes, pop their values from the map (or re-record them). Since we always pop contiguous suffix, we can pop from the stack and the map together.
- The path may start and end at the same node (length 0). So we must consider single-node paths.
- n up to 5e4, recursion depth may be large; use iterative DFS or set recursion limit.
- nums[i] can be up to 5e4, so a dict or list of size max(nums)+1 works.

**Algorithm sketch:**  
1. Build adjacency list: for each edge [u, v, w], add both directions.
2. Iterative DFS using a stack of (node, parent). Maintain:
   - `path_nodes`: list of node values currently on the path (in order from root).
   - `path_dist`: list of cumulative distances from root to each node on the path (path_dist[0] = 0).
   - `last_occurrence`: dict value -> index in path_nodes of last occurrence.
3. For each node visited:
   - While `last_occurrence.get(nums[node], -1) >= start` (i.e., duplicate exists in current window), we need to truncate. Actually, we need to set `start = last_occurrence[nums[node]] + 1`. But we must also pop the entries from `last_occurrence` for nodes that are removed. Since we pop a suffix, we can pop from `path_nodes` and `path_dist` until the length equals `start`. For each popped node, remove its value from `last_occurrence` (or set to the new last index, but easier to pop and re-add? Actually we can just delete the entry; later when we push new nodes, we set new entry. But we need `last_occurrence` to reflect the *current* path. So after popping, we should delete the entry for that value, because it's no longer on the path. However, if the same value appears earlier (still on path), we need to keep that earlier occurrence. But since we pop contiguous suffix, the popped values are the most recent ones. So we can just `del last_occurrence[value]` for each popped node. But what if the same value appears again later? Then we'll set it again. That's fine.
   - Wait: if we pop node with value `v`, and there is an older occurrence of `v` still on the path, we must not delete it. But since we pop the suffix, the older occurrence is still on the path. However, `last_occurrence[v]` currently points to the index of the popped node (the most recent). If we delete it, we lose the info about the older occurrence. So we need to update `last_occurrence[v]` to the index of the older occurrence (if any). But we don't have that info easily. Alternative: Instead of popping and deleting, we can keep `last_occurrence` as a dict mapping value to the *current* index (most recent on the current path). When we truncate, we need to recompute `last_occurrence` for the remaining path. That's O(n) per step if done naively.
   - Better approach: Use a stack of (value, index) and maintain `last_occurrence` as a dict. When we encounter a duplicate at index `i`, we set `start = i + 1`. Then we need to pop nodes from the path until the path length equals `start`. For each popped node, we remove its value from `last_occurrence` only if its index matches the popped index. But we can just pop and then, after popping, we can set `last_occurrence[value] = new_index` if the value still appears. However, we don't know the new index without scanning. So we need a different data structure.

**Alternative data structure:**  
We can maintain `last_occurrence` as a dict mapping value to the *stack index* of its last occurrence. When we truncate, we pop nodes from the stack. For each popped node, we check if `last_occurrence[value] == popped_index`. If yes, we delete it (or set to the next occurrence, but we don't know). Actually, we can maintain a separate stack of values, and when we pop, we just pop the value from the value stack. The `last_occurrence` dict always points to the topmost occurrence. So when we pop the topmost, we delete the dict entry. If there is an older occurrence, it must be at a lower index, but its dict entry was overwritten when the newer one was pushed. So we lose it. That's a problem.

**Solution:**  
We can maintain `last_occurrence` as a dict mapping value to the *index* in the path stack. When we push a new node, we set `last_occurrence[value] = new_index`. When we need to truncate to `start`, we pop nodes from the stack until the stack size equals `start`. For each popped node at index `i`, we check if `last_occurrence.get(value) == i`. If yes, we delete it. But if there is an older occurrence, its index is less than `i`, and the dict entry was overwritten. So we lose it. However, after truncation, the older occurrence is still on the path (if `start` is after the older occurrence? No, `start` is set to `last_occurrence[value] + 1`, which is exactly after the previous occurrence. So the previous occurrence is at index `last_occurrence[value]`, which is now removed because we popped it? Wait: if we encounter a duplicate, the previous occurrence is at index `prev_idx = last_occurrence[value]`. We set `start = prev_idx + 1`. That means the previous occurrence is *not* included in the new path. So we must remove it. So the older occurrence is removed. So it's fine to delete the dict entry. But what if there is an even older occurrence? The path is truncated to start after the most recent duplicate. So all occurrences of that value before `prev_idx` are also removed (because they are before `start`). So we can safely delete the dict entry for that value. However, there might be other values that are popped; for those, we need to delete their dict entries only if they are the most recent occurrence. But since we pop a contiguous suffix, any popped node is the most recent occurrence of its value (because if there were a newer occurrence, it would be higher in the stack, but we are popping from the top). So we can safely delete the dict entry for each popped node's value.

Wait: consider value `v` appears at indices 2 and 5. We push index 5, dict has `v -> 5`. Now we encounter another `v` at index 6. `last_occurrence[v] = 5`. We set `start = 6`. We pop index 6? No, we haven't pushed it yet. Actually, we are about to push index 6. The duplicate is at index 5. So we need to truncate to start = 6. That means we pop indices 6? No, we pop from the stack until size = 6. But the stack currently has size 6 (indices 0..5). We need to pop index 5. So we pop node at index 5 (value `v`). We delete `last_occurrence[v]`. Now the stack has size 5 (indices 0..4). But there is an older occurrence of `v` at index 2. However, `last_occurrence` no longer has `v`. That's fine because the new path (indices 0..4) does not contain `v`? Wait, index 2 is still in the stack. So the path still contains `v` at index 2. But we lost the dict entry. That's a bug.

So we cannot simply delete the dict entry when popping. We need to update it to the previous occurrence. But we don't have that info.

**Better approach:**  
Instead of popping and updating dict, we can maintain `last_occurrence` as a dict mapping value to the *index* of its last occurrence on the current path. When we truncate, we don't physically pop the nodes from the stack; we just adjust a `start` pointer. But we need to know the cumulative distance at `start-1` to compute path length. We can keep the full stack of distances, but we need to know which nodes are "active". The `last_occurrence` dict must reflect only the active window. So when we move `start` forward, we need to remove entries for values that are no longer in the window. This is tricky.

**Standard solution for "longest special path" (LeetCode 3425):**  
I recall this problem: "Longest Special Path" on LeetCode. The typical solution uses DFS with a stack of (node, cumulative distance) and a hashmap `last` mapping value to the index in the stack of its last occurrence. When a duplicate is found, we pop the stack back to the index after the previous occurrence. While popping, we update `last` for the popped nodes? Actually, the standard solution uses a list `path` of nodes and a dict `pos` mapping value to its position in `path`. When a duplicate is encountered, we set `start = pos[value] + 1`. Then we pop nodes from `path` until `len(path) == start`. For each popped node, we remove its value from `pos` if `pos[value] == popped_index`. But as we saw, this fails if there is an older occurrence. However, in the standard solution, they don't remove; they just update `pos` when pushing new nodes. When popping, they don't delete from `pos`; they just let it be overwritten later. But then `pos` might contain stale indices that are less than `start`. That's okay because when we check for duplicates, we only care about the most recent occurrence. If `pos[value] < start`, it's not in the current window. So we can ignore it. But we need to ensure that when we push a new node, we set `pos[value] = new_index`. And when we pop, we don't need to delete. However, we need to compute the path length correctly. The path length is `dist[current] - dist[start-1]`. The `start` is the index of the first node in the current window. We maintain `start` as a variable. When we encounter a duplicate at index `i`, we set `start = i + 1`. But we also need to pop the stack to reflect that nodes before `start` are no longer in the window? Actually, we can keep the full stack and just adjust `start`. The `dist` array still has distances for all nodes. The path from `start` to current is valid. The `last_occurrence` dict may have stale entries, but we only use it to find the index of the most recent occurrence. If the stored index is < `start`, it's invalid. So when checking for duplicate, we should check `if last_occurrence.get(value, -1) >= start`. If so, we need to update `start = last_occurrence[value] + 1`. But we don't need to pop the stack physically; we just update `start`. However, we need to ensure that the stack doesn't grow indefinitely? It can grow up to n, which is fine. But we need to compute the path length using `dist[current] - dist[start-1]`. So we need `dist` for all nodes on the path from root to current. That's fine.

But wait: if we don't pop, then `last_occurrence` may have an entry for a value that is no longer in the window (because we moved `start` past it). That's okay as long as we check `>= start`. However, when we later encounter the same value again, we will see `last_occurrence[value]` which might be an old index < `start`. We will treat it as not in the window, so we won't truncate. That's correct. But what if we encounter a value that is in the window? Its index in `last_occurrence` will be the most recent one, which is >= `start`. So we truncate correctly.

So we can avoid popping entirely! We just maintain:
- `stack_nodes`: list of node values from root to current.
- `stack_dist`: list of cumulative distances.
- `last_occurrence`: dict value -> index in stack_nodes of most recent occurrence.
- `start`: index of the first node in the current valid window.

When we visit a node `u` with value `v = nums[u]`:
- If `v` in `last_occurrence` and `last_occurrence[v] >= start`:
    - `start = last_occurrence[v] + 1`
- Then push `v` onto `stack_nodes`, push `dist[u]` onto `stack_dist`.
- Set `last_occurrence[v] = len(stack_nodes) - 1`.
- Now the current window is `stack_nodes[start:]`. Its length is `stack_dist[-1] - (stack_dist[start-1] if start > 0 else 0)`.
- Node count is `len(stack_nodes) - start`.
- Update answer.

This works! And we don't need to pop. The `last_occurrence` dict may have stale entries (indices < `start`), but we ignore them by checking `>= start`. This is O(1) amortized per node.

But we need to be careful: when we move `start` forward, we don't remove the old entries from `last_occurrence`. That's fine. However, we must ensure that `stack_dist` has the correct distances for indices < `start`. They are still there, but we don't use them for the current window. That's fine.

One subtlety: when we set `start = last_occurrence[v] + 1`, we are effectively discarding the node at `last_occurrence[v]` and all nodes before it. But we don't physically remove them from the stack. That's okay because we only look at the suffix. However, we need to make sure that the `last_occurrence` dict doesn't cause issues later. For example, suppose value `a` appears at indices 2 and 5. We truncate to start=6. `last_occurrence[a]` is still 5. Later we encounter `a` again at index 7. We check `last_occurrence[a] >= start`? `5 >= 6` is false, so we don't truncate. That's correct because the occurrence at index 5 is no longer in the window. So we treat it as not present. Good.

But what if we encounter a value `b` that appears at index 3 (which is < start=6) and then again at index 8? `last_occurrence[b]` is 3. We check `3 >= 6` false, so we don't truncate. That's correct because index 3 is not in the window. So we can safely ignore stale entries.

Thus the algorithm is simple and efficient.

**Complexities:**  
- Time: O(n) because each node is visited once, and each operation is O(1) amortized.
- Space: O(n) for the stack and dict.

**Implementation details:**  
- Build adjacency list.
- DFS from root (0). Use iterative stack to avoid recursion depth issues, or set recursionlimit.
- Maintain `dist` array or just compute cumulative distance on the fly.
- Keep `path_vals` and `path_dist` lists.
- Keep `last_occurrence` dict.
- Keep `start` index (integer).
- Keep global `max_len` and `min_nodes`.

**Edge cases:**  
- Single node path: length 0, node count 1.
- Duplicate at root: if root value appears again, we truncate to start = index of root + 1 = 1. So path starts at child.
- All values same: longest special path is any single node, length 0, min nodes 1.

**Verification with examples:**  
Example 1: edges as given. Should output [6,2].
Example 2: [0,1] with edge length 8. Root 0, child 1. nums [2,2]. Path 0->1 has duplicate, so longest is single node length 0, min nodes 1. Output [0,1].

**Potential pitfalls:**  
- The `start` variable must be updated correctly. When we set `start = last_occurrence[v] + 1`, we must ensure that `last_occurrence[v]` is the index in the current stack. Since we push after checking, the index is the length of stack before push. So `last_occurrence[v]` is the index of the previous occurrence. So `start` becomes that index + 1. That's correct.
- The path length calculation: `path_dist[-1] - (path_dist[start-1] if start > 0 else 0)`.
- Node count: `len(path_vals) - start`.
- We need to handle the root specially: `start` initially 0, `path_dist` initially [0].

**Iterative DFS:**  
We can use a stack of (node, parent, state). Or we can do recursive with `sys.setrecursionlimit(10**6)`. Since n <= 5e4, recursion depth up to 5e4, which is okay in Python with increased recursion limit (default 1000). So we should set recursionlimit.

**Alternative: BFS?** No, we need to maintain path from root, so DFS is natural.

**Final plan:**  
1. Build adjacency list.
2. Initialize `path_vals = []`, `path_dist = [0]`, `last_occurrence = {}`, `start = 0`.
3. DFS from 0:
   - For each child, compute cumulative distance.
   - Apply the logic above.
4. Return [max_len, min_nodes].

**Testing:**  
We should test with small cases.

Let's write a quick mental test:
- n=2, edges=[[0,1,10]], nums=[1,2].
  - DFS: start=0, path_vals=[], path_dist=[0].
  - Visit 0: value 1. last_occurrence empty. Push: path_vals=[1], path_dist=[0]. last_occurrence[1]=0. start=0. Path length = 0 - 0 = 0. nodes = 1. max_len=0, min_nodes=1.
  - Visit 1: value 2. last_occurrence[2] not present. Push: path_vals=[1,2], path_dist=[0,10]. last_occurrence[2]=1. start=0. Path length = 10 - 0 = 10. nodes = 2. max_len=10, min_nodes=2.
  - Output [10,2]. Correct.

- n=2, nums=[1,1].
  - Visit 0: push, path length 0, max_len=0, min_nodes=1.
  - Visit 1: value 1. last_occurrence[1]=0 >= start=0. So start = 0+1 = 1. Push: path_vals=[1,1], path_dist=[0,10]. last_occurrence[1]=1. Path length = 10 - path_dist[0] = 10 - 0 = 10? Wait, start=1, so path_dist[start-1] = path_dist[0] = 0. So length = 10 - 0 = 10. nodes = 2 - 1 = 1. So path is just node 1, length 10, nodes 1. max_len becomes 10, min_nodes=1. Output [10,1]. But expected? The problem says downward path with unique values. Path 0->1 has duplicate values, so not allowed. Path 1 alone is allowed, length 10. So [10,1] is correct.

- Example 2: edges=[[1,0,8]], nums=[2,2]. Root is 0? The edges are given as undirected, but we root at 0. So adjacency: 0-1. nums[0]=2, nums[1]=2.
  - Visit 0: push, length 0, max_len=0, min_nodes=1.
  - Visit 1: value 2. last_occurrence[2]=0 >= start=0. start=1. Push: path_vals=[2,2], path_dist=[0,8]. last_occurrence[2]=1. Path length = 8 - path_dist[0] = 8. nodes = 2-1=1. max_len=8, min_nodes=1. Output [8,1]. But example says [0,1]. Wait, example 2 output is [0,1]. Let's re-read example 2: edges = [[1,0,8]], nums = [2,2]. Output: [0,1]. Explanation: The longest special paths are 0 and 1, both having a length of 0. So they consider length 0 as max? Why is path 1 length 0? Because the edge length is 8, but maybe they define length as number of edges? No, length is sum of edge lengths. Path 0->1 has length 8. But they say length 0. Why? Let's check the problem statement: "A special path is defined as a downward path from an ancestor node to a descendant node such that all the values of the nodes in that path are unique." "Return an array result of size 2, where result[0] is the length of the longest special path". In example 2, they say longest special paths are 0 and 1, both having a length of 0. But path 0->1 is not special because values are not unique (both 2). So the only special paths are single nodes 0 and 1. Each has length 0 (since no edges). So max length is 0. So my algorithm gave length 8 for path 1 alone? Wait, path 1 alone is just node 1. Its length is 0 because there are no edges. But in my calculation, I computed length as `path_dist[-1] - path_dist[start-1]`. For node 1, path_dist[-1] is the cumulative distance from root to node 1, which is 8. start=1, so path_dist[start-1] = path_dist[0] = 0. So length = 8 - 0 = 8. That's wrong because the path from start to current is just node 1, which has no edges. The cumulative distance includes the edge from root to node 1. But the path from node 1 to itself should have length 0. The issue is that `path_dist` stores distance from root, not from `start`. So `path_dist[-1] - path_dist[start-1]` gives the sum of edges from the node at `start-1` to the current node. If `start` is the index of the first node in the window, then the path is from node at `start` to current. The edges are those between consecutive nodes in the window. The distance from root to node at `start` is `path_dist[start]`. The distance from root to current is `path_dist[-1]`. So the sum of edges in the window is `path_dist[-1] - path_dist[start]`. Wait, let's think: path_dist[i] is distance from root to node i. If the window is indices start..end, then the edges are between i and i+1 for i in start..end-1. The sum is path_dist[end] - path_dist[start]. Because path_dist[start] is distance to first node, path_dist[end] is distance to last node. The difference is the sum of edges between them. So the formula should be `path_dist[-1] - path_dist[start]`. Not `path_dist[start-1]`. Let's verify with example 1: path 0->1->4. Suppose distances: root 0 dist 0. 1 dist 2. 4 dist 6. If start=0 (node 0), path length = dist[4] - dist[0] = 6 - 0 = 6. Correct. If start=1 (node 1), path length = dist[4] - dist[1] = 6 - 2 = 4. That's correct for path 1->4. So the formula is `path_dist[-1] - path_dist[start]`. Node count is `len(path_vals) - start`. So we need to adjust.

In my earlier mental test with n=2, nums=[1,1], path 1 alone: start=1, path_dist[-1]=10, path_dist[start]=path_dist[1]=10. So length = 10 - 10 = 0. Correct! So the formula is `path_dist[-1] - path_dist[start]`.

Thus the algorithm is:
- `path_dist` list, where `path_dist[i]` is distance from root to node at index i.
- When window is `start..end`, length = `path_dist[end] - path_dist[start]`.
- Node count = `end - start + 1`.

So we need to compute `path_dist` correctly. For root, `path_dist[0] = 0`. For child, `path_dist.append(path_dist[-1] + edge_length)`.

Now example 2: start=1, path_dist[1]=8, path_dist[-1]=8, length=0. Correct.

So the algorithm is correct with this formula.

**Implementation steps:**
1. Build adjacency list: `adj[u].append((v, w))`, `adj[v].append((u, w))`.
2. Initialize:
   - `path_vals = []`
   - `path_dist = []` (will start with 0 for root)
   - `last_occurrence = {}`
   - `start = 0`
   - `max_len = 0`
   - `min_nodes = 1`
3. DFS function:
   ```python
   def dfs(u, parent, curr_dist):
       nonlocal start, max_len, min_nodes
       v = nums[u]
       # Check duplicate
       if v in last_occurrence and last_occurrence[v] >= start:
           start = last_occurrence[v] + 1

## worker: Implement the DFS solution with iterative stack to
The solution uses an iterative DFS with a stack to avoid recursion depth issues. We maintain:
- `path_vals`: list of node values along the current root-to-node path
- `path_dist`: cumulative distance from root for each node in the path
- `last_occurrence`: dictionary mapping each value to its most recent index in `path_vals`
- `start`: index marking the beginning of the current valid window (where all values are unique)

When entering a node, we check if its value appeared in the current window. If so, we move `start` to just after the previous occurrence. Then we add the node to the path and update the answer. When leaving the node, we pop it from the path. This approach avoids physically removing nodes from the stack when duplicates are found, making it O(n) time and O(n) space.

The key formula: for a window from `start` to `end`, the path length is `path_dist[end] - path_dist[start]` and node count is `end - start + 1`.

## worker: Implement the iterative DFS traversal in the `long
The solution uses an iterative DFS with a stack to avoid recursion depth issues. We maintain:
- `path_vals`: list of node values along the current root-to-node path
- `path_dist`: cumulative distance from root for each node in the path (path_dist[i] is distance from root to node at index i)
- `last_occurrence`: dictionary mapping each value to its most recent index in `path_vals`
- `start`: index marking the beginning of the current valid window (where all values are unique)

When entering a node, we check if its value appeared in the current window. If so, we move `start` to just after the previous occurrence. Then we add the node to the path and update the answer. When leaving the node, we pop it from the path. This approach avoids physically removing nodes from the stack when duplicates are found, making it O(n) time and O(n) space.

The key formula: for a window from `start` to `end`, the path length is `path_dist[end] - path_dist[start]` and node count is `end - start + 1`. This correctly handles single-node paths (length 0) and paths starting at non-root nodes.
