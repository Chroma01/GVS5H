import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    X = int(input_data[1])
    Y = int(input_data[2])
    S = input_data[3]
    T = input_data[4]
    
    # Check if total number of 1s is the same
    if S.count('1') != T.count('1'):
        print("No")
        return

    def compress(s):
        if not s:
            return []
        blocks = []
        current_char = s[0]
        count = 1
        for i in range(1, len(s)):
            if s[i] == current_char:
                count += 1
            else:
                blocks.append((current_char, count))
                current_char = s[i]
                count = 1
        blocks.append((current_char, count))
        return blocks

    def canonical(blocks, X, Y):
        # We will use a stack to process blocks
        # Each element in stack is [char, count]
        stack = []
        
        for char, count in blocks:
            # Push current block
            stack.append([char, count])
            
            # While we can perform swaps between top two blocks
            # Swap condition: top is '0' block, second top is '1' block
            # We want to move 1s to the left and 0s to the right
            # So we look for pattern: ... 1s, 0s ... and swap to ... 0s, 1s ...?
            # Wait, the operation swaps 0^X 1^Y to 1^Y 0^X.
            # This means a block of 0s followed by a block of 1s can be partially swapped.
            # The 1s move left, 0s move right.
            # So if we have stack: [..., (1, c1), (0, c0)], we can't swap directly.
            # We need (0, c0) followed by (1, c1) in the string, which means in stack:
            # stack[-2] is 0, stack[-1] is 1.
            
            while len(stack) >= 2:
                c1, cnt1 = stack[-2]
                c2, cnt2 = stack[-1]
                
                # Check if we have 0s followed by 1s
                if c1 == '0' and c2 == '1':
                    # Number of swaps we can perform
                    k = min(cnt1 // X, cnt2 // Y)
                    if k > 0:
                        # Reduce the blocks
                        stack[-2][1] -= k * X
                        stack[-1][1] -= k * Y
                        
                        # The k*Y ones move to the left, merging with previous 1s if any
                        # The k*X zeros move to the right, merging with next 0s if any
                        
                        # Remove empty blocks from top
                        if stack[-1][1] == 0:
                            stack.pop()
                        if stack[-2][1] == 0:
                            stack.pop()
                            
                        # After popping, we might have created new adjacent blocks
                        # that can be merged. But more importantly, the moved ones
                        # might merge with a block to the left of the 0s block.
                        # And the moved zeros might merge with a block to the right of the 1s block.
                        
                        # However, since we are processing left to right, the "right" part
                        # will be handled when we push the next block.
                        # The "left" part: the ones that moved left should merge with stack[-2] if it exists and is '1'.
                        
                        # Let's re-check the stack state
                        if len(stack) >= 2:
                            c_prev, cnt_prev = stack[-2]
                            c_curr, cnt_curr = stack[-1]
                            if c_prev == c_curr:
                                stack[-2][1] += stack[-1][1]
                                stack.pop()
                    else:
                        break
                else:
                    break
            
            # After pushing and swapping, merge with previous block if same char
            if len(stack) >= 2:
                c_prev, cnt_prev = stack[-2]
                c_curr, cnt_curr = stack[-1]
                if c_prev == c_curr:
                    stack[-2][1] += stack[-1][1]
                    stack.pop()
                    
        return stack

    blocks_S = compress(S)
    blocks_T = compress(T)
    
    canon_S = canonical(blocks_S, X, Y)
    canon_T = canonical(blocks_T, X, Y)
    
    if canon_S == canon_T:
        print("Yes")
    else:
        print("No")

solve()