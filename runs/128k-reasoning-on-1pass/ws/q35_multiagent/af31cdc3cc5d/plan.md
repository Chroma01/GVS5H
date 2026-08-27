1. Parse the input sequence and separate elements into two lists based on their original index parity (even-indexed vs odd-indexed).
2. Sort both lists in ascending order. The optimal strategy to maximize the sum of absolute differences is to pair the smallest elements of one list with the largest of the other.
3. If the lists have equal length, directly pair `O[i]` with `E[len-1-i]` and sum the absolute differences.
4. If one list is longer by exactly one element, compute prefix and suffix sums to efficiently determine which element to discard from the larger list to maximize the total score.
5. Print the computed maximum score.