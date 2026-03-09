class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        return len(s.split()[-1])
        #s=s.strip()
        #words=s.split()
        #length=words[-1]
        
        #return len(words)

        
        