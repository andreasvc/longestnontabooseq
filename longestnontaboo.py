"""Given a set of taboo n-grams and a text, find the longest sequence of
tokens without any of the taboo n-grams. An n-gram is represented as a string
of space-separated tokens."""
import pandas


def tokenize(fname):
	"""Tokenize and lowercase text file."""
	with open(fname, encoding='utf8') as inp:
		tokens = nltk.word_tokenize(inp.read().lower())
	return pandas.Series(tokens)


def getngrams(tokens, taboo):
	"""return list `ngrams` s.t. ngrams[n - 1] contains n-grams of tokens,
	up to a maximum n determined by n-gram strings in `taboo`."""
	result = [tokens]
	if not taboo:
		return result
	maxn = max(len(a.split()) for a in taboo)
	# padding for the last n-grams of the text
	padding = pandas.Series([''] * maxn)
	padded = tokens.append(padding, ignore_index=True)
	for n in range(2, maxn + 1):
		subngrams = [padded[m:len(tokens) + m].values for m in range(1, n)]
		ngrams = tokens.str.cat(subngrams, sep=' ')
		result.append(ngrams)
	return result


def longest_non_taboo_sequence(ngrams, taboo):
	"""return longest sequence of tokens without any taboo n-grams.

	:param ngrams: a list of Series objects, must include n-grams up to
		the longest n-gram in taboo.
	:params taboo: a set of strings."""
	tokens = ngrams[0]
	istaboo = tokens.isin(taboo)
	for x in ngrams[1:]:
		istaboo |= x.isin(taboo)
	if not istaboo.any():
		return tokens
	indices = tokens[istaboo].index
	# pad the begin and end such since the first or last tokens may
	# be the longest non-taboo sequence
	indices = pandas.Series([-1] + list(indices) + [len(tokens)])
	longest = (indices[1:].values - indices[:-1].values).argmax()
	start = indices[longest]
	end = indices[longest + 1]
	if start == -1:
		start = 0
	else:
		start += max(n for a in taboo
				for n, x in enumerate(ngrams, 1) if x[start] == a)
	return tokens[start:end]


def test_getngrams():
	tokens = pandas.Series(['a', 'b', 'c'])
	assert getngrams(tokens, set()) == [tokens]
	assert getngrams(tokens, {'a'}) == [tokens]
	assert len(getngrams(tokens, {'a', 'a b'})) == 2
	assert len(getngrams(tokens, {'a', 'a b', 'a b c'})) == 3
	assert (getngrams(tokens, {'a', 'a b'})[1] == pandas.Series(
			['a b', 'b c', 'c '])).all()
	assert (getngrams(tokens, {'a', 'a b', 'a b c'})[2] == pandas.Series(
			['a b c', 'b c ', 'c  '])).all()


def test_longest_non_taboo_sequence():
	text = 'the cat is on the mat . the cat is sleeping .'
	tokens = pandas.Series(text.split())
	taboo = {'the cat'}
	ngrams = getngrams(tokens, taboo)
	assert len(longest_non_taboo_sequence(ngrams, taboo)) == 5
	assert (longest_non_taboo_sequence(ngrams, taboo)
			== 'is on the mat .'.split()).all()
	assert (longest_non_taboo_sequence(ngrams, {'the cat', 'the'})
			== 'is sleeping .'.split()).all()
	assert (longest_non_taboo_sequence(ngrams, {'mat'})
			== '. the cat is sleeping .'.split()).all()
	assert (longest_non_taboo_sequence(ngrams, {'sleeping'})
			== 'the cat is on the mat . the cat is'.split()).all()
