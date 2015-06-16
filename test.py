from __future__ import division
import glob, re
import random
from collections import Counter
from spam_filter import NaiveBayesClassifier
# modify the path with wherever you've put the files
path = "./data/*/*"

data = []

def split_data(data, prob):
	"""split data into fractions [prob, 1-prob]"""
	results = [], []
	for row in data:
		results[0 if random.random() < prob else 1].append(row)
	return results


for fn in glob.glob(path):
	is_spam = "ham" not in fn

	with open(fn, 'r') as file:
		in_header = True
		file_contents =''
		for line in file:
			if in_header: 
				if line.startswith("Subject:"):
					#remove leading subject and keep remainder
					subject = re.sub(r"^Subject: ", "", line).strip()
					file_contents += subject
				if not line.strip():
					in_header = False
			else: 
				file_contents += line.strip()
		data.append((file_contents, is_spam))

	
train_data, test_data = split_data(data, 0.75)

classifier = NaiveBayesClassifier(min_count = 2)
classifier.train(train_data)

# triplets (subject, actual_is_spam, predicted spam probability)
classified = [(subject, is_spam, classifier.classify(subject))
		for subject, is_spam in test_data]

# assume that spam_probability > 0.5 corresponds to spam prediction
# and count the combinations of (actual is_spam, predicted is_spam)

counts = Counter((is_spam, spam_probability > 0.5)
		for _, is_spam, spam_probability in classified)

print counts

