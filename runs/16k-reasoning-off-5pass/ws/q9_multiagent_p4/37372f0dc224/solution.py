import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    s = input_data[0]
    
    # We need to find the shortest palindrome that has S as its prefix.
    # This is equivalent to finding the longest palindromic suffix of S.
    # Let the longest palindromic suffix be P. Then the answer is S + reverse(S[:-len(P)]).
    #
    # To find the length of the longest palindromic suffix efficiently (O(N)),
    # we can use the KMP algorithm's prefix function (pi array).
    #
    # Strategy:
    # Construct a string T = reverse(S) + '#' + S.
    # Compute the pi array for T.
    # The value pi[len(T)-1] gives the length of the longest proper prefix of T
    # that is also a suffix of T.
    #
    # Let L = pi[len(T)-1].
    # The prefix of T of length L is a prefix of reverse(S), which corresponds to
    # the reverse of the suffix of S of length L.
    # The suffix of T of length L is a suffix of S.
    # Since they match, the suffix of S of length L is equal to the reverse of itself.
    # Thus, it is a palindrome. Since L is the maximum such length found by KMP,
    # it is the longest palindromic suffix.
    
    s_rev = s[::-1]
    sep = '#'
    t = s_rev + sep + s
    
    n = len(t)
    pi = [0] * n
    
    # Compute KMP prefix function
    for i in range(1, n):
        j = pi[i-1]
        while j > 0 and t[i] != t[j]:
            j = pi[j-1]
        if t[i] == t[j]:
            j += 1
        pi[i] = j
        
    # The length of the longest palindromic suffix of S
    l = pi[-1]
    
    # The part of S that is NOT part of the palindromic suffix is the prefix of length (len(S) - l)
    # We need to append the reverse of this part to S to make it a palindrome.
    len_s = len(s)
    prefix_to_reverse = s[:len_s - l]
    suffix_to_append = prefix_to_reverse[::-1]
    
    print(s + suffix_to_append)

if __name__ == '__main__':
    solve()