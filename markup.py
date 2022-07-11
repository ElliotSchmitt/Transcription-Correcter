import jieba
import jieba.posseg as pseg
import re
import cn2an as ca


# dictionary to manually fix homophones
def homophone_replace(input):
	homophoneDict = {'牙吗？写':'亚马逊', '一情':'疫情', '吧。已知85':'85%', '是。':'是', '80%期':'87%', 'G，六':'第六', '区周':'欧洲'}
	for k in homophoneDict:
		input = input.replace(k, homophoneDict.get(k))
	print(input)
# add more as I find them


# fix issues like 90%三 or 1000 1
def percentage_repair(input):
	# inputFile = open('sample.txt', 'r')
	# outputFile = open('sample.txt', 'r')
	input = '而绿地的保护面积达到了七 11，这时'
	output = ''
	tokens = jieba.lcut(input, cut_all=False)
	tokensCopy = tokens[:]
	for i in tokensCopy:
		# fix numbers
		if i.isnumeric():
			if tokensCopy[tokensCopy.index(i) + 1].isnumeric():
				x = int(ca.transform(i, 'cn2an'))
				y = int(ca.transform(tokensCopy[tokensCopy.index(i) + 1], 'cn2an'))
				tokens.remove(tokens[tokens.index(i) + 1])
				tokens[tokens.index(i)] = str(x + y)
			elif (tokensCopy[tokensCopy.index(i) + 1] == ' ' and tokensCopy[tokensCopy.index(i) + 2].isnumeric()):
				x = int(ca.transform(i, 'cn2an'))
				y = int(ca.transform(tokensCopy[tokensCopy.index(i) + 2], 'cn2an'))
				tokens.remove(tokens[tokens.index(i) + 2])
				tokens.remove(tokens[tokens.index(i) + 1])
				tokens[tokens.index(i)] = str(x + y)
		# fix percentages
		elif re.search('%', i):
			if tokensCopy[tokensCopy.index(i) + 1].isnumeric():
				x = int(i.replace('%', ''))
				y = int(ca.transform(tokensCopy[tokensCopy.index(i) + 1], 'cn2an'))
				tokens.remove(tokens[tokens.index(i) + 1])
				tokens[tokens.index(i)] = str(x + y) + '%'
			elif tokensCopy[tokensCopy.index(i) + 1] == ' ' and tokensCopy[tokensCopy.index(i) + 2].isnumeric():
				x = int(ca.transform(tokensCopy[tokensCopy.index(i) + 2], 'cn2an'))
				tokens.remove(tokens[tokens.index(i) + 2])
				tokens.remove(tokens[tokens.index(i) + 1])
				tokens[tokens.index(i)] = str(x) + '%'
	for i in tokens:
		print(i)
#out of range when number is at end of string


# 的/第 issue
def ordinal_numbering():
	#inputFile = open('sample.txt', 'r')
	#outputFile = open('sample.txt', 'r')
	input = '为了减少对环境的污染，在的74家看看电影节期间大量减少用电量。同样在今年的75届戛纳电影节期间会继续实施如下具体措施来减少对当地环境的污染的一，在官方车队中60%的车辆是电动或者混合动力汽车组成的二进行广告非实体化减少印刷量，'
	output = ''
	tokens = jieba.lcut(input, cut_all=False)
	tokensCopy = tokens[:]
	for i in range(len(tokensCopy)):
		if tokensCopy[i] == '的':
			if tokensCopy[i - 1] == '在':
				tokens[i] = '第'
			elif (tokensCopy[i - 1] == '，' or tokensCopy[i - 1] == '。') and tokensCopy[i + 1].isnumeric():
				tokens[i] = '第'
			elif tokensCopy[i + 1].isnumeric() and tokensCopy[i + 2] == '次':
				tokens[i] = '第'
			elif tokensCopy[i + 1].isnumeric() and tokensCopy[i + 2] == '，':
				tokens[i] = '第'
	for i in tokens:
		output += i
	print(output)


