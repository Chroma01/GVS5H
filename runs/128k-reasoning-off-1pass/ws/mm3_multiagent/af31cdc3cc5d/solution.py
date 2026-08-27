import sys
import random
import heapq

def main():
    input = sys.stdin.readline
    N = int(input())
    A = list(map(int, input().split()))
    if N == 1:
        print(0)
        return

    sys.setrecursionlimit(1 << 25)

    # Treap node for order statistics (maintain current alive indices)
    class Node:
        __slots__ = ('key', 'prio', 'left', 'right', 'size')
        def __init__(self, key):
            self.key = key
            self.prio = random.random()
            self.left = None
            self.right = None
            self.size = 1

    def get_size(node):
        return node.size if node else 0

    def update(node):
        if node:
            node.size = 1 + get_size(node.left) + get_size(node.right)
        return node

    def merge(a, b):
        if not a or not b:
            return a or b
        if a.prio < b.prio:
            a.right = merge(a.right, b)
            update(a)
            return a
        else:
            b.left = merge(a, b.left)
            update(b)
            return b

    def erase(node, key):
        if not node:
            return None
        if key == node.key:
            return merge(node.left, node.right)
        elif key < node.key:
            node.left = erase(node.left, key)
            update(node)
            return node
        else:
            node.right = erase(node.right, key)
            update(node)
            return node

    def rank(node, key):
        if not node:
            return 0
        left_size = get_size(node.left)
        if key == node.key:
            return left_size + 1
        elif key < node.key:
            return rank(node.left, key)
        else:
            return left_size + 1 + rank(node.right, key)

    # Doubly linked list of current elements (by original index)
    left = [i - 1 for i in range(N)]
    right = [i + 1 for i in range(N)]
    right[N-1] = -1
    alive = [True] * N

    # Build treap with all indices
    root = None
    for i in range(N):
        root = merge(root, Node(i))

    heap = []
    total = 0

    def get_median_rank():
        sz = get_size(root)
        if sz == 0:
            return None
        return (sz + 1) // 2

    # Initialize heap with all adjacent pairs
    med_rank = get_median_rank()
    for i in range(N - 1):
        diff = abs(A[i] - A[i+1])
        r1 = rank(root, i)
        dist = abs(r1 - med_rank)
        heapq.heappush(heap, (-diff, dist, i))

    while heap:
        neg_diff, dist, i = heapq.heappop(heap)
        if not alive[i] or not alive[i+1]:
            continue
        if right[i] != i+1:
            continue
        diff = -neg_diff
        total += diff

        # Remove i and i+1 from treap
        root = erase(root, i)
        root = erase(root, i+1)
        alive[i] = False
        alive[i+1] = False

        # Update linked list
        l = left[i]
        r = right[i+1]
        if l != -1:
            right[l] = r
        if r != -1:
            left[r] = l

        # Update median rank
        med_rank = get_median_rank()

        # If new pair formed, push it
        if l != -1 and r != -1:
            diff_new = abs(A[l] - A[r])
            rl = rank(root, l)
            dist_new = abs(rl - med_rank) if med_rank is not None else 0
            heapq.heappush(heap, (-diff_new, dist_new, l))

    print(total)

main()