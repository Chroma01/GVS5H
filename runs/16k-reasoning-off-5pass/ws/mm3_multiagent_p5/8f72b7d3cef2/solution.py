import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    
    # Each stack entry: (value, left_boundary, interval_sum)
    # The entry represents a maximal absorbable block where 'value' is the "dominant" slime
    # and the block extends from left_boundary to some right boundary (implicitly the position where this entry was pushed).
    # The interval_sum is the sum of all slimes in that block.
    stack = []
    # ans[i] will store the sum of the maximal block containing index i.
    ans = [0] * N
    
    for i, a in enumerate(A):
        cur_sum = a
        cur_left = i
        # Merge with previous blocks while the current accumulated sum is large enough
        # to absorb the top of the stack.
        while stack and stack[-1][0] <= cur_sum:
            top_val, top_left, top_sum = stack.pop()
            cur_sum += top_sum
            cur_left = top_left
        # The new block spans from cur_left to i.
        # All indices in this range belong to this block and have the same interval sum.
        block_sum = cur_sum
        # Set ans for all indices in this block
        for j in range(cur_left, i+1):
            ans[j] = block_sum
        stack.append((a, cur_left, block_sum))
    
    print(' '.join(map(str, ans)))

if __name__ == "__main__":
    solve()