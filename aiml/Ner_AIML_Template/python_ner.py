# -*- coding:utf-8 -*- 

import re
import os
import copy

def film(sentence, quasiEntity):
	# judging whether the 'quasi' entity is a film or not
	keywords = [u'电影',u'看',u'部',u'演',u'台词',u'片',u'影视',u'票房',u'动画']
	sentence = sentence.decode('utf-8')
	RE1 = quasiEntity + u'.*' 
	RE2 = u'.*' + quasiEntity
	keychain = u''
	for keyword in keywords[:-1]:
		keychain += keyword + '|'
	keychain = u'(' + keychain + keywords[-1] + u')'
	RE1 = RE1 + keychain
	RE2 = keychain + RE2
	RE3 = u'[《<\{\[].*' + quasiEntity + u'.*[>》\}\]]' 
	RE = RE1 + '|' + RE2 + '|' + RE3
	if re.search(RE,sentence):
		return True
	else:
		return False


def music(sentence, quasiEntity):
	# judging whether the 'quasi' entity belongs to music class or not
	keywords = [u'音乐',u'歌',u'首',u'循环',u'曲',u'词',u'旋律',u'专辑',u'唱',u'听']
	sentence = sentence.decode('utf-8')
	RE1 = quasiEntity + u'.*' 
	RE2 = u'.*' + quasiEntity
	keychain = u''
	for keyword in keywords[:-1]:
		keychain += keyword + '|'
	keychain = u'(' + keychain + keywords[-1] + u')'
	RE1 = RE1 + keychain
	RE2 = keychain + RE2
	RE3 = u'[《<\{\[].*' + quasiEntity + u'.*[>》\}\]]' 
	RE = RE1 + '|' + RE2 + '|' + RE3
	if re.search(RE,sentence):
		return True
	else:
		return False

def book(sentence, quasiEntity):
	# judgin whether the 'quasi' entity is a book or not
	keywords = [u'书',u'看',u'读',u'本',u'版',u'作者',u'部']
	sentence = sentence.decode('utf-8')
	RE1 = quasiEntity + u'.*' 
	RE2 = u'.*' + quasiEntity
	keychain = u''
	for keyword in keywords[:-1]:
		keychain += keyword + '|'
	keychain = u'(' + keychain + keywords[-1] + u')'
	RE1 = RE1 + keychain
	RE2 = keychain + RE2
	RE3 = u'[《<\{\[].*' + quasiEntity + u'.*[>》\}\]]' 
	RE = RE1 + '|' + RE2 + '|' + RE3
	if re.search(RE,sentence):
		return True
	else:
		return False

