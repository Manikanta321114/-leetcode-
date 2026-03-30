class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        stack=[]
        
        for ch in s:
            if ch=='(' or ch=='{' or ch=='[' :
                stack.append(ch)
            else:
                if not stack:
                    return False
                top=stack[-1]
                if ch==')' and top!='(':
                    return False
                if ch=='}' and top!='{':
                    return False
                if ch==']' and top!='[':
                    return False
                stack.pop()
        return len(stack)==0