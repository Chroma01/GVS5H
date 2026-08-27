from typing import List


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)

        # nxt[i] is the first index after i whose value is strictly greater
        # than nums[i].
        nxt = [n] * n
        stack = []

        for i, value in enumerate(nums):
            while stack and nums[stack[-1]] < value:
                nxt[stack.pop()] = i
            stack.append(i)

        # Binary lifting over the chain of successive strictly greater values.
        log = n.bit_length()
        up = [nxt]

        # weight[0][i] is the sum contributed by the constant prefix-max block
        # nums[i], ..., nums[nxt[i] - 1]. A terminal block is handled directly
        # during querying.
        weight = [[
            nums[i] * (nxt[i] - i) if nxt[i] < n else 0
            for i in range(n)
        ]]

        for _ in range(1, log):
            prev_up = up[-1]
            prev_weight = weight[-1]
            cur_up = [n] * n
            cur_weight = [0] * n

            for i in range(n):
                mid = prev_up[i]
                if mid < n:
                    cur_up[i] = prev_up[mid]
                    cur_weight[i] = prev_weight[i] + prev_weight[mid]

            up.append(cur_up)
            weight.append(cur_weight)

        prefix = [0] * (n + 1)
        for i, value in enumerate(nums):
            prefix[i + 1] = prefix[i] + value

        def required_increments(left: int, right: int) -> int:
            index = left
            target_sum = 0

            for p in range(log - 1, -1, -1):
                next_index = up[p][index]
                if next_index <= right:
                    target_sum += weight[p][index]
                    index = next_index

            target_sum += nums[index] * (right - index + 1)
            original_sum = prefix[right + 1] - prefix[left]
            return target_sum - original_sum

        answer = 0
        left = 0

        for right in range(n):
            while left <= right and required_increments(left, right) > k:
                left += 1
            answer += right - left + 1

        return answer