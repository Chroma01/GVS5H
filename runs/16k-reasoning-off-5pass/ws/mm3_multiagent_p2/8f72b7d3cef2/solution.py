import sys

def solve():
    input = sys.stdin.readline
    N = int(input())
    A = list(map(int, input().split()))
    
    # Stack-based simulation to compute the final "blocked interval" component size for each position.
    # The stack maintains a list of slimes, each represented as [size, left_index].
    # The size is the current size of the merged slime, and left_index is the
    # leftmost original index that this slime has absorbed.
    # We process the array from left to right. For each new slime A[i],
    # we attempt to merge it with the stack, simulating the optimal absorption
    # process where a larger slime absorbs its smaller neighbors.
    # The rules:
    # - If the current slime is larger than the top of the stack, it absorbs the top,
    #   so we add the top's size to the current size and pop the top.
    # - If the current slime is smaller than the top, the top absorbs the current slime.
    #   So the new top size is the sum, and we continue checking if this new top can
    #   absorb further left neighbors.
    # - If they are equal, neither can absorb the other, so we push the current slime
    #   as a new separate slime.
    # At the end, the stack contains the final slimes. Each slime in the stack
    # represents a contiguous block of original indices. The answer for all indices
    # in that block is the size of the slime.
    
    stack = []  # elements are [size, left_index]
    for i in range(N):
        cur_size = A[i]
        cur_left = i
        while True:
            if not stack:
                stack.append([cur_size, cur_left])
                break
            top_size, top_left = stack[-1]
            if cur_size > top_size:
                # Current absorbs top
                cur_size += top_size
                cur_left = top_left
                stack.pop()
                # Continue to check against the new top
            elif cur_size == top_size:
                # Equal, cannot absorb. Push as new.
                stack.append([cur_size, i])
                break
            else:
                # Top is larger, so top absorbs current.
                # We merge cur_size into the top, then try to absorb further left.
                new_size = top_size + cur_size
                new_left = top_left
                stack.pop()
                # Now we need to treat this merged slime as the new "current" and
                # continue checking against the next element in the stack.
                cur_size = new_size
                cur_left = new_left
                # Loop continues
        # end while
    # end for
    
    # Fill the answers based on the final stack.
    # The stack is in left-to-right order. Each element covers from its left_index
    # up to the next element's left_index - 1, or N-1 for the last.
    ans = [0] * N
    for k in range(len(stack)):
        size, left = stack[k]
        if k + 1 < len(stack):
            right = stack[k+1][1] - 1
        else:
            right = N - 1
        for j in range(left, right + 1):
            ans[j] = size
    
    print(' '.join(map(str, ans)))

solve()