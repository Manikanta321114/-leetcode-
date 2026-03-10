class Solution(object):
    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        prefix=strs[0]
        prefix = ""

        for i in range(len(strs[0])):

            for word in strs:

                if i >= len(word) or word[i] != strs[0][i]:
                    return prefix

            prefix += strs[0][i]

        return prefix





















