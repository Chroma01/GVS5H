import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    S = data[1].strip()
    T = data[2].strip()
    
    # target[c] = final letter that all occurrences of c in S must become
    target = [-1] * 26
    possible = True
    for i in range(N):
        sc = ord(S[i]) - ord('a')
        tc = ord(T[i]) - ord('a')
        if target[sc] == -1:
            target[sc] = tc
        elif target[sc] != tc:
            possible = False
            break
    
    if not possible:
        print(-1)
        return
    
    # DSU for 26 letters
    parent = list(range(26))
    rank = [0] * 26
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(x, y):
        x = find(x)
        y = find(y)
        if x == y:
            return
        if rank[x] < rank[y]:
            parent[x] = y
        elif rank[x] > rank[y]:
            parent[y] = x
        else:
            parent[y] = x
            rank[x] += 1
    
    # For each letter that appears in S, union it with its target letter
    for c in range(26):
        if target[c] != -1:
            union(c, target[c])
    
    # Group letters by component
    comp_letters = {}
    for c in range(26):
        if target[c] != -1:
            root = find(c)
            if root not in comp_letters:
                comp_letters[root] = []
            comp_letters[root].append(c)
    
    ans = 0
    for root, letters in comp_letters.items():
        size = len(letters)
        # Check if any letter in this component is a fixed point (target[c] == c)
        has_fixed = any(target[c] == c for c in letters)
        if has_fixed:
            ans += size
        else:
            ans += size + 1
    
    print(ans)

if __name__ == "__main__":
    solve()