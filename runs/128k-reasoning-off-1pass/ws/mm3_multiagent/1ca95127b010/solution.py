import sys

def reduce_to_normal(s, X, Y):
    if not s:
        return []
    # Parse into runs
    runs = []
    cur_char = s[0]
    cur_len = 1
    for c in s[1:]:
        if c == cur_char:
            cur_len += 1
        else:
            runs.append((cur_char, cur_len))
            cur_char = c
            cur_len = 1
    runs.append((cur_char, cur_len))
    
    n = len(s)
    max_nodes = 4 * n + 10
    typ = [0] * max_nodes
    ln = [0] * max_nodes
    nxt = [0] * max_nodes
    prv = [0] * max_nodes
    
    head = 0
    tail = 1
    typ[head] = -1
    typ[tail] = -2
    nxt[head] = tail
    prv[tail] = head
    node_count = 2
    
    def new_node(t, l):
        nonlocal node_count
        typ[node_count] = t
        ln[node_count] = l
        node_count += 1
        return node_count - 1
    
    # Build initial list
    last = head
    for t, l in runs:
        new = new_node(t, l)
        nxt[last] = new
        prv[new] = last
        last = new
    nxt[last] = tail
    prv[tail] = last
    
    cur = nxt[head]
    while True:
        # Find pattern: cur is zero-run with length >= X, and nxt[cur] is one-run with length >= Y
        found = False
        while cur != tail:
            if typ[cur] == 0 and ln[cur] >= X:
                nxt_node = nxt[cur]
                if nxt_node != tail and typ[nxt_node] == 1 and ln[nxt_node] >= Y:
                    found = True
                    break
            cur = nxt[cur]
        if not found:
            break
        
        # Apply operation at cur
        L = ln[cur]
        R = ln[nxt_node]
        prev_node = prv[cur]
        aft_node = nxt[nxt_node]
        
        # Build the segment runs (the affected region)
        seg = []
        if prev_node != head:
            seg.append((typ[prev_node], ln[prev_node]))
        if L - X > 0:
            seg.append((0, L - X))
        seg.append((1, Y))
        seg.append((0, X))
        if R - Y > 0:
            seg.append((1, R - Y))
        if aft_node != tail:
            seg.append((typ[aft_node], ln[aft_node]))
        
        # Merge adjacent same types
        merged = []
        for t, l in seg:
            if merged and merged[-1][0] == t:
                merged[-1] = (t, merged[-1][1] + l)
            else:
                merged.append((t, l))
        
        # Remove all nodes between prev_node and aft_node
        nxt[prev_node] = aft_node
        prv[aft_node] = prev_node
        
        # Insert the merged runs after prev_node
        last_node = prev_node
        for t, l in merged:
            new = new_node(t, l)
            nxt[last_node] = new
            prv[new] = last_node
            last_node = new
        nxt[last_node] = aft_node
        prv[aft_node] = last_node
        
        # Set cur to the first node of the inserted segment (or aft_node if merged is empty)
        if merged:
            cur = nxt[prev_node]
        else:
            cur = aft_node
    
    # Collect final runs
    result = []
    cur = nxt[head]
    while cur != tail:
        result.append((typ[cur], ln[cur]))
        cur = nxt[cur]
    return result

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    X = int(data[1])
    Y = int(data[2])
    S = data[3].strip()
    T = data[4].strip()
    
    # Quick check: counts of 0s and 1s must match
    if S.count('0') != T.count('0') or S.count('1') != T.count('1'):
        print("No")
        return
    
    # Reduce both strings to their normal form
    norm_S = reduce_to_normal(S, X, Y)
    norm_T = reduce_to_normal(T, X, Y)
    
    if norm_S == norm_T:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()