import sys
sys.setrecursionlimit(1 << 25)

def solve():
    import sys
    input = sys.stdin.readline

    N = int(input())
    A = [0] + list(map(int, input().split()))
    B = [0] + list(map(int, input().split()))
    K = int(input())
    queries = []
    for idx in range(K):
        x, y = map(int, input().split())
        queries.append((y, x, idx))

    # prefix sums of A and B
    SA = [0] * (N + 1)
    SB = [0] * (N + 1)
    for i in range(1, N + 1):
        SA[i] = SA[i-1] + A[i]
        SB[i] = SB[i-1] + B[i]

    # segment tree arrays (1-indexed for nodes)
    size = 4 * N + 5
    minA = [0] * size
    maxA = [0] * size
    sumA = [0] * size
    cnt = [0] * size          # sum of c_i
    sumB = [0] * size         # sum of s_i
    sumAcnt = [0] * size      # sum of A_i * c_i
    lazy_cnt = [0] * size     # pending +1 to c_i for all i in node
    lazy_sumB = [0] * size    # pending +b to s_i for all i in node

    def build(node, l, r):
        if l == r:
            v = A[l]
            minA[node] = maxA[node] = v
            sumA[node] = v
            cnt[node] = sumB[node] = sumAcnt[node] = 0
            lazy_cnt[node] = lazy_sumB[node] = 0
        else:
            mid = (l + r) // 2
            build(node * 2, l, mid)
            build(node * 2 + 1, mid + 1, r)
            minA[node] = min(minA[node * 2], minA[node * 2 + 1])
            maxA[node] = max(maxA[node * 2], maxA[node * 2 + 1])
            sumA[node] = sumA[node * 2] + sumA[node * 2 + 1]
            cnt[node] = sumB[node] = sumAcnt[node] = 0
            lazy_cnt[node] = lazy_sumB[node] = 0

    def apply(node, l, r, b):
        """Apply update to whole node: add 1 to cnt, b to sumB, sumA to sumAcnt."""
        length = r - l + 1
        cnt[node] += length
        sumB[node] += b * length
        sumAcnt[node] += sumA[node]
        lazy_cnt[node] += 1
        lazy_sumB[node] += b

    def push(node, l, r):
        """Propagate pending lazy values to children."""
        if lazy_cnt[node] == 0 and lazy_sumB[node] == 0:
            return
        if l != r:
            mid = (l + r) // 2
            left = node * 2
            right = node * 2 + 1
            left_len = mid - l + 1
            right_len = r - mid
            # left child
            cnt[left] += lazy_cnt[node] * left_len
            sumB[left] += lazy_sumB[node] * left_len
            sumAcnt[left] += sumA[left] * lazy_cnt[node]
            lazy_cnt[left] += lazy_cnt[node]
            lazy_sumB[left] += lazy_sumB[node]
            # right child
            cnt[right] += lazy_cnt[node] * right_len
            sumB[right] += lazy_sumB[node] * right_len
            sumAcnt[right] += sumA[right] * lazy_cnt[node]
            lazy_cnt[right] += lazy_cnt[node]
            lazy_sumB[right] += lazy_sumB[node]
        lazy_cnt[node] = 0
        lazy_sumB[node] = 0

    # Iterative update using explicit stack to avoid recursion overhead
    def iterative_update(b):
        """Update all indices i with A_i >= b."""
        stack = [(1, 1, N, 0)]  # (node, l, r, state); state 0 = first visit, 1 = after children
        while stack:
            node, l, r, state = stack.pop()
            if state == 0:
                if maxA[node] < b:
                    # No element in this range qualifies
                    continue
                if minA[node] >= b:
                    # Whole range qualifies
                    apply(node, l, r, b)
                    continue
                # Mixed: need to go deeper. First push current node's lazy to children.
                push(node, l, r)
                # Re-add current node for post-order recomputation
                stack.append((node, l, r, 1))
                mid = (l + r) // 2
                # Push children (order does not matter)
                stack.append((node * 2, l, mid, 0))
                stack.append((node * 2 + 1, mid + 1, r, 0))
            else:
                # Post-order: recompute aggregates from children
                cnt[node] = cnt[node * 2] + cnt[node * 2 + 1]
                sumB[node] = sumB[node * 2] + sumB[node * 2 + 1]
                sumAcnt[node] = sumAcnt[node * 2] + sumAcnt[node * 2 + 1]

    # Recursive query for prefix [1, x]
    def query(node, l, r, ql, qr):
        if ql <= l and r <= qr:
            return cnt[node], sumB[node], sumAcnt[node]
        push(node, l, r)
        mid = (l + r) // 2
        if qr <= mid:
            return query(node * 2, l, mid, ql, qr)
        elif ql > mid:
            return query(node * 2 + 1, mid + 1, r, ql, qr)
        else:
            c1, s1, sa1 = query(node * 2, l, mid, ql, qr)
            c2, s2, sa2 = query(node * 2 + 1, mid + 1, r, ql, qr)
            return c1 + c2, s1 + s2, sa1 + sa2

    # Build the segment tree
    build(1, 1, N)

    # Sort queries by Y (the prefix length of B)
    queries.sort()
    ans = [0] * K
    qi = 0
    for y in range(1, N + 1):
        # Process the new B value
        iterative_update(B[y])
        # Answer all queries with this Y
        while qi < K and queries[qi][0] == y:
            _, x, idx = queries[qi]
            c, sb, sac = query(1, 1, N, 1, x)
            SAx = SA[x]
            SBy = SB[y]
            # Formula: answer = x * SB[y] - y * SA[x] - 2*sb + 2*sac
            val = x * SBy - y * SAx - 2 * sb + 2 * sac
            ans[idx] = val
            qi += 1

    out = '\n'.join(map(str, ans))
    sys.stdout.write(out)

if __name__ == "__main__":
    solve()