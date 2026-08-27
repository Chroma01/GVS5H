import sys
sys.setrecursionlimit(10000)

def solve():
    MOD = 998244353
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    S = input_data[1].strip()
    # Build match array using stack
    match = [0] * N
    stack = []
    for i, c in enumerate(S):
        if c == '(':
            stack.append(i)
        else:
            j = stack.pop()
            match[i] = j
            match[j] = i
    # For each position l that is '(', find its children: the maximal valid substrings
    # strictly inside (l, match[l]).
    # We'll compute canonical ID for each node (l, r) where r = match[l].
    # We'll store the canonical ID in an array indexed by l (the start index).
    canon = [0] * N
    # Process nodes by increasing length (so children are processed before parents)
    # Actually, we need to process from shorter to longer.
    # We can iterate over l from 0 to N-1, but only for positions where S[l] == '('.
    # For each l, we find its children, but we need the children's canonical IDs.
    # Since children's intervals are strictly inside, their lengths are smaller, so if we
    # process in order of increasing l? No, we need to process in order of increasing length.
    # Easiest: collect all (l, r) pairs, sort by length, then process.
    nodes = []
    for l in range(N):
        if S[l] == '(':
            r = match[l]
            nodes.append((l, r))
    nodes.sort(key=lambda x: x[1] - x[0])  # sort by length ascending
    # Map from tuple of sorted child IDs to unique ID
    id_map = {}
    next_id = 0
    # For each node, find its children
    for l, r in nodes:
        # Find children: inside (l, r), find positions i such that S[i] == '(' and i is the start
        # of a top-level child, i.e., either i == l+1, or match[i-1] == i-1 (meaning the previous
        # char is part of a previous child, so i starts a new one).
        children_ids = []
        i = l + 1
        while i < r:
            # S[i] must be '(' because the substring (l+1, r-1) is a concatenation of valid sequences.
            # Actually, S[i] is the start of a child.
            child_l = i
            child_r = match[i]
            children_ids.append(canon[child_l])  # this will be set if child length is smaller, which it is.
            i = child_r + 1
        # Sort children IDs to get unordered canonical form
        children_ids.sort()
        key = tuple(children_ids)
        if key not in id_map:
            id_map[key] = next_id
            next_id += 1
        canon[l] = id_map[key]
    # Now we have canonical IDs for all nodes.
    # Count nodes with two children having different canonical IDs.
    # A node corresponds to (l, r). It has children as found above.
    # The number of distinct strings is 2^{#nodes where children_ids has size 2 and the two are distinct}.
    # Actually, if a node has 0 or 1 child, swapping does nothing (or is not applicable).
    # If it has 2 children and they are isomorphic, swapping yields the same string.
    # If they are non-isomorphic, swapping yields a new string, and this choice is independent.
    # So we count nodes with exactly 2 children and the two children's IDs are different.
    count = 0
    for l, r in nodes:
        # find children again
        children_ids = []
        i = l + 1
        while i < r:
            child_l = i
            child_r = match[i]
            children_ids.append(canon[child_l])
            i = child_r + 1
        if len(children_ids) == 2 and children_ids[0] != children_ids[1]:
            count += 1
    ans = pow(2, count, MOD)
    print(ans)

if __name__ == "__main__":
    solve()