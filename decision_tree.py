from __future__ import division
from collections import defaultdict
import math

def entropy(class_probabilities):
	"""given a list of class probabilities, compute the entropy"""
	return sum(-p * math.log(p, 2)
		for p in class_probabilities
		if p)	# ignore zero probabilities

def class_probabilities(labels):
	total_count = len(labels)
	return [count / total_count
		for count in Counter(labels).values()]

def data_entropy(labeled_data):
	labels = [label for _, label in labeled_data]
	probabilities = class_probabilities(labels)
	return entropy(probabilities)

def partition_entropy(subsets):
	"""find the entropy from this partition of data in subsets
	subsets is a list of lists of labeled data"""

	total_count = sum(len(subset) for subset in subsets)

	return sum( data_entropy(subset) * len(subset) / total_count
		for subset in subsets)

def partition_by(inputs, attribute):
	"""each input is a pair (attribute_dict, label).
	returns a dict : attribute_value -> inputs"""
	groups = defaultdict(list)
	for input in inputs:
		key = input[0][attribute]  # get the value of the specified attribute
		groups[key].append(input)  # then add this input to the correct list
	return groups

def partition_entropy(inputs, attribute):
	"""returns the entropy of partitioning the inputs by the specified attribute"""
	partitions = partition_by(inputs, attribute)
	return partition_entropy(partitions.values())

def classify(tree, input):
	"""runs an input through an already constructed decision tree"""

	# if this is a leaf node, return its value
	if tree in [True, False]:
		return tree

	# otherwise this tree consists of an attribute to split on
	# and a dictionary whose keys are values of that attribtue
	# and whose values are subtrees to consider next
	attribute, subtree_dict = tree

	subtree_key = input.get(attribute)	# None if input is missing attribute

	if subtree_key not in subtree_dict:	# if no subtree for key,
		subtree_key = None				# we'll use the None subtree

	subtree = subtree_dict[subtree_key]	# choose the appropriate subtree
	return classify(subtree, input)		# and use it to classify the input




inputs = [
        ({'level':'Senior','lang':'Java','tweets':'no','phd':'no'},   False),
        ({'level':'Senior','lang':'Java','tweets':'no','phd':'yes'},  False),
        ({'level':'Mid','lang':'Python','tweets':'no','phd':'no'},     True),
        ({'level':'Junior','lang':'Python','tweets':'no','phd':'no'},  True),
        ({'level':'Junior','lang':'R','tweets':'yes','phd':'no'},      True),
        ({'level':'Junior','lang':'R','tweets':'yes','phd':'yes'},    False),
        ({'level':'Mid','lang':'R','tweets':'yes','phd':'yes'},        True),
        ({'level':'Senior','lang':'Python','tweets':'no','phd':'no'}, False),
        ({'level':'Senior','lang':'R','tweets':'yes','phd':'no'},      True),
        ({'level':'Junior','lang':'Python','tweets':'yes','phd':'no'}, True),
        ({'level':'Senior','lang':'Python','tweets':'yes','phd':'yes'},True),
        ({'level':'Mid','lang':'Python','tweets':'no','phd':'yes'},    True),
        ({'level':'Mid','lang':'Java','tweets':'yes','phd':'no'},      True),
        ({'level':'Junior','lang':'Python','tweets':'no','phd':'yes'},False)
    ]

