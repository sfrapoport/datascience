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
		for line in file:
			if line.startswith("Subject:"):
				#remove leading subject and keep remainder
				subject = re.sub(r"^Subject: ", "", line).strip()
				data.append((subject, is_spam))

random.seed(0)
train_data, test_data = split_data(data, 0.75)

classifier = NaiveBayesClassifier()
classifier.train(train_data)

# triplets (subject, actual_is_spam, predicted spam probability)
classified = [(subject, is_spam, classifier.classify(subject))
		for subject, is_spam in test_data]

# assume that spam_probability > 0.5 corresponds to spam prediction
# and count the combinations of (actual is_spam, predicted is_spam)

counts = Counter((is_spam, spam_probability > 0.5)
		for _, is_spam, spam_probability in classified)

print counts

# sort by spam_probability from smallest to largest
classified.sort(key=lambda row: row[2])
#print classified[-5:]
#highest predicted spam probs among the non-spams
spammiest_hams = filter(lambda row: not row[1], classified)[-5:]
hammiest_spams = filter(lambda row: row[1], classified)[:5]


