class Solution:
	def backspaceCompare(self, S, T):
		i = len(S) - 1			# Traverse from the end of the strings
		j = len(T) - 1

		skipS = 0              # The number of backspaces required till we arrive at a valid character
		skipT = 0

		while i >= 0 or j >= 0:
			while i >= 0:					# Ensure that we are comparing a valid character in S
				if S[i] == "#" :
					skipS += 1				# If not a valid character, keep times we must backspace.
					i = i - 1

				elif skipS > 0:
					skipS -= 1				# Backspace the number of times calculated in the previous step
					i = i - 1

				else:
					break

			while j >= 0:					# Ensure that we are comparing a valid character in T
					if T[j] == "#":
						skipT += 1			# If not a valid character, keep times we must backspace.
						j = j - 1

					elif skipT > 0:
						skipT -= 1			# Backspace the number of times calculated in the previous step
						j = j - 1

					else:
						break

			print("Comparing", S[i], T[j])		# Print out the characters for better understanding.

			if i>= 0 and j >= 0 and S[i] != T[j]:    # Compare both valid characters. If not the same, return False.
				return False

			if (i>=0) != (j>=0):		# Also ensure that both the character indices are valid. If it is not valid,
				return False			#  it means that we are comparing a "#" with a valid character.

			i = i - 1
			j = j - 1

		return True					# This means both the strings are equivalent.