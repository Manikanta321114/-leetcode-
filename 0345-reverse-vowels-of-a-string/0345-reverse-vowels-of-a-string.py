class Solution(object):
    def reverseVowels(self, s):
        """
        :type s: str
        :rtype: str
        """
        v="aeiouAEIOU"
        left=0
        right=len(s)-1
        s=list(s)
        while left<right:
            if(s[left] in v and s[right] in v):
                s[left],s[right]=s[right],s[left]
                left += 1
                right -= 1
            elif(s[left]not in v):
                left+=1
            elif(s[right] not in v):

                right-=1
        return "".join(s)      