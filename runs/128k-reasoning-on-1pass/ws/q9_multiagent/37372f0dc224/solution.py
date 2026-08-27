import sys

def solve():
    # Read all input from standard input
    # Using read().split() handles potential surrounding whitespace/newlines robustly
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    s = input_data[0]
    n = len(s)
    
    # If s is empty (though constraints say length >= 1), handle gracefully
    if n == 0:
        print("")
        return

    s_rev = s[::-1]
    
    # We construct the string P = s_rev + '#' + s
    # The '#' is a separator not present in s (s contains only uppercase letters)
    # We compute the KMP prefix function (pi array) for P.
    # pi[i] stores the length of the longest proper prefix of P[0...i] 
    # that is also a suffix of P[0...i].
    # The value pi[len(P)-1] will give the length of the longest prefix of s_rev
    # that is also a suffix of s.
    
    separator = '#'
    p = s_rev + separator + s
    
    m = len(p)
    pi = [0] * m
    
    # Compute pi array iteratively in O(m) time
    for i in range(1, m):
        j = pi[i-1]
        while j > 0 and p[i] != p[j]:
            j = pi[j-1]
        if p[i] == p[j]:
            j += 1
        pi[i] = j
    
    # The length of the longest suffix of s that matches a prefix of s_rev
    l = pi[m-1]
    
    # The shortest palindrome is s + s_rev[l:]
    # s_rev[l:] is the part of s_rev that does not overlap with the suffix of s
    result = s + s_rev[l:]
    
    print(result)

if __name__ == '__main__':
    solve()