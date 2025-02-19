
import random
import re
# >> pip install english-words==2.0.1
# https://pypi.org/project/english-words/2.0.1/
# from english_words import get_english_words_set
# web2lowerset = get_english_words_set(['gcide'], lower=True, alpha=False)
from english_dictionary.scripts.read_pickle import get_dict


# https://linguistics.stackexchange.com/questions/4082/impossible-bigrams-in-the-english-language
# to speed up processing, each letter should have a unique duplicate
# so that impossible letter combos can be modified at this level
impossible_bigrams = {
'b': ['k', 'q', 'x'], 'f': ['q', 'v', 'x', 'z', 'k'], 
'j': ['c', 't', 'd', 'v', 'f', 'w', 'g', 'x', 'h', 'y', 'k', 'z', 'l', 'm', 'n', 'p', 'q', 'r', 'b', 's'], 
'm': ['j', 'q', 'x', 'z', 'g'], 
'q': ['h', 'x', 'j', 'y', 'k', 'z', 'l', 'm', 'n', 'o', 'b', 'p', 'c', 'r', 'd', 's', 'e', 't', 'f', 'v', 'g', 'w'], 
'v': ['j', 'k', 'm', 'n', 'p', 'q', 't', 'b', 'w', 'c', 'x', 'd', 'z', 'f', 'g', 'h'], 
'w': ['z', 'q', 'v', 'x'], 'z': ['h', 'j', 'n', 'q', 'r', 's', 'x', 'b', 'c', 'g'], 
'x': ['b', 'g', 'j', 'k', 'v', 'z'], 'c': ['b', 'f', 'g', 'j', 'p', 'v', 'w', 'x'], 
's': ['x', 'z'], 'g': ['q', 'v', 'x'], 'p': ['q', 'v', 'x'], 't': ['q', 'x'], 'k': ['q', 'v', 'x', 'z'], 
'h': ['k', 'v', 'x', 'z'], 'y': ['q', 'v', 'z'], 'l': ['q', 'x'], 'd': ['x'], 'i': ['y']
}

