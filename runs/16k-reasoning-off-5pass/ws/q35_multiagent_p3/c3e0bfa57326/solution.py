import sys

# Increase recursion depth just in case, though we can do iterative if needed.
sys.setrecursionlimit(10000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    S = input_data[1]
    
    MOD = 998244353
    
    # We will build the parse tree.
    # Each node will be represented by an index.
    # We'll store the children of each node as a list of child indices.
    # To handle the root, we can imagine a virtual root that contains all top-level components.
    
    # Stack will store indices of nodes currently open.
    stack = []
    
    # List of nodes. Each node is a list of its children indices.
    # We'll append new nodes as we encounter '('.
    nodes = []
    
    # We'll use a virtual root at index 0.
    # But actually, it's easier to just collect top-level components and put them in a virtual root.
    # Let's create a virtual root.
    nodes.append([]) # Node 0 is virtual root
    
    for char in S:
        if char == '(':
            # Create a new node
            new_node_idx = len(nodes)
            nodes.append([])
            stack.append(new_node_idx)
        else:
            # char == ')'
            if stack:
                # Pop the top node, which is a completed primitive sequence
                child_idx = stack.pop()
                
                # Add this child to the current top of the stack (if any)
                if stack:
                    parent_idx = stack[-1]
                    nodes[parent_idx].append(child_idx)
                else:
                    # This is a top-level component, add to virtual root
                    nodes[0].append(child_idx)
    
    # Now, nodes[0] contains all top-level components.
    # We need to assign a unique ID to each unique subtree structure to check for equality.
    # We can do this bottom-up or via DFS.
    # Since the tree is built such that children are always added before the parent is closed,
    # we can process nodes in reverse order of their index? 
    # Not necessarily, because a child might have a higher index than its parent? 
    # No, we create a new node for each '(', so children are created after parents? 
    # Wait: When we see '(', we create a node and push it. When we see ')', we pop it.
    # The children of a node are the nodes that were popped while this node was on the stack.
    # These children have indices greater than the parent? 
    # Let's trace: 
    # S = "()()"
    # i=0, '(': create node 1, stack=[0, 1] (assuming virtual root 0 was pushed initially? No, we handled virtual root separately)
    # Let's re-trace with virtual root 0.
    # S = "()()"
    # i=0, '(': new node 1, stack=[1]. nodes[1]=[]
    # i=1, ')': pop 1. stack empty. Add 1 to nodes[0]. nodes[0]=[1].
    # i=2, '(': new node 2, stack=[2]. nodes[2]=[]
    # i=3, ')': pop 2. stack empty. Add 2 to nodes[0]. nodes[0]=[1, 2].
    # So children have higher indices than their parent? 
    # In this case, 1 and 2 are children of 0. 1 < 0? No. 1 > 0. 2 > 0.
    # What about nested? S = "(())"
    # i=0, '(': new node 1, stack=[1].
    # i=1, '(': new node 2, stack=[1, 2].
    # i=2, ')': pop 2. Add 2 to nodes[1]. nodes[1]=[2].
    # i=3, ')': pop 1. Add 1 to nodes[0]. nodes[0]=[1].
    # Here, child 2 has index 2, parent 1 has index 1. 2 > 1.
    # So yes, children always have higher indices than their parents.
    # Therefore, we can process nodes in reverse order (from N down to 0) to compute their canonical IDs.
    
    # Map from tuple of children IDs to a unique integer ID.
    tuple_to_id = {}
    next_id = 0
    
    # node_ids[i] will store the canonical ID of the subtree rooted at node i.
    node_ids = [0] * len(nodes)
    
    # Process in reverse order
    for i in range(len(nodes) - 1, -1, -1):
        children = nodes[i]
        # Get the IDs of the children
        child_ids = tuple(node_ids[c] for c in children)
        
        if child_ids not in tuple_to_id:
            tuple_to_id[child_ids] = next_id
            next_id += 1
        node_ids[i] = tuple_to_id[child_ids]
        
    # Now, count the number of nodes whose children list is NOT a palindrome.
    # We need to check if the list of children IDs is a palindrome.
    # Note: We use the original children list indices, but we can just check if the sequence of node_ids is a palindrome.
    # Actually, we already have the child_ids tuple. We can check if child_ids is a palindrome.
    
    asymmetric_count = 0
    
    for i in range(len(nodes)):
        children = nodes[i]
        if len(children) <= 1:
            # A list of 0 or 1 element is always a palindrome.
            continue
        
        # Check if the sequence of child IDs is a palindrome
        # We can use the child_ids tuple we computed earlier? 
        # No, we computed it in the loop above. Let's recompute or store it.
        # Actually, we can just check the list of children indices and compare their node_ids.
        
        # Get the list of node_ids for children
        child_id_list = [node_ids[c] for c in children]
        
        # Check palindrome
        is_palindrome = True
        left = 0
        right = len(child_id_list) - 1
        while left < right:
            if child_id_list[left] != child_id_list[right]:
                is_palindrome = False
                break
            left += 1
            right -= 1
            
        if not is_palindrome:
            asymmetric_count += 1
            
    # The answer is 2^asymmetric_count % MOD
    ans = pow(2, asymmetric_count, MOD)
    print(ans)

solve()