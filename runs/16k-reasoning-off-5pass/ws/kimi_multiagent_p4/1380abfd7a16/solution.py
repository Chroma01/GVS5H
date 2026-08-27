import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    P = list(map(int, data[1:1+n]))
    
    # Fenwick tree for available slots
    tree = [0] * (n + 1)
    
    def update(i, delta):
        while i <= n:
            tree[i] += delta
            i += i & -i
    
    # Initialize all slots as available
    for i in range(1, n + 1):
        update(i, 1)
    
    # Find k-th available slot (1-indexed)
    def find_kth(k):
        idx = 0
        bitmask = 1 << (n.bit_length() - 1)
        while bitmask:
            t = idx + bitmask
            if t <= n and tree[t] < k:
                idx = t
                k -= tree[t]
            bitmask >>= 1
        return idx + 1
    
    ans = [0] * (n + 1)
    for i in range(n, 0, -1):
        pos = find_kth(P[i-1])
        ans[pos] = i
        update(pos, -1)
    
    sys.stdout.write(' '.join(map(str, ans[1:])) + '\n')

if __name__ == '__main__':
    main()