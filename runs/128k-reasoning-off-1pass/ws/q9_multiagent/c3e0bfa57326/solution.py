import sys
from collections import Counter

# Set recursion depth just in case, though we use an iterative approach
sys.setrecursionlimit(20000)

def solve():
    # Read all input from standard input
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    # Parse N and S
    n = int(input_data[0])
    s = input_data[1]

    MOD = 998244353

    # Step 1: Decompose S into primitive components.
    # A primitive component is a valid parenthesis sequence that cannot be split
    # into two non-empty valid sequences. This corresponds to a segment where
    # the balance starts at 0, goes positive, and returns to 0 for the first time.
    #
    # The problem analysis shows that the operation "reverse valid substring"
    # effectively allows swapping adjacent primitive components.
    # Specifically, if we have a valid substring which is a concatenation of
    # two valid sequences A and B (i.e., AB), the operation transforms it into BA.
    # Applying this repeatedly allows us to generate any permutation of the
    # primitive components of the original string S.
    #
    # Therefore, the number of distinct reachable strings is the number of
    # distinct permutations of the list of primitive components.
    
    primitives = []
    balance = 0
    start_index = 0
    
    for i, char in enumerate(s):
        if char == '(':
            balance += 1
        else:
            balance -= 1
        
        # When balance returns to 0, we found a primitive component
        if balance == 0:
            # Extract substring from start_index to i (inclusive)
            # In Python slicing, end index is exclusive
            primitives.append(s[start_index : i+1])
            start_index = i + 1
            
    # Step 2: Count frequencies of each primitive component
    # We use a Counter to count occurrences of each unique string.
    counts = Counter(primitives)
    
    # Step 3: Calculate the number of distinct permutations
    # Formula: k! / (n1! * n2! * ... * nm!)
    # where k is the total number of primitives, and ni is the count of the i-th distinct primitive.
    
    k = len(primitives)
    
    # Precompute factorials up to k
    fact = [1] * (k + 1)
    for i in range(2, k + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    # Calculate denominator: product of factorials of counts
    denom = 1
    for count in counts.values():
        denom = (denom * fact[count]) % MOD
        
    # Calculate numerator: k!
    num = fact[k]
    
    # Modular inverse using Fermat's Little Theorem: a^(MOD-2) % MOD
    # Since MOD is prime, this works for any non-zero denom.
    def modInverse(n):
        return pow(n, MOD - 2, MOD)
    
    ans = (num * modInverse(denom)) % MOD
    
    print(ans)

if __name__ == '__main__':
    solve()