import sys
import random

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
    """Split treap into (L, R) where L contains first k elements."""
    if not node:
        return (None, None)
    if sz(node.left) >= k:
        # Desired split is entirely in left subtree
        L, R = split(node.left, k)
        node.left = R
        update(node)
        return (L, node)
    else:
        # Split point is at or after current node
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

def inorder(node, res):
    if not node:
        return
    inorder(node.left, res)
    res.append(node.val)
    inorder(node.right, res)

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    P = [int(next(it)) for _ in range(N)]

    root = None
    for i, p in enumerate(P, start=1):
        node = Node(i)
        left, right = split(root, p)
        root = merge(merge(left, node), right)

    result = []
    inorder(root, result)
    sys.stdout.write(' '.join(map(str, result)))

if __name__ == "__main__":
    solve()