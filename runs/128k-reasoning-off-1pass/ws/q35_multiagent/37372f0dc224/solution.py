import sys

def solve():
    s = sys.stdin.readline().strip()
    if not s:
        return
    
    n = len(s)
    # We want to find the longest palindromic suffix of s.
    # Construct T = reverse(s) + '#' + s
    # The KMP pi array for T will have at the last position the length of the
    # longest prefix of T that is also a suffix of T.
    # Prefix of T is a prefix of reverse(s), which is reverse of a suffix of s.
    # Suffix of T is a suffix of s.
    # So pi[-1] gives the length L such that reverse(s[0:L]) == s[n-L:n]
    # which implies s[n-L:n] is a palindrome.
    
    rev_s = s[::-1]
    t = rev_s + '#' + s
    
    m = len(t)
    pi = [0] * m
    
    # Compute KMP prefix function
    for i in range(1, m):
        j = pi[i-1]
        while j > 0 and t[i] != t[j]:
            j = pi[j-1]
        if t[i] == t[j]:
            j += 1
        pi[i] = j
        
    # The length of the longest palindromic suffix
    l = pi[m-1]
    
    # The part of s that is not part of the palindromic suffix
    # is s[0 : n-l]
    # We need to reverse this part and append it to s
    to_append = s[:n-l][::-1]
    
    print(s + to_append)

if __name__ == '__main__':
    solve()