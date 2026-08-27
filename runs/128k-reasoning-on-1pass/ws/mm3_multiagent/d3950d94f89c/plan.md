**Solution Explanation**

For every node we need the longest *downward* path (ancestor → … → node) that

* uses only the values of the visited nodes,
* contains no value twice.

The length of a path is the sum of the edge lengths, not the number of nodes.
Among all such paths we need

* `maxLen` – the maximum possible length,
* `minCnt` – the smallest number of nodes among the paths whose length is
  `maxLen`.

The tree is rooted at node `0`.



--------------------------------------------------------------------

#### 1.   Observations

* While we walk from the root to a node `v` we always know the whole
  ancestor → `v` path – it is exactly the current recursion stack.
* On this linear path the condition *“all values are different”* is the
  same as the classic “longest sub‑array with distinct elements”.
  The usual sliding‑window technique can be used:
  when a value appears again we have to cut the left border of the
  window to the position **after** the previous occurrence.
* The *longest* special path that ends in the current node is obtained
  by cutting as little as possible – i.e. by moving the left border only
  when a duplicate forces us to.
  Consequently the left border is the smallest index `L` such that
  `nums[L … curDepth]` are pairwise different.
* If we know the depth `L` we also know the distance to that node,
  therefore the length of the best path ending in `curDepth` is  

  `curDist – dist[L]`.

* While walking downwards we only need three pieces of information

  * `curDist` – distance from the root to the current node,
  * `curDepth` – number of edges from the root,
  * for every value the **last depth** where it appeared on the current
    path (`lastPos[value] = depth`).

  The left border `L` is stored in a single integer `startDepth`.
  When a duplicate of the current value is seen we increase `startDepth`
  to `max(startDepth, lastPos[value] + 1)`.

* The path length for the current node is

```
len  = curDist - dist[ startDepth ]
cnt  = curDepth - startDepth + 1          (number of nodes)
```

* The global answer is updated with the usual
  “better length, or same length but fewer nodes”.

All operations are `O(1)`.  
Every node is pushed and popped exactly once – overall `O(n)` time and
`O(n)` memory.



--------------------------------------------------------------------

#### 2.   Algorithm
```
build adjacency list of the undirected tree
depthDist[depth]   // distance from root to the node that is at this depth
lastPos[value]     // most recent depth of this value on the current path
startDepth = 0
bestLen   = -1
bestCnt   = n+1

DFS(v, parent, curDist, curDepth):
    val = nums[v]

    # ----- handle the duplicate, if any -----
    prevDepth = lastPos.get(val, -1)          # -1 → value not seen yet
    oldStart  = startDepth
    if prevDepth != -1:                       # duplicate exists
        startDepth = max(startDepth, prevDepth + 1)

    # ----- put current node into the structures -----
    lastPos[val] = curDepth
    depthDist[curDepth] = curDist

    # ----- longest special path that ends here -----
    candLen = curDist - depthDist[startDepth]
    candCnt = curDepth - startDepth + 1
    if candLen > bestLen or (candLen == bestLen and candCnt < bestCnt):
        bestLen = candLen
        bestCnt = candCnt

    # ----- recurse to children -----
    for (to, w) in adj[v]:
        if to == parent: continue
        DFS(to, v, curDist + w, curDepth + 1)

    # ----- backtrack : restore previous state -----
    startDepth = oldStart
    if prevDepth == -1:
        del lastPos[val]
    else:
        lastPos[val] = prevDepth
```

Call `DFS(0, -1, 0, 0)`.  
Return `[bestLen, bestCnt]`.



--------------------------------------------------------------------

#### 3.   Correctness Proof  

We prove that the algorithm returns the required pair
`(maximum length, minimum number of nodes among all maximum‑length paths)`.

---

##### Lemma 1  
During the execution of `DFS(v, …)` the variables satisfy

* `startDepth` is the smallest index `L` such that all values in the
  current root‑to‑`v` path with depths `L … curDepth` are pairwise different.

* `lastPos[value]` equals the **largest** depth of a node with that value
  among the nodes with depth `≤ curDepth` (i.e. the most recent occurrence).

* `depthDist[d]` equals the total length from the root to the node that
  currently has depth `d`.

**Proof.**  
Induction over the recursion depth.

*Base* – before the first call (`v = 0`):
`startDepth = 0`, no value has been seen, `lastPos` is empty,
`depthDist[0] = 0`.  
All statements are true.

*Induction step* – assume the statements hold for the current call.
When we enter a child `to` with value `val = nums[to]`

* If `val` has not been seen (`prevDepth = -1`) we do not move
  `startDepth`. The new path contains only the new value,
  therefore the smallest possible left border is unchanged → `startDepth`
  stays the smallest valid index.

* If `val` has been seen at depth `prevDepth` then any valid window must
  start **after** that previous occurrence, i.e. at depth
  `prevDepth+1`.  
  `startDepth = max(startDepth, prevDepth+1)` becomes the smallest index
  that fulfills all distinctness requirements, because any index `< startDepth`
  would either be `< prevDepth+1` (contains the duplicate) or be
  `< old startDepth` (already excluded earlier).

* In both cases we store `lastPos[val] = curDepth`.  
  No other node with the same value is deeper, therefore the stored depth
  is the most recent one.

* `depthDist[curDepth] = curDist` obviously stores the correct distance.

