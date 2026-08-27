import sys

def solve():
    s = sys.stdin.readline().strip()
    if not s:
        return
    
    n = len(s)
    if n == 0:
        print("")
        return
        
    # We want to find the longest palindromic suffix of s.
    # Construct T = reverse(s) + '#' + s
    # The KMP prefix function (pi array) for T at the last position
    # gives the length of the longest prefix of T that is also a suffix of T.
    # Prefix of T is a prefix of reverse(s).
    # Suffix of T is a suffix of s.
    # Let this length be L.
    # Then reverse(s)[0:L] == s[n-L:n]
    # reverse(s)[0:L] is the reverse of s[n-L:n].
    # So reverse(s[n-L:n]) == s[n-L:n], which means s[n-L:n] is a palindrome.
    # And L is the maximum such length.
    
    rev_s = s[::-1]
    separator = '#'
    t = rev_s + separator + s
    
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
        
    # The length of the longest palindromic suffix of s
    l = pi[m-1]
    
    # The part of s that is not part of the palindromic suffix is s[0 : n-l]
    # We need to append the reverse of this part to s.
    to_append = s[:n-l][::-1]
    result = s + to_append
    print(result)

if __name__ == '__main__':
    solve()