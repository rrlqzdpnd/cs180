from mpmath import *
from os import listdir
from os.path import isfile, join

mp.dps = 75	# uses floating point numbers up to 75 decimal places

class HammySpammy(object):

	def train(self):
		# asks for directory of ham training set
		hamdir = raw_input(">> Enter training directory for ham: ")
		hams = [ f for f in listdir(hamdir) if isfile(join(hamdir, f)) ]

		# asks for directory of spam training set
		spamdir = raw_input(">> Enter training directory for spam: ")
		spams = [ f for f in listdir(spamdir) if isfile(join(spamdir, f)) ]

		print ">> Scanning directories for the list of files..."
		self.hamcount = len(hams)	# initializes total count for ham emails
		self.spamcount = len(spams)	# initialized total count for spam emails
		self.total = self.hamcount + self.spamcount 	# initializes total number of emails

		self.hamdict = dict()
		self.spamdict = dict()
		self.dict = dict()

		# parse each ham email and collects list of words per email
		print ">> Creating dictionary for ham emails..."
		for ham in hams:
			filename = join(hamdir, ham)
			file = open(filename, "r")

			words = []
			while True:
				instr = file.read()
				if instr == "":
					break

				words = words + instr.split()

			words = list(set(words))	# uses the principle that a set cannot have multiple entries for the same element
			for word in words:
				if word in self.hamdict:
					self.hamdict[word] = self.hamdict[word] + 1
				else:
					self.hamdict[word] = 1

			file.close()

		# parse each spam email and collects list of words per email
		print ">> Creating dictionary for spam emails..."
		for spam in spams:
			filename = join(spamdir, spam)
			file = open(filename, "r")

			words = []
			while True:
				instr = file.read()
				if instr == "":
					break

				words = words + instr.split()

			words = list(set(words))	# uses the principle that a set cannot have multiple entries for the same element
			for word in words:
				if word in self.spamdict:
					self.spamdict[word] = self.spamdict[word] + 1
				else:
					self.spamdict[word] = 1

			file.close()

		# computes the probabilities for each word
		print ">> Computing distributions..."
		keys = self.hamdict.keys()
		for key in keys:
			if key not in self.dict:
				a = (self.hamdict[key] * 1.0) / self.hamcount 	# computes probability
				b = 0 if (key not in self.spamdict) else ((self.spamdict[key] * 1.0) / self.spamcount)	# if word also exists in spam, compute and add
				self.dict[key] = (a, b)	#adds word to dictionary of all words

		keys = self.spamdict.keys()
		for key in keys:
			if key not in self.dict:
				a = 0	# set to zero because these are the words in the spam messages only so zero probability
				b = (self.spamdict[key] * 1.0) / self.spamcount 	# computes probability
				self.dict[key] = (a, b)

		#### uncomment code below if you want to show to a separate file the words ####
		# file = open("out.txt", "w")
		# keys = self.dict.keys()
		# keys.sort()
		# for key in keys:
		# 	file.write(str(key) + ":\t\t" + str(self.dict[key][0]) + ",\t\t" + str(self.dict[key][1]) + "\n")
		# file.close()

		# set lambda (defaults to zero)
		willlambda = raw_input(">> Would you like to use lambda smoothing [Y/N]? ")
		if willlambda.upper()[:1] == "Y":
			try:
				self.lamb = input(">> Please input your value of lambda: ")
			except SyntaxError:
				self.lamb = 1
				print ">> Lambda set to default value of 1"
		else:
			self.lamb = 0

		print ">> Done training."


	def test(self):
		# asks for testing directory
		testdir = raw_input(">> Enter testing directory: ")
		filenames = [f for f in listdir(testdir) if isfile(join(testdir, f))]

		spamcounter = 0
		hamcounter = 0

		# opens each test file
		print "Analyzing files..."
		for filename in filenames:
			f = join(testdir, filename)
			file = open(f, "r")

			words = []
			while True:
				instr = file.read()
				if instr == "":
					break

				words = words + instr.split()

			words = list(set(words))
			hamtotal = mpf((self.hamcount * 1.0) / self.total)	# uses the mpmath package to convert to higher-precision floating points
			spamtotal = mpf((self.spamcount * 1.0) / self.total)	# uses the mpmath package to convert to higher-precision floating points
			for word in words:
				if word not in self.dict:
					continue	# ignores if word does not exist in dictionary
				else:
					a = self.dict[word][0]
					b = self.dict[word][1]

					if a == 0:	# if zero, uses lambda smoothing
						a = (self.lamb * 1.0) / (self.hamcount + (self.lamb * 2))
					if b == 0:	# if zero, uses lambda smoothing
						b = (self.lamb * 1.0) / (self.spamcount + (self.lamb * 2))

				hamtotal = hamtotal * a
				spamtotal = spamtotal * b

				# print word, hamtotal, spamtotal

			probability = (hamtotal * 1.0) / (hamtotal + spamtotal)	# computes probability whether ham or spam

			if probability < 0.5:	# if probability is less than 50%, spam
				out = "spam"
				spamcounter = spamcounter + 1
			else:	# otherwise, ham
				out = "ham"
				hamcounter = hamcounter + 1

			print filename + "\t- " + out
			file.close()

		print "Total number of ham messages:", hamcounter
		print "Total number of spam messages:", spamcounter

while True:
	print "**---------- MENU ----------**"
	choice = input("[1] Train\n[2] Test\n[3] Exit\n>> Enter choice: ")

	if choice == 1:
		analyzer = HammySpammy()
		analyzer.train()
	elif choice == 2:
		analyzer.test()
	elif choice == 3:
		print ">> Goodbye."
		break
	else:
		print ">> Invalid input."

	print ""