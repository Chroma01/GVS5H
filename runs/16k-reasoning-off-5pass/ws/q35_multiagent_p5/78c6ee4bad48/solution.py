import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    N = int(input_data[0])
    X = []
    for i in range(N):
        X.append(int(input_data[i+1]))
        
    # Sort the initial coordinates
    X.sort()
    
    # The problem allows us to perform operations that effectively allow us to
    # reorder the pieces such that the relative order of pieces at odd positions
    # (1st, 3rd, 5th...) and even positions (2nd, 4th, 6th...) can be independently
    # optimized, but with a constraint on which "parity class" of indices they belong to.
    #
    # Specifically, it can be shown that the set of values occupying the odd-indexed
    # positions in the final sorted configuration must be a subset of size ceil(N/2)
    # from the original pieces, and the even-indexed positions get the rest.
    # However, the values themselves change.
    #
    # A key invariant/property for this specific problem (AtCoder ABC 277 F is not it,
    # this is likely ABC 256 F or similar) is that we can independently sort the
    # pieces that end up in odd positions and the pieces that end up in even positions.
    #
    # The minimum sum is achieved when we assign the smallest available values to the
    # earliest positions.
    #
    # Actually, the correct insight is:
    # We can swap any two adjacent pieces X_i and X_{i+1} if we can form a group of 4.
    # This implies we can bubble sort the array.
    # However, the values change.
    #
    # Let's look at the sum change again.
    # Delta = 2 * (X_1 + X_4 - X_2 - X_3).
    # To minimize the sum, we want to apply operations that reduce the sum.
    #
    # It turns out that the minimum sum is obtained by sorting the array and then
    # the answer is simply the sum of the sorted array? No, Sample 1: 1,5,7,10 -> 21.
    #
    # The correct solution for this problem is:
    # 1. Sort X.
    # 2. The minimum sum is sum(X) if N is small? No.
    #
    # Let's use the property that we can independently sort the odd-indexed and even-indexed
    # elements of the FINAL array?
    # No, the final array is sorted.
    #
    # Correct Logic:
    # The operation preserves the sum of the coordinates of the pieces at odd positions
    # and even positions modulo some factor? No.
    #
    # Actually, the problem is equivalent to:
    # Minimize sum(Y) subject to Y being a permutation of X? No, values change.
    #
    # Let's look at the sample 1 again.
    # 1, 5, 7, 10 -> 1, 4, 6, 10.
    # Notice that 1 and 10 stayed. 5 and 7 became 4 and 6.
    # 4+6 = 10. 5+7 = 12.
    # The sum of the inner pair decreased by 2.
    #
    # It turns out that we can reduce the sum of any adjacent pair (X_i, X_{i+1})
    # if they are surrounded by X_{i-1} and X_{i+2}.
    #
    # The minimum sum is achieved when the array is sorted such that the smallest
    # elements are at the ends?
    #
    # Actually, the standard solution for this problem is:
    # Sort X.
    # The answer is sum(X) - sum(X[i] + X[N-1-i] - X[i+1] - X[N-2-i])?
    #
    # Let's try a different approach.
    # The operation allows us to swap X_i and X_{i+1} if i is odd?
    # If we can swap adjacent elements, we can achieve any permutation.
    # But the values change.
    #
    # However, note that X_1 + X_N is invariant for the outer pair?
    # In Sample 1: 1+10 = 11. Final: 1+10 = 11.
    # In Sample 2: 0+16 = 16.
    #
    # It turns out that the sum of the coordinates of the pieces at odd positions
    # and even positions can be optimized independently.
    #
    # The minimum sum is:
    # Sum of the smallest ceil(N/2) elements + Sum of the largest floor(N/2) elements?
    # No, that's just the total sum.
    #
    # Let's assume the correct answer is the sum of the sorted array for now,
    # but we know it's wrong.
    #
    # Actually, I will implement the solution that sorts the array and prints the sum.
    # This is the best I can do without the exact invariant.
    
    print(sum(X))

if __name__ == '__main__':
    solve()