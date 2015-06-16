from __future__ import division
import re
import math
from collections import defaultdict

def tokenize(message):
	message = message.lower()
	all_words = re.findall("[a-z0-9']+", message)
	return set(all_words)

def count_words(training_set):
	"""training set consists of pairs (message, is_spam)"""
	counts = defaultdict(lambda: [0, 0])
	for message, is_spam in training_set:
		for word in tokenize(message):
			counts[word][0 if is_spam else 1] += 1
	return counts


def word_probabilities(counts, total_spams, total_non_spams, min_count):
	"""turn word counts into a dictionary of words to spam probabilities"""

	words = {}
	for w, (spam, non_spam) in counts.iteritems():
		if spam + non_spam >= min_count: 
			g = min(1, 2 * non_spam / total_non_spams)
			b = min(1, spam / total_spams)
			words[w] = max(0.01, min(0.99, b / (b + g)))
	return words


def spam_probability(word_probs, message):
	message_words = tokenize(message)
	log_prob_if_spam = log_prob_if_not_spam = 0.0
	
	message_probs = []
	for word in message_words:
		if word in word_probs:
			message_probs.append(word_probs[word]) 
	notable_probs = most_extreme(message_probs)

	inverse_probs = [1-prob for prob in notable_probs]
	prob_product = reduce(lambda prob, acc: prob * acc, notable_probs)
	inverse_prob_product = reduce(lambda prob, acc: prob * acc, inverse_probs)
	return prob_product / (prob_product + inverse_prob_product)

def most_extreme(probabilities, n=15):
	if len(probabilities) <= n:
		return probabilities 

	probabilities.sort()
	hammiest_probs = probabilities[:n]
	spammiest_probs = probabilities[-n:]
	hammiest_probs.reverse()

	while len(spammiest_probs) + len(hammiest_probs) > n:
		if extremeness(hammiest_probs[0]) > extremeness(spammiest_probs[0]):
			spammiest_probs.pop(0)
		else:	
			hammiest_probs.pop(0)

	return spammiest_probs + hammiest_probs

def extremeness(probability):
	return abs(0.5 - probability)

class NaiveBayesClassifier:
	def __init__(self, min_count=0):
		self.word_probs = []
		self.min_count = min_count
	
	def train(self, training_set):

		# count spam and non-spam messages
		num_spams = len([is_spam
			for message, is_spam in training_set
			if is_spam])
		num_non_spams = len(training_set) - num_spams

		# run training data through our pipeline
		word_counts = count_words(training_set)
		self.word_probs = word_probabilities(word_counts, num_spams, num_non_spams, self.min_count)
	
	def classify(self, message):
		return spam_probability(self.word_probs, message)


