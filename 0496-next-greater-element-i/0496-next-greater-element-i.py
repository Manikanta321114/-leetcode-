class Solution(object):
    def nextGreaterElement(self, nums1, nums2):
        stack = []
        d = {}

        # Build next greater map from nums2
        for num in nums2:
            while stack and num > stack[-1]:
                d[stack.pop()] = num
            stack.append(num)

        # Remaining elements → no greater element
        while stack:
            d[stack.pop()] = -1

        # Build result for nums1
        result = []
        for num in nums1:
            result.append(d[num])

        return result