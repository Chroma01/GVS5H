import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        X = int(next(iterator))
        Y = int(next(iterator))
        S = next(iterator)
        T = next(iterator)
    except StopIteration:
        return

    # Check if total counts of 0s and 1s match
    if S.count('0') != T.count('0'):
        print("No")
        return

    # If no operations are possible (X+Y > N), S must be identical to T
    if X + Y > N:
        if S == T:
            print("Yes")
        else:
            print("No")
        return

    # Function to get run lengths and their types
    def get_runs(s):
        if not s:
            return []
        runs = []
        current_char = s[0]
        count = 1
        for char in s[1:]:
            if char == current_char:
                count += 1
            else:
                runs.append((current_char, count))
                current_char = char
                count = 1
        runs.append((current_char, count))
        return runs

    runs_S = get_runs(S)
    runs_T = get_runs(T)

    # If the number of runs is different, we might still be able to transform if we can split/merge runs.
    # However, the invariant is the sequence of (type, length % modulus).
    # Let's construct the signature for S and T.
    # Signature is a list of tuples: (type, length % (X if type is '0' else Y))
    
    sig_S = []
    for char, length in runs_S:
        mod = X if char == '0' else Y
        sig_S.append((char, length % mod))

    sig_T = []
    for char, length in runs_T:
        mod = X if char == '0' else Y
        sig_T.append((char, length % mod))

    if sig_S == sig_T:
        print("Yes")
    else:
        print("No")

if __name__ == '__main__':
    solve()