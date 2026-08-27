import sys

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    N = int(input_data[idx]); idx += 1
    pos = [0] * (N + 1)
    for i in range(1, N + 1):
        p = int(input_data[idx]); idx += 1
        pos[p] = i
    
    # Use a Fenwick tree (BIT) to count, for each v from 1 to N,
    # how many already-placed values (1..v-1) have original position > pos[v].
    # That count equals (v-1) - query(pos[v]-1), where query returns
    # the number of already-placed values with position <= pos[v]-1.
    # Each such smaller value will effectively "block" v and must be
    # passed over via a swap involving v; the cost contribution is v per such crossing.
    bit = [0] * (N + 2)
    def update(i, val=1):
        while i <= N:
            bit[i] += val
            i += i & (-i)
    def query(i):
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & (-i)
        return s
    
    ans = 0
    for v in range(1, N + 1):
        count_smaller_to_right = (v - 1) - query(pos[v] - 1)
        ans += v * count_smaller_to_right
        update(pos[v], 1)
    
    print(ans)

solve()