import jieba
import jieba.posseg as pseg
import re
import cn2an as ca


# dictionary to manually fix homophones
def homophone_replace():
	input = '牙吗？写是这里一情的一个很大的问题'
	homophoneDict = {'牙吗？写':'亚马逊', '一情':'疫情'}
	for k in homophoneDict:
		input = input.replace(k, homophoneDict.get(k))
	print(input)
# add more as I find them


# fix issues like 90%三 or 1000 1
def percentage_repair():
	# inputFile = open('sample.txt', 'r')
	# outputFile = open('sample.txt', 'r')
	input = '特别1000 1是海洋变温还养吸收了90%三的多余能量'
	output = ''
	tokens = jieba.lcut(input, cut_all=False)
	tokensCopy = tokens[:]
	for i in tokensCopy:
		#fix numbers
		if i.isnumeric():
			if tokensCopy[tokensCopy.index(i) + 1] == ' ' and tokensCopy[tokensCopy.index(i) + 2].isnumeric():
				x = int(i)
				y = int(tokensCopy[tokensCopy.index(i) + 2])
				tokens.remove(tokens[tokens.index(i) + 2])
				tokens.remove(tokens[tokens.index(i) + 1])
				tokens[tokens.index(i)] = str(x + y)
		#fix percentages
		elif re.search('%', i) and tokensCopy[tokensCopy.index(i) + 1].isnumeric():
			x = int(i.replace('%', ''))
			y = int(ca.transform(tokensCopy[tokensCopy.index(i) + 1], 'cn2an'))
			tokens.remove(tokens[tokens.index(i) + 1])
			tokens[tokens.index(i)] = str(x + y) + '%'
	for i in tokens:
		output += i
	print(output)


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
# do something with time words


# 的 sentence breaks
def de_sentence_breaks():
	input = '中国还没有加入任何为推动生物多样性为保护目标成立的主要联盟，中国也没有签署领导人对自然的承诺，而该校园中有约60位。政治家承诺采取有益的行动来解决地球紧急情况，' \
		'发过生态开发署生态转型负责人克莱斯表示，到目前为止，我们很少与生态环保的外交层面上看到中国，在经济转型上中国很少或者根本就没有参与，中共可能会继续尽可能的在生态保护领域' \
		'上保持中立态度，因为分析指出，对中国来说，最重要的似乎在2020年春天通过一个可以实施的。生态环境全球框架西方人正在推动一项雄心勃勃的生态环境学约，但是中国人首先想是实现承诺，'\
		'这是北京要想在本次昆明生态的约方必须达到承诺10年前在日本通过自在智识生物多样性丧失的爱织目标的20个目标到目前均未实现'
	output = ''
	# right side of target substring
	rightPlaceholder = input[input.find('的。'):]
	rightPlaceholder = rightPlaceholder[2:]
	if rightPlaceholder.find('，') > rightPlaceholder.find('。'):
		rightPlaceholder = rightPlaceholder[:rightPlaceholder.find('，')]
	elif rightPlaceholder.find('，') < rightPlaceholder.find('。'):
		rightPlaceholder = rightPlaceholder[:rightPlaceholder.find('。')]
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
	# this puts tokens + POS into list
	words = pseg.cut(targetSubstring)
	segmentPOS = []
	for i in words:
		segmentPOS.append([i.word, i.flag])
	for i in segmentPOS:
		print(i)

	# error as flag variable, if error, place '。' at end of targetSubstring, if no error, place '。' after 的. then, attach to output
	errorFlag = False
	segmentCopy = segmentPOS[:]
	for i in segmentCopy:
		if i[0] == '的' and segmentCopy[segmentCopy.index(i)+1][0] == '。':
	# if only sub + verb, likely error
		# if noun + verb then de, likely error
	# If has 和 before preceding noun, likely error
		# basically loop through look for 和, between 和 and 的 only nouns then errorFlag = True

	# then after this, repeat for subsequent chunks of code if need be
	# numOccurrence = input.count('的。')
	# for i in range(numOccurrence):

	# maybe some kind of broader analysis is needed? constituency parsing?


#playing with constituency parsing
import stanza
nlp = stanza.Pipeline(lang='zh', processors='tokenize,pos,constituency')
doc = nlp(targetSubstring)
for sentence in doc.sentences:
	print(sentence.constituency)