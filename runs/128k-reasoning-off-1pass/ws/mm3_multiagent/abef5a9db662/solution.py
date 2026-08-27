import sys
sys.setrecursionlimit(1 << 25)

def solve():
    input = sys.stdin.readline
    N = int(input())
    intervals = []
    max_r = 0
    for _ in range(N):
        l, r = map(int, input().split())
        intervals.append((l, r))
        if r > max_r:
            max_r = r
    Q = int(input())
    queries = [int(input()) for _ in range(Q)]
    
    MAX = max_r + N + 5
    size = 1 << (MAX.bit_length())
    # Segment tree arrays
    maxv = [0] * (2 * size)
    minv = [0] * (2 * size)
    lazy = [0] * (2 * size)
    
    # Initialize leaves
    for i in range(MAX + 1):
        maxv[size + i] = i
        minv[size + i] = i
    for i in range(size - 1, 0, -1):
        maxv[i] = max(maxv[2*i], maxv[2*i+1])
        minv[i] = min(minv[2*i], minv[2*i+1])
    
    def push(node):
        if lazy[node]:
            add = lazy[node]
            left = 2*node
            right = 2*node+1
            maxv[left] += add
            minv[left] += add
            maxv[right] += add
            minv[right] += add
            lazy[left] += add
            lazy[right] += add
            lazy[node] = 0
    
    def range_add(node, l, r, ql, qr, val):
        if ql > r or qr < l:
            return
        if ql <= l and r <= qr:
            maxv[node] += val
            minv[node] += val
            lazy[node] += val
            return
        push(node)
        mid = (l + r) // 2
        range_add(2*node, l, mid, ql, qr, val)
        range_add(2*node+1, mid+1, r, ql, qr, val)
        maxv[node] = max(maxv[2*node], maxv[2*node+1])
        minv[node] = min(minv[2*node], minv[2*node+1])
    
    # Find leftmost index >= L
    def find_first_ge(node, l, r, L):
        if r < l or maxv[node] < L:
            return None
        if l == r:
            return l
        push(node)
        mid = (l + r) // 2
        left_res = find_first_ge(2*node, l, mid, L)
        if left_res is not None:
            return left_res
        return find_first_ge(2*node+1, mid+1, r, L)
    
    # Find rightmost index <= R
    def find_last_le(node, l, r, R):
        if r < l or minv[node] > R:
            return None
        if l == r:
            return l
        push(node)
        mid = (l + r) // 2
        right_res = find_last_le(2*node+1, mid+1, r, R)
        if right_res is not None:
            return right_res
        return find_last_le(2*node, l, mid, R)
    
    # Process contests
    for L, R in intervals:
        left = find_first_ge(1, 0, size-1, L)
        if left is None:
            continue
        right = find_last_le(1, 0, size-1, R)
        if right is None:
            continue
        if left > right:
            continue
        # Ensure left and right are within [0, MAX]
        if left > MAX:
            continue
        if right > MAX:
            right = MAX
        range_add(1, 0, size-1, left, right, 1)
    
    # Extract final values
    final = [0] * (MAX + 1)
    def collect(node, l, r):
        if l > MAX:
            return
        if l == r:
            final[l] = maxv[node]
            return
        push(node)
        mid = (l + r) // 2
        collect(2*node, l, mid)
        collect(2*node+1, mid+1, r)
    collect(1, 0, size-1)
    
    out = []
    for x in queries:
        out.append(str(final[x]))
    print('\n'.join(out))

if __name__ == "__main__":
    solve()