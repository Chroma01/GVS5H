
## ideation


## worker: (none)
The problem asks for the number of valid paths in a grid with a forbidden rectangular region.
We used complementary counting: Total paths in the full grid minus paths that touch the forbidden region.
The total number of paths in a grid $[0, W] \times [0, H]$ is given by a closed-form formula involving binomial coefficients.
Paths touching the forbidden region are classified by their first point of contact.
We derived a system of linear equations for the number of paths that first touch the forbidden region at each boundary point.
This system is tridiagonal and can be solved in linear time.
Finally, we computed the contribution of each boundary point to the total number of bad paths and subtracted it from the total.
The complexity is dominated by the linear scan of the boundary, which is $O(W+H)$.
Modulo arithmetic is used throughout.
