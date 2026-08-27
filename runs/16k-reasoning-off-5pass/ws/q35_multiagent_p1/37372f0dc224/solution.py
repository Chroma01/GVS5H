import sys

def solve():
    s = sys.stdin.readline().strip()
    if not s:
        return
    
    n = len(s)
    if n == 0:
        print("")
        return
        
    # Construct T = reverse(S) + '#' + S
    s_rev = s[::-1]
    t = s_rev + '#' + s
    
    # Compute prefix function (pi array) for T
    m = len(t)
    pi = [0] * m
    
    for i in range(1, m):
        j = pi[i-1]
        while j > 0 and t[i] != t[j]:
            j = pi[j-1]
        if t[i] == t[j]:
            j += 1
        pi[i] = j
        
    # The length of the longest palindromic suffix of S is pi[m-1]
    l = pi[m-1]
    
    # The part of S that is not part of the palindromic suffix is S[0 : n-l]
    # We reverse this part and append it to S
    suffix_to_add = s[:n-l][::-1]
    result = s + suffix_to_add
    print(result)

if __name__ == "__main__":
    solve()