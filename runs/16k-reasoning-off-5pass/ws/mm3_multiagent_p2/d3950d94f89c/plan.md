We need to find the longest downward (ancestor→descendant) path in the rooted tree such that all node values on the path are unique, and also return the minimum number of nodes among all such longest paths. The tree is given as undirected but rooted at 0. The naive O(N²) check of all paths is too slow for N up to 5·10⁴.

We will perform a DFS from the root, maintaining a sliding window of ancestors with unique values. While traversing, we keep a stack (or map) of the last occurrence position of each value along the current root→node path. When we encounter a value that already exists on the current path, we pop ancestors up to (and including) the previous occurrence, removing their values from the map. This ensures the current path from the new start to the current node has all unique values.

At each node we compute:
- the total length of the current unique‑value segment (sum of edge lengths from the first valid ancestor to the node)
- the number of nodes in that segment

We track the global maximum length and, when a new max is found, reset the minimum node count to the current segment size; when we tie the max, keep the smaller node count. This yields O(N) time and O(H) space (H = tree height).