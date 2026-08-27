import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    S = data[1].strip()
    T = data[2].strip()
    
    # Step 1: Build the mapping from S to T
    target = [-1] * 26
    for i in range(N):
        c = ord(S[i]) - ord('a')
        d = ord(T[i]) - ord('a')
        if target[c] == -1:
            target[c] = d
        elif target[c] != d:
            print(-1)
            return
    
    # Step 2: Determine which letters appear in S
    used = [False] * 26
    for ch in S:
        used[ord(ch) - ord('a')] = True
    
    # Step 3: Build the directed graph (next array)
    next_letter = [-1] * 26
    for c in range(26):
        if used[c]:
            next_letter[c] = target[c]
    
    # Step 4: Build reverse edges for undirected traversal
    rev = [[] for _ in range(26)]
    for c in range(26):
        if used[c]:
            v = next_letter[c]
            if v != -1 and used[v]:
                rev[v].append(c)
    
    # Step 5: Find connected components and compute operations
    visited = [False] * 26
    total_ops = 0
    
    for start in range(26):
        if not used[start] or visited[start]:
            continue
        
        # Collect nodes in the component via DFS
        component = []
        stack = [start]
        visited[start] = True
        while stack:
            u = stack.pop()
            component.append(u)
            v = next_letter[u]
            if v != -1 and used[v] and not visited[v]:
                visited[v] = True
                stack.append(v)
            for w in rev[u]:
                if not visited[w]:
                    visited[w] = True
                    stack.append(w)
        
        size = len(component)
        comp_set = set(component)
        
        # Check if there is a node whose target is outside the component
        has_outside = False
        for u in component:
            v = next_letter[u]
            if v == -1 or not used[v] or v not in comp_set:
                has_outside = True
                break
        
        if has_outside:
            total_ops += size
        else:
            # Check for self-loop
            has_self_loop = False
            for u in component:
                if next_letter[u] == u:
                    has_self_loop = True
                    break
            if has_self_loop:
                total_ops += size - 1
            else:
                total_ops += size + 1
    
    print(total_ops)

if __name__ == "__main__":
    main()