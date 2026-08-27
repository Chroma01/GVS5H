import sys

def solve():
    s = sys.stdin.readline().strip()
    if not s:
        return
    
    n = len(s)
    if n == 0:
        print("")
        return
    
    # Construct T = s + '#' + reverse(s)
    rev_s = s[::-1]
    t = s + '#' + rev_s
    m = len(t)
    
    # Compute KMP failure function (pi array)
    pi = [0] * m
    k = 0
    for q in range(1, m):
        while k > 0 and t[k] != t[q]:
            k = pi[k-1]
        if t[k] == t[q]:
            k += 1
        pi[q] = k
    
    # The length of the longest palindromic suffix of s is pi[m-1]
    longest_pal_suffix_len = pi[m-1]
    
    # The part of s that needs to be reversed and appended is s[0:n-longest_pal_suffix_len]
    prefix_to_append = s[:n - longest_pal_suffix_len]
    result = s + prefix_to_append[::-1]
    
    print(result)

if __name__ == "__main__":
    solve()