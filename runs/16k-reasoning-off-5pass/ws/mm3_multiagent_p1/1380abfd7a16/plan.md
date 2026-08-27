We need to reconstruct the final array after a sequence of insertions into a list. For each i from 1 to N, we insert i at position P_i (1-indexed) into the current list A.

A naive approach using Python's `list.insert` would be O(N) per operation, leading to O(N^2) total — too slow for N up to 5·10^5.

We need a more efficient data structure supporting order-maintaining insert-by-index. A Fenwick tree (Binary Indexed Tree) or a balanced BST with order statistics works, but implementing a splay/treap is the standard trick. I'll use a treap (randomized BST) with implicit keys: each node stores its value, subtree size, and we maintain heap property on random priorities. Insertion at a position is a split-merge operation: split root into (left, right) at position P_i, then merge(left, new_node) then merge result with right. This is O(log N) per operation, total O(N log N). For N=5e5 this is fast.

After all insertions, we perform an in-order traversal of the treap to extract the final array and print it.

We'll also set a recursion limit high enough or use an iterative approach to avoid recursion depth issues (N up to 5e5). We can write the treap with a stack-based iterative approach, or keep recursion but set `sys.setrecursionlimit(1_000_000)`. In Python, recursion for 5e5 depth can be problematic due to function call overhead, but each insert only recurses on O(log N) depth (around ~19 for N=5e5), so recursion depth is small. However, building the treap via 5e5 calls, each with recursion, may still be slow due to Python function call overhead. We'll optimize by using loops and minimal overhead, but `sys.setrecursionlimit` for safety.

Implementation steps:
1. Read N and list P.
2. Initialize treap with root = None.
3. For each i in 1..N:
   - Create new node with value i.
   - Perform split(root, P_i) -> (left, right) where left has size P_i.
   - Set root = merge(merge(left, new_node), right).
4. Do an in-order traversal of root, collecting values into list ans.
5. Print ans with spaces.

Edge cases: P_i can be i, meaning insertion at the end; P_i can be 1, meaning at front. Both are handled correctly by the split function. Splitting by size: if node is None, return (None, None). Else, we compare size of left subtree + 1 with k.

Let’s outline functions:

```python
import sys, random
sys.setrecursionlimit(1_000_000)

class Node:
    __slots__ = ('val', 'prio', 'size', 'left', 'right')
    def __init__(self, val):
        self.val = val
        self.prio = random.randrange(1 << 30)
        self.size = 1
        self.left = None
        self.right = None

def sz(node):
    return node.size if node else 0

def update(node):
    if node:
        node.size = 1 + sz(node.left) + sz(node.right)

def split(node, k):
    # splits node into (L, R) where L has first k elements
    if not node:
        return (None, None)
    if sz(node.left) >= k:
        # desired split is in left subtree
        L, R = split(node.left, k)
        node.left = R
        update(node)
        return (L, node)
    else:
        # split point is at or after current node
        L, R = split(node.right, k - sz(node.left) - 1)
        node.right = L
        update(node)
        return (node, R)

def merge(left, right):
    if not left or not right:
        return left or right
    if left.prio > right.prio:
        left.right = merge(left.right, right)
        update(left)
        return left
    else:
        right.left = merge(left, right.left)
        update(right)
        return right
```

Then:

```python
def inorder(node, res):
    if not node:
        return
    inorder(node.left, res)
    res.append(node.val)
    inorder(node.right, res)
```

Now iterate:

```python
root = None
for i, p in enumerate(P, start=1):
    node = Node(i)
    left, right = split(root, p)
    root = merge(merge(left, node), right)
res = []
inorder(root, res)
print(' '.join(map(str, res)))
```

Complexities: each operation is expected O(log N) due to randomized treap. Total time O(N log N). Memory O(N).

Edge Cases: N=1. P_1=1 => result [1]. Works. Random seed fixed? Not needed but we can set random.seed(0) for deterministic.

The problem is straightforward: we just simulate insertions using an efficient data structure.