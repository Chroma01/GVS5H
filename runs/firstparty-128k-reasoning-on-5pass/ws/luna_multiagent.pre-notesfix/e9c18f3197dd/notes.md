
## ideation
The core difficulty is that one element of `nums` can be incremented to a value that simultaneously covers several target entries. The cost for covering a chosen subset is the distance to the next multiple of that subset’s LCM, while every `nums` element may be used at most once. Thus, independently minimizing the cost for each target is incorrect because it can reuse the same element or miss beneficial shared coverage. The small target size, at most four, is the key exploitable constraint.

## worker: Implement the streaming subset-mask DP: compute ea
For each subset of target indices, compute its LCM. Incrementing a number to the next multiple of that LCM makes it cover every target in the subset, with minimum cost equal to the distance to that next multiple.

The DP mask records which target indices are already covered. Each `nums` element is either skipped or assigned to a subset of currently uncovered targets, ensuring that no element is reused. Since there are at most four targets, the mask DP is small; the transition count per number is at most \(3^4 = 81\).

Duplicate target values are handled correctly because target entries remain separate mask bits, while their combined LCM naturally avoids unnecessary extra increments.
