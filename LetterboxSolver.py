
# NYT letter-boxed solver
# the goal is to use all the letters
# in the minimum number of words
# where every following word must use
#   the last letter of the previous word
# where no letter can be repeated
# where every next letter must be on another
#   side of the box (not in the same sub-list)
from pickle import NONE
import random
import re
# >> pip install english-words==2.0.1
# https://pypi.org/project/english-words/2.0.1/
# from english_words import get_english_words_set
from english_dictionary.scripts.read_pickle import get_dict

# web2lowerset = get_english_words_set(['gcide'], lower=True, alpha=False)
web2lowerset = set([x.lower() for x in get_dict().keys()])

side1 = ["a", "w", "i"]
side2 = ["t", "m", "e"]
side3 = ["p", "n", "r"]
side4 = ["b", "k", "s"]

randomStart = False
if randomStart:
	randLetters = [chr(ord("a")+i) for i in range(26) if i<22 and i!=16]
	random.shuffle(randLetters)
	side1 = randLetters[0:3]
	side2 = randLetters[3:6]
	side3 = randLetters[6:9]
	side4 = randLetters[9:12]

BOX = [side1, side2, side3, side4]
LETTERS = []
for small in BOX:
	for letter in small:
		LETTERS.append(letter)

print("LETTER BOX")
print(side1)
print(side2)
print(side3)
print(side4)

current_letter = ""
current_sublist = 0

def GetNextValidLetters(sublist_index):
	valid_sublists = [x for idx, x in enumerate(BOX) if idx != sublist_index]
	valid_letters = [item for sublist in valid_sublists for item in sublist]
	return valid_letters
	
ADJACENCIES = {}
for idx, x in enumerate(BOX):
	for letter in x:
		ADJACENCIES[letter] = GetNextValidLetters(idx)
		

		
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
for letter in ADJACENCIES:
	if letter.lower() in impossible_bigrams:
		ADJACENCIES[letter] = [x for x in ADJACENCIES[letter] if x.lower() not in impossible_bigrams[letter.lower()]]

# remove any words that contain letters NOT IN the letterbox
def filter_words2(word):
	return len(set(word).difference(set(LETTERS))) == 0
web2lowerset = list(filter(lambda word: filter_words2(word), web2lowerset))
# print(web2lowerset)
print(len(web2lowerset))
# remove any words that contains DOUBLE letters
regexp = re.compile(r"(.)\1")
def filter_words3(word):
	return re.search(regexp, word) == None
web2lowerset = list(filter(lambda word: filter_words3(word), web2lowerset))
# print(web2lowerset)
print(len(web2lowerset))
# remove any words that contains NON ADJACENT letters
def filter_words4(word):
	if len(word) < 3: return False
	for idx in range(len(word)-1):
		if word[idx+1] not in ADJACENCIES[word[idx]]:
			return False
	return True
web2lowerset = list(filter(lambda word: filter_words4(word), web2lowerset))
web2lowerset.sort(key=lambda x: len(x), reverse=True)


COMPARE_SET = set([x.lower() for sublist in ADJACENCIES for x in sublist])
def AllLettersUsed(words):
	word_set = set([x.lower() for sublist in words for x in sublist])
	# print(COMPARE_SET.intersection(word_set))
	return len(COMPARE_SET) == len(COMPARE_SET.intersection(word_set))



#############################
#############################
#############################
# WE ARE FORGETTING THAT THE NEXT WORD NEEDS TO START
# WITH THE LAST LETTER OF THE PREVIOUS!!!!!!!!!!!!!!!
#############################
#############################
# start the real path finding
setLETTERS = set(LETTERS)
for word in web2lowerset:
	if AllLettersUsed(word):
		print(f"FOUND SUPER WORD = {word}")
print("FINISH SOLO WORD SEARCH")

for idx, word in enumerate(web2lowerset):
	for idx2, word2 in enumerate([x for y, x in enumerate(web2lowerset) if y > idx and x != word]):
		size = len(setLETTERS.intersection(set(word), set(word2))) 
		if (AllLettersUsed([word, word2])):
			print(f"FOUND (potential) PAIR = {word}, {word2}")
			
print("FINISH DOUBLE WORD SEARCH")

		
max_depth = 3
def deep_search(current_solution):
	for idx, word in enumerate(web2lowerset):
		deep_search2([word], [idx])
		
def deep_search2(current_solution, indeces):
	if len(current_solution) >= max_depth:
		if AllLettersUsed(current_solution):
			print(f"found solution = {current_solution}")
		return
	# for idx2, word2 in [(y, x) for y, x in enumerate(web2lowerset) if y > max(indeces) and x not in current_solution]:
	for idx2, word2 in [(y, x) for y, x in enumerate(web2lowerset) if x not in current_solution and (x[0] == (current_solution[-1])[-1]) ]:
		current_solution.append(word2)
		indeces.append(idx2)
		if AllLettersUsed(current_solution):
			print(f"found solution = {current_solution}")
			current_solution.pop()
			indeces.pop()
			return
		else:
			deep_search2(current_solution, indeces)
		current_solution.pop()
		indeces.pop()
solution = []
deep_search(solution)