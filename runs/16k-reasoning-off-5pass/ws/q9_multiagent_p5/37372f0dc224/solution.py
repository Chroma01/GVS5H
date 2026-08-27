import sys

# Increase recursion depth just in case, though we use iterative KMP
sys.setrecursionlimit(2000)

def compute_pi(P):
    """
    Computes the KMP failure function (pi array) for pattern P.
    pi[i] is the length of the longest proper prefix of P[0..i] 
    that is also a suffix of P[0..i].
    """
    m = len(P)
    pi = [0] * m
    k = 0
    for q in range(1, m):
        while k > 0 and P[k] != P[q]:
            k = pi[k-1]
        if P[k] == P[q]:
            k += 1
        pi[q] = k
    return pi

def solve():
    # Read input from stdin
    s = sys.stdin.readline().strip()
    
    # Handle empty input case if necessary, though constraints say length >= 1
    if not s:
        return
    
    # Construct the string T = S + '#' + reverse(S)
    # '#' is a separator not present in uppercase English letters (A-Z)
    rev_s = s[::-1]
    t = s + '#' + rev_s
    
    # Compute the pi array for T
    pi = compute_pi(t)
    
    # The length of the longest suffix of S that is a prefix of reverse(S)
    # is given by the last value in the pi array.
    l = pi[-1]
    
    # The part of reverse(S) that needs to be appended to S to make it a palindrome
    # is the part of reverse(S) starting from index l.
    suffix_to_append = rev_s[l:]
    result = s + suffix_to_append
    
    # Print the result to stdout
    print(result)

if __name__ == '__main__':
    solve()