Thus the three statements are preserved for the child call.
The back‑tracking step restores `startDepth` and `lastPos` to the values
they had before the child was processed, which are exactly the
induction hypothesis for the caller. ∎



##### Lemma 2  
For the current node `v` (depth `d = curDepth`) the algorithm computes

* `candLen = curDist - depthDist[startDepth]` – the maximum possible length
  of a special path that ends in `v`.

* `candCnt = d - startDepth + 1` – the number of nodes of that path.

**Proof.**  
By Lemma&nbsp;1 the nodes with depths `startDepth … d` are pairwise
different, therefore the path that starts at depth `startDepth` and ends
at `v` is a valid special path.
Its length is the sum of edge lengths along the path, i.e.
`curDist - depthDist[startDepth]`.  
All other valid paths ending in `v` must start at some index `L ≥ startDepth`
(because `startDepth` is already the smallest possible).  
Since the distance from the root is monotone in the depth,
any later start would give a *shorter* length.
Hence the computed `candLen` is the maximum possible.
The number of nodes on that path is `d - startDepth + 1`. ∎



##### Lemma 3  
During the whole execution `bestLen` equals the length of the longest
special path discovered so far, and `bestCnt` is the smallest node count
among all discovered special paths whose length equals `bestLen`.

**Proof.**  
Initially `bestLen = -1` (no path) and `bestCnt = n+1`.  
When a node is processed we compute `candLen, candCnt` (Lemma&nbsp;2) and
update the pair exactly as the definition requires:

* if the new path is longer, it becomes the new best,
* if it has the same length but fewer nodes, it replaces the previous
  one.

No other assignments to `bestLen, bestCnt` occur.
Therefore after processing each node the invariant holds. ∎



##### Lemma 4  
After the complete DFS finishes, `bestLen` is the length of the longest
special path in the whole tree and `bestCnt` is the minimum number of
nodes among all longest special paths.

**Proof.**  
Every node of the tree is visited exactly once, and for each visited
node the algorithm evaluates the best special path that ends there
(Lemma&nbsp;2).  
Every special path in the tree ends at some node, consequently its
length and node count are examined at the moment that endpoint is
processed.  
By Lemma&nbsp;3 after the last node has been processed `bestLen` and
`bestCnt` are respectively the maximum length and the smallest node
count among **all** special paths. ∎



##### Theorem  
`longestSpecialPath` returns an array `[L, K]` where

* `L` is the maximum possible length of a special downward path,
* `K` is the minimum number of nodes among all special paths whose
  length equals `L`.

**Proof.**  
The algorithm builds the rooted tree, runs the DFS described above and
finally returns `[bestLen, bestCnt]`.  
By Lemma&nbsp;4 `bestLen` is the required maximum length and `bestCnt`
the required minimum node count. ∎



--------------------------------------------------------------------

#### 4.   Complexity Analysis  

*Building the adjacency list* – `O(n)` time, `O(n)` memory.  

*DFS* – each node is entered and left once, every operation inside the
function is `O(1)`.  
Total time `O(n)`, additional memory:

* adjacency list – `2·(n‑1)` edges,
* `depthDist` – `n` integers,
* dictionary `lastPos` – at most `n` entries,
* recursion stack – at most the height of the tree (`≤ n`).

Overall `O(n)` time and `O(n)` extra memory.



--------------------------------------------------------------------

#### 5.   Reference Implementation  (Python 3)

```python
import sys
from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        """
        Returns [maximum length, minimum number of nodes] among all special
        downward paths in the tree rooted at 0.
        """
        n = len(nums)
        # ---------- build adjacency list ----------
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        sys.setrecursionlimit(1_000_000)          # safe for n = 5·10^4

        # ---------- data structures ----------
        depth_dist = [0] * n          # distance from root to the node at a given depth
        last_pos = {}                 # value -> most recent depth on current path
        start_depth = 0               # left border of the current distinct‑value window

        best_len = -1
        best_cnt = n + 1

        # ---------- depth‑first search ----------
        def dfs(v: int, parent: int, cur_dist: int, cur_depth: int) -> None:
            nonlocal best_len, best_cnt, start_depth

            val = nums[v]

            # ----- handle duplicate (if any) -----
            prev_depth = last_pos.get(val, -1)          # -1 → not seen before
            old_start = start_depth
            if prev_depth != -1:
                # window must start after the previous occurrence
                if prev_depth + 1 > start_depth:
                    start_depth = prev_depth + 1

            # ----- insert current node -----
            last_pos[val] = cur_depth
            depth_dist[cur_depth] = cur_dist

            # ----- candidate best path ending here -----
            cand_len = cur_dist - depth_dist[start_depth]
            cand_cnt = cur_depth - start_depth + 1
            if cand_len > best_len or (cand_len == best_len and cand_cnt < best_cnt):
                best_len = cand_len
                best_cnt = cand_cnt

            # ----- recurse to children -----
            for to, w in adj[v]:
                if to == parent:
                    continue
                dfs(to, v, cur_dist + w, cur_depth + 1)

            # ----- backtrack : restore previous state -----
            start_depth = old_start
            if prev_depth == -1:
                del last_pos[val]
            else:
                last_pos[val] = prev_depth

        # start from the root
        dfs(0, -1, 0, 0)

        return [best_len, best_cnt]
```

The program follows exactly the algorithm proven correct above
and conforms to the required `O(n)` time and memory limits.