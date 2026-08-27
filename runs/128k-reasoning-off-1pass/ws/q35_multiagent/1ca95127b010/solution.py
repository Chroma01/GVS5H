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
    
    # If the total number of 1s is different, it's impossible.
    if S.count('1') != T.count('1'):
        print("No")
        return

    # We will reduce both S and T to a canonical form.
    # The reduction rule is:
    # If the string ends with 0^X 1^Y, replace with 1^Y 0^X.
    # If the string ends with 1^Y 0^X, replace with 0^X 1^Y.
    # We repeat this until no more replacements are possible.
    # Since N is up to 5*10^5, we need an efficient stack-based approach.
    
    def reduce_string(s, x, y):
        stack = []
        # We'll store the stack as a list of characters for simplicity.
        # To optimize, we can store runs, but given the constraints and nature of operations,
        # a character-by-character stack with checks might be slow if we do string slicing.
        # However, we can check the end of the stack efficiently.
        
        # Let's use a list of characters.
        # To avoid O(N) slicing, we can check the last X+Y characters.
        
        for char in s:
            stack.append(char)
            
            # Check if we can apply the reduction at the end
            # We need to check if the last X chars are '0' and the Y chars before them are '1'
            # OR if the last Y chars are '1' and the X chars before them are '0'
            
            if len(stack) >= x + y:
                # Check for 0^X 1^Y at the end
                # stack[-x:] should be '0'*x
                # stack[-x-y:-x] should be '1'*y
                
                # Optimization: check the last character first
                if stack[-1] == '0' and stack[-x] == '0':
                    # Check if all last x are '0'
                    all_zeros = True
                    for k in range(x):
                        if stack[-1-k] != '0':
                            all_zeros = False
                            break
                    if all_zeros:
                        # Check if all y before are '1'
                        all_ones = True
                        for k in range(y):
                            if stack[-x-1-k] != '1':
                                all_ones = False
                                break
                        if all_ones:
                            # Replace 0^X 1^Y with 1^Y 0^X
                            # Remove last x+y chars
                            del stack[-x-y:]
                            # Append 1^Y 0^X
                            stack.extend(['1'] * y)
                            stack.extend(['0'] * x)
                            # Continue to check again from the new end
                            # We can use a while loop or just let the next iteration handle it?
                            # No, we need to check again because the new end might form a pattern.
                            # So we should not break, but continue the for loop?
                            # Actually, we should re-check the end.
                            # Let's use a while loop for the stack processing.
                            pass
                
                # Check for 1^Y 0^X at the end
                elif stack[-1] == '1' and stack[-y] == '1':
                    # Check if all last y are '1'
                    all_ones = True
                    for k in range(y):
                        if stack[-1-k] != '1':
                            all_ones = False
                            break
                    if all_ones:
                        # Check if all x before are '0'
                        all_zeros = True
                        for k in range(x):
                            if stack[-y-1-k] != '0':
                                all_zeros = False
                                break
                        if all_zeros:
                            # Replace 1^Y 0^X with 0^X 1^Y
                            del stack[-x-y:]
                            stack.extend(['0'] * x)
                            stack.extend(['1'] * y)

        return stack

    # The above approach with nested loops for checking might be O(N*(X+Y)) in worst case.
    # We need a more efficient way.
    # Let's use a stack that stores tuples (char, count) to represent runs.
    
    def reduce_string_optimized(s, x, y):
        # Stack stores (char, count)
        stack = []
        
        for char in s:
            if stack and stack[-1][0] == char:
                stack[-1] = (char, stack[-1][1] + 1)
            else:
                stack.append((char, 1))
            
            # Check if we can reduce at the end
            # We need to check if the last two runs can be merged/reduced
            # The pattern is either 0^X 1^Y or 1^Y 0^X
            # This means we need at least two runs at the end.
            
            while len(stack) >= 2:
                c2, n2 = stack[-1]
                c1, n1 = stack[-2]
                
                # Check for 0^X 1^Y
                # c1 should be '0', c2 should be '1'
                # We need at least X zeros and Y ones
                if c1 == '0' and c2 == '1':
                    if n1 >= x and n2 >= y:
                        # We can swap X zeros and Y ones
                        # This means we remove X from n1 and Y from n2
                        # And add Y ones and X zeros in reverse order?
                        # No, the operation swaps 0^X 1^Y with 1^Y 0^X.
                        # So we replace the last X zeros and Y ones with Y ones and X zeros.
                        # But they are adjacent runs.
                        # So we reduce n1 by X, n2 by Y.
                        # Then we add a run of Y ones, then a run of X zeros.
                        # But wait, the new ones might merge with the run before c1?
                        # No, the new ones are at the position of the old zeros.
                        # The new zeros are at the position of the old ones.
                        
                        # Let's update the stack
                        stack[-2] = (c1, n1 - x)
                        stack[-1] = (c2, n2 - y)
                        
                        # If n1 - x > 0, we keep the run of zeros
                        # If n2 - y > 0, we keep the run of ones
                        
                        # Now we need to add the swapped part: Y ones followed by X zeros
                        # But these might merge with existing runs.
                        
                        # First, add Y ones
                        # Check if the new top (if n2-y > 0) is '1', then merge
                        # Or if the stack is empty or top is not '1', add new run
                        
                        # Let's handle the remaining parts
                        if stack[-1][1] > 0:
                            # Keep the remaining ones
                            pass
                        else:
                            stack.pop()
                            
                        if stack[-2][1] > 0:
                            # Keep the remaining zeros
                            pass
                        else:
                            stack.pop()
                            
                        # Now add Y ones
                        if stack and stack[-1][0] == '1':
                            stack[-1] = ('1', stack[-1][1] + y)
                        else:
                            stack.append(('1', y))
                            
                        # Now add X zeros
                        if stack and stack[-1][0] == '0':
                            stack[-1] = ('0', stack[-1][1] + x)
                        else:
                            stack.append(('0', x))
                            
                        # Continue checking
                        continue
                    else:
                        break
                # Check for 1^Y 0^X
                elif c1 == '1' and c2 == '0':
                    if n1 >= y and n2 >= x:
                        # Swap Y ones and X zeros
                        stack[-2] = (c1, n1 - y)
                        stack[-1] = (c2, n2 - x)
                        
                        if stack[-1][1] > 0:
                            pass
                        else:
                            stack.pop()
                            
                        if stack[-2][1] > 0:
                            pass
                        else:
                            stack.pop()
                            
                        # Add X zeros
                        if stack and stack[-1][0] == '0':
                            stack[-1] = ('0', stack[-1][1] + x)
                        else:
                            stack.append(('0', x))
                            
                        # Add Y ones
                        if stack and stack[-1][0] == '1':
                            stack[-1] = ('1', stack[-1][1] + y)
                        else:
                            stack.append(('1', y))
                            
                        continue
                    else:
                        break
                else:
                    break
                    
        return stack

    # Convert stack to string for comparison
    def stack_to_str(stack):
        res = []
        for char, count in stack:
            res.append(char * count)
        return ''.join(res)

    redS = reduce_string_optimized(S, X, Y)
    redT = reduce_string_optimized(T, X, Y)
    
    if stack_to_str(redS) == stack_to_str(redT):
        print("Yes")
    else:
        print("No")

solve()