class ner:
	def __init__(self, entityNameList = ['film','music','book','entertainer','politician','location','company','country','food','entrepreneur_cn','event','animation']):
		self.entityDict = {}
		curpath = os.path.dirname(os.path.abspath(__file__))
		for entityName in entityNameList:
			file = curpath + '/Data/' + entityName + '.txt'
			self.entityDict[entityName] = self.buildEntityHashing(file)

	def getWordsList(self,shortSentence):
		# split a short sentence(includes no punctuation) into several chinese words or english words
		wordList = []
		assert isinstance(shortSentence,unicode) 
		while len(shortSentence.strip()) > 0:
			# m = re.match(ur'[\u4e00-\u9fa5]',shortSentence)
			if re.match(ur'[\u4e00-\u9fa5]',shortSentence):
				m = re.match(ur'[\u4e00-\u9fa5]',shortSentence)
				shortSentence = shortSentence[len(m.group(0)):]
				wordList.append(m.group(0))
			elif re.match(ur'\w+',shortSentence):
				m = re.match(ur'\w+',shortSentence)
				shortSentence = shortSentence[len(m.group(0)):]
				wordList.append(u' '+m.group(0))
			else:
				shortSentence = shortSentence[1:]
		return wordList

	def splitSentence(self,sentence):
		# split a long sentence into several parts, the delimiters include Chinese punctuation { 。，：；？“”‘’［］｛｝《》｜、／～｀！@＃¥％……&＊（）－——＋＝ }  
		# and English punctuation { .,:;?"'[]{}<>|\/~`!@#$%^&*()-_+= }
		shortSentenceList = re.split(ur'[。，；？“”‘’［］｛｝《》｜、／～｀！@＃¥％…&＊（）－——＋＝\t,;?"\[\]\{\}<>|\\/~`!@#$%^*\(\)_+=]+'\
			,sentence.decode('utf-8'))
		return shortSentenceList


	def buildNgram(self,wordList):
		# build a lower triangular matrix (list in list) to store the ngrams, for a input word list wl = ['a','b','c'] the result looks like:
		# [
		#  ['a'],
		#  ['b','ab'],
		#  ['c','bc','abc']
		# ]
		record = []
		ngram = []
		for word in wordList:
			record.insert(0,u'')
			for i in range(len(record)):
				record[i] += word
				record[i] = record[i].strip()
			newrecord = copy.deepcopy(record)
			ngram.append(newrecord)
		return ngram


	def buildEntityHashing(self,fileName):
		# Read a entity list file and return an initialized hash table which looks like:
		# {
		#	'entityname1':[total=0, count_as_entity=0],
		#	'alias of entity1': entityname1
		#	'entityname2':[total=0, count_as_entity=0],
		#   ...,
		# }
		try:
			f = open(fileName,'r')
		except IOError, err:
			print err
		# else:
		# 	print 'Failed to open the specific file!'

		EntityHashTable = {}
		for line in f.readlines():
			tokens = line.decode('utf-8').split('\t')
			assert len(tokens) >= 1
			EntityHashTable[tokens[0].strip()] = [0,0]
			for token in tokens[1:]:
				if not EntityHashTable.has_key(token.strip()):
					EntityHashTable[token.strip()] = tokens[0]
		f.close()

		return EntityHashTable


	def resolveSentence(self, line, disambiguationList = [u'film',u'music',u'book']):
		# count the number of time that the entities appear, and update the entityDict
		# sentences = line.split('\t')
		sentences = [line]
		for sentence in sentences: # sentence is a 'utf-8' string while shortSentences are unicode
			shortSentenceList = self.splitSentence(sentence)
			# print shortSentenceList
			for shortSentence in shortSentenceList:
				wordList = self.getWordsList(shortSentence)
				ngram = self.buildNgram(wordList)
				for record in ngram:
					for item in record:
						for category in self.entityDict.keys():
							if self.entityDict[category].has_key(item):
								# print "find!%s,%s"%(category,item)
								if isinstance(self.entityDict[category][item],list):
									self.entityDict[category][item][0] += 1
								else:
									key = self.entityDict[category][item]
									self.entityDict[category][key][0] += 1
								if category in disambiguationList:
									if globals()[category](sentence, item):
										if isinstance(self.entityDict[category][item],list):
											self.entityDict[category][item][1] += 1
										else:
											key = self.entityDict[category][item]
											self.entityDict[category][key][1] += 1

	def getMatchedEntity(self,sentence):
		matchedEntity = []
		shortSentenceList = self.splitSentence(sentence)
		for shortSentence in shortSentenceList:
			wordList = self.getWordsList(shortSentence)
			if len(wordList) > 0:
				ngram = self.buildNgram(wordList)
				length = len(ngram)
				assert len(ngram[-1]) == length
				hb = length # horizon bound
				row,col = 0,0
				currentMatch = []
				for record in ngram:
					for item in record:
						flag,currentMatch = self.inEntityDict(item,self.entityDict,currentMatch,sentence)
						if flag and currentMatch not in matchedEntity:
							matchedEntity.append(currentMatch)
		return matchedEntity

	def findAllEntity(self,sentence):
		# greedily match all entities that appears in the sentence
		# using a ngram list looks like below
		# [
		#  ['a'],
		#  ['b','ab'],
		#  ['c','cb','abc']
		# ]
		result = {}
		matchedEntity = self.getMatchedEntity(sentence)
		# shortSentenceList = self.splitSentence(sentence)
		# for shortSentence in shortSentenceList:
		# 	wordList = self.getWordsList(shortSentence)
		# 	if len(wordList) > 0:
		# 		ngram = self.buildNgram(wordList)
		# 		length = len(ngram)
		# 		assert len(ngram[-1]) == length
		# 		hb = length # horizon bound
		# 		row,col = 0,0
		# 		currentMatch = []
		# 		for record in ngram:
		# 			for item in record:
		# 				flag,currentMatch = self.inEntityDict(item,self.entityDict,currentMatch,sentence)
		# 				if flag and currentMatch not in matchedEntity:
		# 					matchedEntity.append(currentMatch)
			# while row<length:
			# 	item = ngram[row][col]
			# 	print item
			# 	if inEntityDict(ngram[row][col],entityDict,currentMatch):
			# 		col += 1
			# 	else:
			# 		if len(currentMatch) > 0 and currentMatch not in matchedEntity:
			# 			matchedEntity.append(currentMatch)
			# 			currentMatch = []
			# 		col = 0
			# 	row += 1
			
			# if len(currentMatch) > 0 and currentMatch not in matchedEntity:
			# 	matchedEntity.append(currentMatch)

		matchedEntity.sort(cmp = lambda x,y: cmp(len(y[0]),len(x[0])))
		existedIntervals = []
		# strl = ''
		for item in matchedEntity:
			newIntervals = self.substring(item[0],sentence.decode('utf-8'))
			validIntervals,existedIntervals = self.checkValid(existedIntervals,newIntervals)
			valueDict = {}
			if len(validIntervals):
				valueDict['pos'] = validIntervals
				assert len(item) >= 2
				valueDict['category'] = item[1:]
				result[item[0]] = valueDict
				# print item[0],item[1:],validIntervals
		return result


	def inEntityDict(self, quasiEntity, currentMatch, sentence, disambiguationList = [u'film',u'music',u'book']):
		flag = False
		match = []
		match.append(quasiEntity)
		for key, categoricalDict in self.entityDict.iteritems():
			if categoricalDict.has_key(quasiEntity):
				# print 'match:%s'%quasiEntity
				# if key in disambiguationList:
				# 	if globals()[key](sentence, quasiEntity):
				# 		flag = True
				# 		match.append(key)
				# else:
				flag = True
				match.append(key)
		if flag:
			currentMatch = match
		return flag,currentMatch


	def substring(self,pattern,strl,method = 'kmp'):
		allMatchedIndex = []
		if method == 'kmp':
		# build nextIndex array
			length = len(pattern)
			nextIndex = [0]*length
			curMaxlen = 0
			i = 1
			while i < length:
				if pattern[i]==pattern[curMaxlen]:
					nextIndex[i] = curMaxlen
					i += 1
					curMaxlen += 1
				else:
					if curMaxlen > 0:
						curMaxlen = nextIndex[curMaxlen-1]
					else:
						nextIndex[i] = 0
						i += 1

			i,j = 0,0
			while i < len(strl):
				if strl[i] == pattern[j]:
					i += 1
					j += 1
				if j == length:
					allMatchedIndex.append([i-j,i-1])
					i += 1
					j = 0
				if i < len(strl) and strl[i] != pattern[j]:
					if j > 0:
						j = nextIndex[j-1]	
					else:
						i += 1

		else: # force brute
			length = len(pattern)
			i = 0
			while i < len(strl)-length:
				if strl[i:i+length] == pattern:
					allMatchedIndex.append[i,i+length-1]
					i = i + length
				else:
					i += 1

		return allMatchedIndex

	def checkValid(self,existedIntervals,newIntervals):
		result = []
		if len(existedIntervals) == 0:
			existedIntervals = copy.deepcopy(newIntervals)
			result = copy.deepcopy(newIntervals)
		else:
			flag = True
			for interval in newIntervals:
				for item in existedIntervals:
					if (interval[0] <= item[1] and interval[0] >= item[0]) \
						or (interval[1] <= item[1] and interval[1]>= item[0]):
							flag = False
							continue
				if flag:
					existedIntervals.append(interval)
					result.append(interval)
		# print result,newIntervals
		return result,existedIntervals









