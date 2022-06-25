import jieba
import jieba.posseg as pseg


# 的/第 issue
def ordinal_numbering():
	#inputFile = open('sample.txt', 'r')
	#outputFile = open('sample.txt', 'r')
	inputFile = '的一，在官方车队中60%的车辆是电动或者混合动力汽车组成的二进行广告非实体化减少印刷量，甚至禁止专用各类电影推销的资料已经完全数字。华从让戛纳电影节的纸张使用量比此前减少了50%在第七十四届戛纳电影节期间已经完全取消塑料瓶和塑料杯的使用来减少塑料对环境的污染，今年会持续同样的措施，因为各路明星在电影节期间晚上登上的红地毯已经用可回收材料制成，而且减少了50%的行量，电影节首次对回收红地毯进行长期循环使用进行了测试，在2021年回收了2600多功能的红毯进行循环使用的五还推出了负责任的餐厅饮食措施，会外卖店尽量使用当地的新鲜食材，减少食品浪费在戛纳电影节这个密集人流区清理垃圾的专业企业，帮助戛纳杰电影宫收集和回收垃圾，配备各类垃圾。迪亚时期减少了垃圾的体积，提高了回收垃圾的效率，如在2021年电影节期间产生的250吨垃圾中百人之99得到了回收和再利用，现身戛纳电影节的电工内实行垃圾分类等不同的环保举措取得了成功，从2019年到2021年分列垃圾达到30% 1921年，所有在戛纳电影节的参与者都交付了一笔环保分摊金来补偿，开车前往参加电影节和在电价住宿期间时候的碳排放行期限是。'
	outputFile = ''
	segmentList = list(jieba.cut(inputFile, cut_all=False))
	for i in segmentList:
		if i != '的':
			# outputFile.write(i)
			outputFile += i
		else:
			if segmentList[segmentList.index(i) - 1] == '在':
				outputFile += '第'
			elif (segmentList[segmentList.index(i) - 1] == '，' or segmentList[segmentList.index(i) - 1] == '。') and \
					segmentList[segmentList.index(i) + 1].isnumeric():
				outputFile += '第'
			elif segmentList[segmentList.index(i) + 1].isnumeric() and segmentList[segmentList.index(i) + 2] == '次':
				outputFile += '第'
			elif segmentList[segmentList.index(i) + 1].isnumeric() and segmentList[segmentList.index(i) + 2] == '，':
				outputFile += '第'
			else:
				outputFile += i
	print(inputFile)
	print(outputFile)
	return outputFile
# do something with time words


# 的 sentence breaks
def de_sentence_breaks():
# input/output
input = '中国还没有加入任何为推动生物多样性为保护目标成立的主要联盟，中国也没有签署领导人对自然的承诺，而该校园中有约60位。政治家承诺采取有益的行动来解决地球紧急情况，' \
	'发过生态开发署生态转型负责人克莱斯表示，到目前为止，我们很少与生态环保的外交层面上看到中国，在经济转型上中国很少或者根本就没有参与，中共可能会继续尽可能的在生态保护领域' \
	'上保持中立态度，因为分析指出，对中国来说，最重要的似乎在2020年春天通过一个可以实施的。生态环境全球框架西方人正在推动一项雄心勃勃的生态环境学约，但是中国人首先想是实现承诺，'\
	'这是北京要想在本次昆明生态的约方必须达到承诺10年前在日本通过自在智识生物多样性丧失的爱织目标的20个目标到目前均未实现'
output = ''

# targetSubstring is clauses to the left and right of '的。' when we see it occur, placeholders help accomplish this
targetSubstring = ''
leftPlaceholder = ''
rightPlaceholder = ''

# left side of target substring
leftPlaceholder = input[0: input.find('的。')]
leftPlaceholder += '的'
if leftPlaceholder.rfind('，') > leftPlaceholder.rfind('。'):
	leftPlaceholder = leftPlaceholder[leftPlaceholder.rfind('，'):]
elif leftPlaceholder.rfind('，') < leftPlaceholder.rfind('。'):
	leftPlaceholder = leftPlaceholder[leftPlaceholder.find('。'):]
leftPlaceholder = leftPlaceholder[1:]

# right side of target substring
rightPlaceholder = input[input.find('的。'):]
rightPlaceholder = rightPlaceholder[2:]
if rightPlaceholder.find('，') > rightPlaceholder.find('。'):
	rightPlaceholder = rightPlaceholder[:rightPlaceholder.find('，')]
elif rightPlaceholder.find('，') < rightPlaceholder.find('。'):
	rightPlaceholder = rightPlaceholder[:rightPlaceholder.find('。')]

# put them together, '。' following 的 has been deleted
targetSubstring = leftPlaceholder + rightPlaceholder

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
for i in segmentPOS:
# if only sub + verb, likely error
# If has 和 before preceding noun, likely error


# then after this, repeat for subsequent chunks of code if need be
# numOccurrence = input.count('的。')
# for i in range(numOccurrence):


# If has 和 before preceding noun, likely error
# basically loop through look for 和, between 和 and 的 only nouns then errorFlag = True
# if only sub + verb, likely error
# if noun + verb then de, likely error




# maybe some kind of broader analysis is needed? constituency parsing?