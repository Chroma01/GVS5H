import sys

def prefix_function(s: str):
    """Compute the KMP prefix function (also called failure function) for string s."""
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    return pi

def solve() -> None:
    # Read the string S
    S = sys.stdin.readline().strip()
    n = len(S)
    
    # Reverse S and build the combined string: rev(S) + '#' + S
    rev = S[::-1]
    combined = rev + '#' + S
    
    # Compute the prefix function; the last value is the length of the longest
    # suffix of S that is also a palindrome (longest border between rev(S) and S).
    pi = prefix_function(combined)
    L = pi[-1]   # length of the longest palindromic suffix
    
    # Append the reverse of the prefix that is not part of that suffix
    answer = S + S[:n - L][::-1]
    sys.stdout.write(answer)

if __name__ == "__main__":
    solve()