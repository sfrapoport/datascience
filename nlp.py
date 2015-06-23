from bs4 import BeautifulSoup
import requests, re, random
from collections import defaultdict

def fix_unicode(text):
	return text.replace(u"\u2019", "'")

# url = "http://radar.oreilly.com/ideas/what-is-data-science"
# html = requests.get(url).text
# soup = BeautifulSoup(html, 'html5lib')

# content = soup.find("div", "article-body")
# regex = r"[\w']+|[\.]"

# document = []

# for paragraph in content("p"):
# 	words = re.findall(regex, fix_unicode(paragraph.text))
# 	document.extend(words)

# bigrams = zip(document, document[1:])
# transitions = defaultdict(list)
# for prev, current in bigrams:
# 	transitions[prev].append(current)

def generate_using_bigrams():
	current = "."
	result = []
	while True:
		next_word_candidates = transitions[current]
		current = random.choice(next_word_candidates)
		result.append(current)
		if current == ".": return " ".join(result)

# trigrams = zip(document, document[1:], document[2:])
# trigram_transitions = defaultdict(list)
# starts = []

# for prev, current, next in trigrams:
# 	if prev == ".":
# 		starts.append(current)

# 	trigram_transitions[(prev, current)].append(next)

def generate_using_trigrams():
	current = random.choice(starts)
	prev = "."
	result = [current]
	while True:
		next_word_candidates = trigram_transitions[(prev, current)]
		next_word = random.choice(next_word_candidates)

		prev, current = current, next_word
		result.append(current)

		if current == ".":
			return " ".join(result)
# Grammars 

grammar = {
        "_S" : ["_NP _VP"],
        "_NP" : ["_N", 
            "_A _NP _P _A _N"],
        "_VP" : ["_V", 
            "_V _NP"],
        "_N" : ["data science", "Python", "regression", "buffalo"],
        "_A" : ["big", "linear", "logistic", "Buffalo"],
        "_P" : ["about", "near"],
        "_V" : ["learns", "trains", "tests", "is", "buffalo"]
        }

def is_terminal(token):
    return token[0] != "_"

def expand(grammar, tokens):
    for i, token in enumerate(tokens):
        if is_terminal(token): continue

        replacement = random.choice(grammar[token])

        if is_terminal(replacement):
            tokens[i] = replacement
        else:
            tokens = tokens[:i] + replacement.split() + tokens[(i+1):]

        return expand(grammar, tokens)
    return tokens

def generate_sentence(grammar):
    return " ".join(expand(grammar, ["_S"]))

for i in range(0, 6): print generate_sentence(grammar)

