from typing import List, Optional, Tuple
from bisect import bisect_left


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        # Sort by ending position so every previously processed interval ends
        # no later than the current interval.
        ordered = sorted(
            (left, right, weight, index)
            for index, (left, right, weight) in enumerate(intervals)
        )
        ordered.sort(key=lambda item: item[1])

        ends = sorted({right for _, right, _, _ in ordered})
        endpoint_count = len(ends)

        State = Tuple[int, Tuple[int, ...]]

        def better(
            first: Optional[State],
            second: Optional[State],
        ) -> Optional[State]:
            if first is None:
                return second
            if second is None:
                return first

            if first[0] != second[0]:
                return first if first[0] > second[0] else second

            return first if first[1] < second[1] else second

        # One Fenwick tree for each exact number of chosen intervals.
        trees: List[List[Optional[State]]] = [
            [None] * (endpoint_count + 1) for _ in range(5)
        ]

        def query(
            tree: List[Optional[State]],
            position: int,
        ) -> Optional[State]:
            result: Optional[State] = None
            while position > 0:
                result = better(result, tree[position])
                position -= position & -position
            return result

        def update(
            tree: List[Optional[State]],
            position: int,
            state: State,
        ) -> None:
            while position <= endpoint_count:
                tree[position] = better(tree[position], state)
                position += position & -position

        best_by_count: List[Optional[State]] = [None] * 5
        best_by_count[0] = (0, ())

        for left, right, weight, original_index in ordered:
            end_position = bisect_left(ends, right) + 1

            # Descending order prevents using the current interval twice.
            for count in range(4, 0, -1):
                if count == 1:
                    candidate: State = (weight, (original_index,))
                else:
                    # Only endpoints strictly smaller than `left` are valid.
                    prefix_length = bisect_left(ends, left)
                    predecessor = query(trees[count - 1], prefix_length)

                    if predecessor is None:
                        continue

                    previous_weight, previous_indices = predecessor
                    candidate = (
                        previous_weight + weight,
                        tuple(sorted(previous_indices + (original_index,))),
                    )

                update(trees[count], end_position, candidate)
                best_by_count[count] = better(
                    best_by_count[count], candidate
                )

        answer: Optional[State] = None
        for state in best_by_count:
            answer = better(answer, state)

        return list(answer[1]) if answer is not None else []