class Solver:
	def __init__(self, side1, side2, side3, side4):
		self.side1 = side1
		self.side2 = side2
		self.side3 = side3
		self.side4 = side4
		self.max_depth = 3
		self.all_possible_words = set([x.lower() for x in get_dict().keys()])
		self.BOX = [side1, side2, side3, side4]
		print(self.BOX)
		self.LETTERS = [x_letter for y_list in self.BOX for x_letter in y_list]
		print(self.LETTERS)
		self.ADJACENCIES = {}
		for idx, x in enumerate(self.BOX):
			for letter in x:
				self.ADJACENCIES[letter] = self.GetNextValidLetters(idx)
		for letter in self.ADJACENCIES:
			if letter.lower() in impossible_bigrams:
				self.ADJACENCIES[letter] = [x for x in self.ADJACENCIES[letter] if x.lower() not in impossible_bigrams[letter.lower()]]
		# self.randomStart = False
		# if self.randomStart:
		# 	randLetters = [chr(ord("a")+i) for i in range(26) if i<22 and i!=16]
		# 	random.shuffle(randLetters)
		# 	side1 = randLetters[0:3]
		# 	side2 = randLetters[3:6]
		# 	side3 = randLetters[6:9]
		# 	side4 = randLetters[9:12]
				
	def GetNextValidLetters(self, sublist_index):
		valid_sublists = [x for idx, x in enumerate(self.BOX) if idx != sublist_index]
		valid_letters = [item for sublist in valid_sublists for item in sublist]
		return valid_letters
	# remove any words that contain letters NOT IN the letterbox
	def filter_words2(self, word):
		return len(set(word).difference(set(self.LETTERS))) == 0
	
	# remove any words that contains DOUBLE letters
	def filter_words3(self, word):
		return re.search(self.regexp, word) == None
	
	# remove any words that contains NON ADJACENT letters
	def filter_words4(self, word):
		if len(word) < 3: return False
		for idx in range(len(word)-1):
			if word[idx+1] not in self.ADJACENCIES[word[idx]]:
				return False
		return True

	def AllLettersUsed(self, words):
		word_set = set([x.lower() for sublist in words for x in sublist])
		# print(COMPARE_SET.intersection(word_set))
		return len(self.COMPARE_SET) == len(self.COMPARE_SET.intersection(word_set))

	def deep_search(self, current_solution, depth):
		for idx, word in enumerate(self.all_possible_words):
			self.deep_search2([word], [idx], depth)
		
	def deep_search2(self, current_solution, indeces, depth):
		if len(current_solution) >= depth:
			if self.AllLettersUsed(current_solution):
				print(f"found solution = {current_solution}")
			return
		# for idx2, word2 in [(y, x) for y, x in enumerate(web2lowerset) if y > max(indeces) and x not in current_solution]:
		for idx2, word2 in [(y, x) for y, x in enumerate(self.all_possible_words) if x not in current_solution and (x[0] == (current_solution[-1])[-1]) ]:
			current_solution.append(word2)
			indeces.append(idx2)
			if self.AllLettersUsed(current_solution):
				print(f"found solution = {current_solution}")
				current_solution.pop()
				indeces.pop()
				return
			else:
				self.deep_search2(current_solution, indeces, depth)
			current_solution.pop()
			indeces.pop()
			
	# start the real path finding
	def Solve(self, exhaustive=True):
		self.regexp = re.compile(r"(.)\1")
		self.all_possible_words = list(filter(lambda word: self.filter_words2(word), self.all_possible_words))
		self.all_possible_words = list(filter(lambda word: self.filter_words3(word), self.all_possible_words))
		self.all_possible_words = list(filter(lambda word: self.filter_words4(word), self.all_possible_words))
		# self.all_possible_words.sort(key=lambda x: len(x), reverse=True)
		self.all_possible_words.sort()
		self.COMPARE_SET = set([x.lower() for sublist in self.ADJACENCIES for x in sublist])
		
		solution = [word for word in self.all_possible_words if self.AllLettersUsed(word)]
		for word in solution:
			print(f"FOUND SUPER WORD = {word}")
		
		if len(solution) > 0:
			input(f"continue...")
		print("FINISH SOLO WORD SEARCH")

		# setLETTERS = set(self.LETTERS)
		# for idx, word in enumerate(self.all_possible_words):
		# 	for idx2, word2 in enumerate([x for y, x in enumerate(self.all_possible_words) if y > idx and x != word]):
		# 		size = len(setLETTERS.intersection(set(word), set(word2))) 
		# 		if (self.AllLettersUsed([word, word2])):
		# 			print(f"FOUND (potential) PAIR = {word}, {word2}")
		# print("FINISH DOUBLE WORD SEARCH")
		
		self.deep_search(solution, 2)
		print("FINISH DEPTH 2 SEARCH")
		
		if not exhaustive: return
		input(f"continue exhaustive search...")
		for i in range(3, self.max_depth+1):
			self.deep_search(solution, i)
			
		print("FINISH MAX DEPTH SEARCH")

# MAIN
if __name__ == "__main__":
	print("LETTER BOXED")
	print("(Input letters like 'xyz' or 'abc')")
	user_input = input("side 1: ")
	side1 = [str(letter) for letter in user_input[:3]]
	user_input = input("side 2: ")
	side2 = [str(letter) for letter in user_input[:3]]
	user_input = input("side 3: ")
	side3 = [str(letter) for letter in user_input[:3]]
	user_input = input("side 4: ")
	side4 = [str(letter) for letter in user_input[:3]]
	user_input = input("look for 3 word solutions? (y/n): ")
	exhaustive = user_input != '' and user_input[0].lower() == 'y'
	
	solver = Solver(side1, side2, side3, side4)
	solver.Solve(exhaustive)