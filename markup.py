import jieba
import jieba.posseg as pseg
import re
import cn2an as ca


# dictionary to manually fix homophones
def homophone_replace(input):
	homophoneDict = {'牙吗？写':'亚马逊', '一情':'疫情', '吧。已知85':'85%', '是。':'是', 'G，六':'第六', '区周':'欧洲', '1美元':'亿美元',
					 '该纳电影节':'戛纳电影节', '30% 1921年':'30%。1921年', '一点，十':'一点事','写森林砍伐与':'写森林砍日益',
					 '台中的重要一部':'台在减排中的重要一部','杨盛曾':'杨海洋盛曾','我们从':'欧盟从','你听政府':'各位听众政府','你要对老年':'疫苗对老年人','code 15':'抠破15'}
	for k in homophoneDict:
		input = input.replace(k, homophoneDict.get(k))
	return(input)


# fix issues like 90%三 or 1000 1
def percentage_repair(input):
	output = ''
	# put words from input into a list
	tokens = jieba.lcut(input, cut_all=False)
	tokensCopy = tokens[:]
	for i in tokensCopy:
		# fix numbers
		# code is messy, but essentially identifies if an error like 1000 1 is present and then repairs it by adding the numbers together
		if i.isnumeric():
			try:
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
			except IndexError:
				pass
		# fix percentages
		# similar to the above code, but for percentages
		elif re.search('%', i):
			try:
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
				elif tokensCopy[tokensCopy.index(i) + 1] == '期':
					tokens.remove(tokens[tokens.index(i) + 1])
					tokens[tokens.index(i)] = str(int(i.replace('%', '')) + 7) + '%'
				elif tokensCopy[tokensCopy.index(i) + 1] == '点' and tokensCopy[tokensCopy.index(i) + 2].isnumeric():
					x = int(ca.transform(tokensCopy[tokensCopy.index(i) + 2], 'cn2an'))
					tokens.remove(tokens[tokens.index(i) + 2])
					tokens.remove(tokens[tokens.index(i) + 1])
					tokens[tokens.index(i)] = i + '.' + str(x) + '%'
			except IndexError:
				pass
	# fill output string with corrected transcript and return
	for i in tokens:
		output += i
	return(output)


# 的/第 issue
def ordinal_numbering(input):
	output = ''
	# put words from input into a list
	tokens = jieba.lcut(input, cut_all=False)
	tokensCopy = tokens[:]
	for i in range(len(tokensCopy)):
		# identify the presence of 的 and repair if it is incorrect
		if tokensCopy[i] == '的':
			try:
				# if preceded by the preposition 在
				if tokensCopy[i - 1] == '在':
					tokens[i] = '第'
				# if beginning of clause and precedes a number
				elif (tokensCopy[i - 1] == '，' or tokensCopy[i - 1] == '。') and tokensCopy[i + 1].isnumeric():
					tokens[i] = '第'
				# if followed by a number and then the character 次, which means time. like, "the first time"
				elif tokensCopy[i + 1].isnumeric() and tokensCopy[i + 2] == '次':
					tokens[i] = '第'
				# if beginning of a phrase like "first, ..."
				elif tokensCopy[i + 1].isnumeric() and tokensCopy[i + 2] == '，':
					tokens[i] = '第'
			except IndexError:
				pass
	# fill output string with corrected transcript and return
	for i in tokens:
		output += i
	return(output)


# 的 sentence breaks
def de_sentence_breaks(input):
	output = ''
	# first identify if 的。 is present, then loop through for each time it occurs
	# this is to make sure that all instances of 的。 receive analysis, not just the first one
	numOccurrence = input.count('的。')
	if numOccurrence > 0:
		for i in range(numOccurrence):
			# goal is to isolate the substring containing 的。 and pass everything else into the output
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
			# error is a 'flag' variable. if error, place '。' at end of targetSubstring, if no error, place '。' after 的.
			# then, attach to output and continue for the rest of the input file
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
	return(output)
# tags are provided by jieba, I tried to include all instances (like a noun as a pronoun, proper noun, etc) but they may need to be updated