# 的 sentence breaks
def de_sentence_breaks():
	input = '来保护当地自然环境和居民的。健康因为新冠疫情大流行一年后导致的74届戛纳电影节推迟举行'
	output = ''
	numOccurrence = input.count('的。')
	if numOccurrence > 0:
		for i in range(numOccurrence):

			# right side of target substring
			rightPlaceholder = input[input.find('的。'):]
			rightPlaceholder = rightPlaceholder[2:]
			if rightPlaceholder.find('，') > rightPlaceholder.find('。'):
				rightPlaceholder = rightPlaceholder[:rightPlaceholder.find('。')]
			elif rightPlaceholder.find('，') < rightPlaceholder.find('。'):
				rightPlaceholder = rightPlaceholder[:rightPlaceholder.find('，')]

			# left side of target substring
			leftPlaceholder = input[0: input.find('的。')]
			leftPlaceholder += '的'
			if leftPlaceholder.rfind('，') > leftPlaceholder.rfind('。'):
				leftPlaceholder = leftPlaceholder[leftPlaceholder.rfind('，'):]
			elif leftPlaceholder.rfind('，') < leftPlaceholder.rfind('。'):
				leftPlaceholder = leftPlaceholder[leftPlaceholder.find('。'):]
			leftPlaceholder = leftPlaceholder[1:]

			# put them together, '。' following 的 has been included
			targetSubstring = leftPlaceholder + '。' + rightPlaceholder

			# everything until target string goes into output
			output += input[0:input.index(targetSubstring[0:4])]
			input = input.replace(input[0:input.index(targetSubstring[0:4])], '')
			input = input.replace(targetSubstring, '')

			# this puts tokens + POS into list
			words = pseg.cut(targetSubstring)
			segmentPOS = []
			for i in words:
				segmentPOS.append([i.word, i.flag])

			# error as flag variable, if error, place '。' at end of targetSubstring, if no error, place '。' after 的. then, attach to output
			segmentCopy = segmentPOS[:]
			errorFlag = False
			for i in range(len(segmentCopy)):
				if segmentCopy[i][0] == '的' and segmentCopy[i+1][0] == '。':

					#If has 和 before preceding noun, likely error
					if segmentCopy[i-1][1] == 'n' and segmentCopy[i-2][0] == '和':
						errorFlag = True
						#remove period, throw at end
						break

					#If no noun before period, noun following period, then error
					#checks for noun following 。, then if there is no noun preceding 。then errorFlag = True
					elif segmentCopy[i+2][1] == 'n' or segmentCopy[i+2][1] == 'l' or segmentCopy[i+2][1] == 'nr' or segmentCopy[i+2][1] == 'nd' or segmentCopy[i+2][1] == 'r':
						flag = True
						temp = segmentCopy[:i]
						for j in temp:
							if j[1] == 'n':
								flag = True
							else:
								flag = False
						if flag == False:
							errorFlag = True
							break

					#If no object of sentence, then error
					#works by iterating backwards and if finds verb before noun then no object in chunk preceding 。
					else:
						x = 0
						temp = segmentCopy[:i]
						for j in reversed(temp):
							if j[1] == 'v':
								x+=1
							elif j[1] == 'r' or j[1] == 'n' or j[1] == 'nr' or j[1] == 'nd' or j[1] == 'r':
								break
						if x > 0:
							errorFlag = True
							break
						break

			#repair sentence, attach to output, strip input and continue
			if errorFlag:
				targetSubstring = targetSubstring.replace('。', '')
				targetSubstring += '。'
				output += targetSubstring
				input = input[1:]
			else:
				output += targetSubstring
				input = input[1:]
		output += input
	#return output
	else:
		output = input
	print(output)
#works now! but, omits final char sometimes... why? shuouldn't be na issue?? we'll see





