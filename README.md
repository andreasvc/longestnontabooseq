# Find the longest non-taboo sequence

Find the longest sequence of tokens in a text without any taboo n-grams.

## Usage

Given a set of taboo n-grams and a text, find the longest sequence of tokens
without any of the taboo n-grams. An n-gram is represented as a string of
space-separated tokens.

$ longestnontaboo.py [--len] <taboofile> <filenames...>

Specify taboo n-grams with one n-gram per line in taboofile;
multiple filenames can be specified.
By default the output is the longest non-taboo sequence.
With --len, only the length of this sequence is reported.
