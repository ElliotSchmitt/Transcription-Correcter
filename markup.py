import jieba
import jieba.posseg as pseg
import re
import cn2an as ca


# dictionary to manually fix homophones
def homophone_replace():
	input = '牙吗？写是这里一情的一个很大的问题80%期'
	homophoneDict = {'牙吗？写':'亚马逊', '一情':'疫情', '吧。已知85':'85%', '是。':'是', '80%期':'87%', 'G，六':'第六', '区周':'欧洲'}
	for k in homophoneDict:
		input = input.replace(k, homophoneDict.get(k))
	print(input)
# add more as I find them


# fix issues like 90%三 or 1000 1
def percentage_repair():
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
	input = '然后果的26家气候峰会11月13日在格拉斯哥落下帷幕，然后国秘书长古特雷斯在大会结束时声明说此次峰会慢出了重大的一部，但这还并不足够，应该加快行动才能够达到1.5度的目标，而对瑞典期货活动分子格蕾塔灯般来说的26家气候峰会又是一次空话连篇的峰会，那么此次峰会究竟是否取得了一些具体的进展，古特雷斯所谓迈出的重大一步指的是什么，人们对此次峰会的反应为何有如此巨大的落差，就以上问题，我们综合各方专家的总结，以及法广在格拉斯哥峰会现场的将来向大家做一个综述，说先就格拉斯哥峰会的成就一部族法国可持续发。讲一国际关系研究学院的气候项目专家罗拉玛丽和女士的总结和为中看，他认为此次峰会虽然在援助贫穷国家方面存在严重不足，但是依然取得了许多具体的进展，这些进展主要体现在印度11日，利亚先后宣布了将在2010年和2016年年打到碳中和，从而使全球制的坦诚和时间表的国家增加至81个，各国承诺将在明年年底之前重新调整在2030年前的减排指标峰会，虽然在融资方面并未取得具体进展，哥本哈根峰会时承诺的每年1000美元的援助资金依然缺少210，不过各国承诺将在2023年之前达到融资目标，格拉斯哥峰会的第2大成果就是明确提出逐步减低对化石燃料的资金援助，这是联合国气候协议中首次明确的提出，上述要求虽然这一幕。目前仅仅停留在象征性的一部，因为各国尚未被要求制定出具体的时间表，化石燃料的燃烧是全球75%的温室气体的来源，和目前全球各国对化石能源的开发援助总金额高达6000亿美元，峰会期间与丹麦，哥斯达黎加为首的40多个国家签署了停止援助化石能源开发的协议，明年气候峰会的东道国爱级在此领域可以起到积极的作用，以及在2013年至2017年期间将化石能源的资助金额减低了60%格拉斯哥峰会的第3大成就，就是完成了巴黎协定的实施细则，这从程序上来看要比2018年的芬兰卡特拉斯峰会于2019年大马德里峰会要走得更远，具体而言就是格拉斯哥峰会终于救巴黎协定中最引发争议的第6条的落是达成了协议。第6条之所以引发争议，正是因为协议的落实，对不同的利益团体不同的国家将产生不同的经济后果，它的具体落实对全球减低碳排放究竟是否能够起到积极的作用，答案是仁者见仁智者见智，这也是格拉斯哥峰会最终不得不延迟一天的主要原因，那么巴黎协定中的第6条的弱势究竟为何引发如此巨大的争议，我们来听听中国气候谈判专家，中国国家气候变化专家委员会副主任王毅先生的解释第6条件核心的问题就是单质量对于主要是养用市场经济的方法来不断的去降低我们的简单成本，而这其中一天就是碳排放能源交易机制，它就是一个核心内容，是怎么样的一个让要构建议更好的碳排放交易鸡翅，怎么把现有的一些已经纳入的NPC对些目标能够将来能够进入。女市长中国市场交易办法来确定一个碳的价格，使我们未来的建材成本能够更加强的同时呢，如果提高我们的减排的效率，这是一个最基本的重要的经济机制，所有这个里头有就有很多的争议，就是比如说我们现在的有的一些cdn项目，包括现在已有的一些NPC的，救国家自主贡献这些指标，而是不是可以纳入的探员，长野范围怎么画，对比例怎么调，需要那个国家对此还是有不同的认识的，而且个体由于条件不同台，比如说他也没有办法，现在展示能够建立一个全球场上，而即使这样的话，有可能有这个所谓的public key就是这个碳的，这个这个泄漏可能他会把那个成本低的地方去找啊就有，所以这样的话他可能也涉及到一些不公平的问题，也包括发达国家，发展中国家，而这些问题都需要我们进一步处理并且载的。巴黎协定的执行，其实施细则当中要把它固定下来，变成一个可以具有法律约束力的一个一个条款，能够供我们大致的说一下第6条探机制里面目前谈判各方的主要的分歧是什么，然后哪些国家是出什么样的主张就准备技术也太巧了，我就大概说的就是你哪些东西要纳入到菜市场里头去，比如说举个例子来讲，对于中国人中对中国人来讲究中国的话，现在中国的坦然只有电力行业纳入进来了，光的电话张力还是不够，那么下一步是不是要把这个其他的可再生能源行业那天来的范围怎么去华定，这就是一个比较大的第2医院，就是我们已经取得的一些减排的一些效果，比如说我们过去说的cdm就是所有清洁发展机制或者现在的NPC界国家的自主贡献里头，他涉及到的。减排的一些对葛亮是不是可以变成一个简单信用，能够加入到太原来可以交易，要比如果中的述了中的书单有这个能够形成的碳汇了，那我姓这个行程的一个流量能不能也都要纳入的市场，就这是需要那个比较明确的这个规定的，而特别是说我需要就是这个周，这谁看下它并不是一个纯纯的自由市场大还是一个人认为的是长，因为他对你哪些东西纳入进去的定价怎么了，考虑配额怎么去分配法，随着里都是一道很多的规则的制定的规则，非常希望能够更加公平，而是最后的约旦家能够真正起到作用的，真正能够促进减排，能够提高效率，降低成本，这是我们希望达到的一个目的，确实让易先生点出了问题的关键所在，那就是碳补偿机制是否真的能够起到减低碳排放的作用太复杂。其次，是否会将气候谈判转变成一个金融投资者讨价还价的最大的国际市场，此次气候峰会上，金融机构的代表人用的总数远远高于以往的气候峰会绝非偶然，这也是个大环境组织的担忧所在，身上京都协定实施之后，碳市场在欧美发达国家早已启动，中国也在最近几年来持续了太市场试验，并且正在设立全国碳市场网络，那么设立碳市场机制对减低温室气体的排放是否已经起到了切实的作用，多年来活跃在联合国气候谈判会场的联合国政府间气候变化专家小组副主席让如此而先生这样向法官表示与社会隔膜洗不掉，那你说说市场确实可以减低排放，但是条件是不能够做双重计算，就是会议，目前正在谈判的交点碳市场一直被认为是。点击态排放的主要手段，但是令我感到失望的是，我们看到碳机制并不能够起到足够的减排作用，在欧洲他或许确实起到了一定的作用，但是在中国中国也有地方太市场，甚至也有全国性的碳市场，但是我们看到坛机制并没有起到减排的作用，因为否则的话，中国的太胖胖就不会增加，所以态补偿机制必须十分谨慎和认为G，六条的落实将10分困难，因为它的难点就在于必须切实的导致胎盘上的减少，而不仅仅是太排放的转移，我不会进入具体的细节，这就是第6条的潜在威胁也是问题的焦点，所在的行驶速度不如者先生所说的双重计算指的是国际转让的减排成果，同时对买卖双方用于实现国家的自主贡献减排承诺，比如说。亚马逊集团为减低它的排放量，在印尼种植的10000公顷的树木，这些树木匠可以吸收一定数量的二氧化钛，但是这些氧化碳不能同时也算入亚马逊集团与印尼的减排成绩中，从以上的例子中我们就可以看出太市场机制可以促进企业为了经济效益而减低排放，但是同时也允许企业出钱购买太太坊，也就是说只要有钱就可以堂而皇之的牌坊，此次峰会上许多高排放企业都做出了在2050年左右达到碳中和的目标，很显然碳市场的运作为污染企业带来了表率的可能性，由此可见叹气滞胃泰排放大国以及高排放的企业找到了一个熟醉的台阶，那么那些遭受气候变化后果严重影响的国家，对此有何看法呢，我们来听听这得土族人妇女协会的唱。人的理学这一布拉欣女士的看法，他在接受法国文化电台采访时这样表示比爸爸回家去mathematics and didnt work early devonian们在谈论气候变化时不能够回比饮水权，住房权以及能源全等最基本的人权问题，再回到此次峰会上广泛引发关注的巴黎协定中的第6条的问题，这次峰会上主要落实了第6条中的三点的链条的第2点，指的是如何联系落实差交易金似点指的是通过何种方式出手，太的8点指的是如何设立一个系统，对整个过程进行监督，监督他是否注重人权，因为这是我们当初在巴黎协定的制定时特别强调的一点，因为倘若在整个过程中当地人的基本人权没有获得尊重的话，那么碳市场就只会是外界所说的表率市场。这将对我们带来致命的伤害是因为此次峰会的人权组织，环保组织的共同担忧11月12日格拉斯哥峰会举行闭幕大会的同时，多个非政府组织人权组织在大会会场的对面召开记者会，谴责此次峰会将气候谈判转变成一个发达国家，跨国集团一旦补偿为有收购贫困国家的贸易市场，从气候谈判几10年来的经验来看，他们的担忧或许并非空穴来风的荣耀与上的环境发展节目为您盘点了Galaxy S7和峰会的成果以失败，并且重点介绍了此次公会的焦点话题，巴黎协定中的第6条的落实，本次节目受杨梅采购，要感谢孙飞鸟与鱼力的技术合作，更感谢各位的收听，我们下次节目再会'
	output = ''
	numOccurrence = input.count('的。')
	if numOccurrence > 0:
		for i in range(numOccurrence):
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
			remainder = input.replace(output, '')
			remainder = remainder.replace(targetSubstring, '')
			# this puts tokens + POS into list
			words = pseg.cut(targetSubstring)
			segmentPOS = []
			for i in words:
				segmentPOS.append([i.word, i.flag])
			# error as flag variable, if error, place '。' at end of targetSubstring, if no error, place '。' after 的. then, attach to output
			errorFlag = False
			segmentCopy = segmentPOS[:]
			for i in range(len(segmentCopy)):
				if segmentCopy[i][0] == '的' and segmentCopy[i+1][0] == '。':
					#If has 和 before preceding noun, likely error
					if segmentCopy[i-1][1] == 'n' and segmentCopy[i-2][0] == '和':
						errorFlag = True
						#remove period, throw at end
						break
					#If no noun before period, noun following period, then error
					elif segmentCopy[i+2][0] == 'n' or segmentCopy[i+2][0] == 'l':
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
					# need to refine this
					else:
						x = 0
						temp = segmentCopy[:i]
						for j in reversed(temp):
							if j[1] == 'v':
								x+=1
							elif j[1] == 'r' or j[1] == 'n':
								break
						if x > 0:
							errorFlag = True
							break
			if errorFlag:
				targetSubstring = targetSubstring.replace('。', '')
				targetSubstring += '。'
			output += targetSubstring
			output += remainder[1:]

	print(output)
	# then after this, repeat for subsequent chunks of code if need be
		# remove chunks from input as I assemble them into remainder/targetSubstring??
	# only run errorFlag chunk if 。的 was found in the first place
	# within errorFlag chunk account for all possible tags
	# maybe some kind of broader analysis is needed? constituency parsing?





def bookmark():
	input = '有可能有这个所谓的public key就是这个碳的，这个这个泄漏可能他会把那个成本低的地方去找啊就有，所以这样的话他可能也涉及到一些不公平的问题，也包括发达国家，发展中国家，而这些问题都需要我们进一步处理并且载的。巴黎协定的执行，其实施细则当中要把它固定下来，变成一个可以具有法律约束力的一个一个条款。比如说我们过去说的cdm就是所有清洁发展机制或者现在的NPC界国家的自主贡献里头，他涉及到的。减排的一些对葛亮是不是可以变成一个简单信用，能够加入到太原来可以交易，要感谢孙飞鸟与鱼力的技术合作，更感谢各位的收听，我们下次节目再的。要感谢孙飞鸟与鱼力的技术合作，'
	output = ''
	numOccurrence = input.count('的。')
	if numOccurrence > 0:
		for i in range(numOccurrence):
			errorFlag = False
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
			input = input.replace(output, '')
			input = input.replace(targetSubstring, '')
			# this puts tokens + POS into list
			words = pseg.cut(targetSubstring)
			segmentPOS = []
			for i in words:
				segmentPOS.append([i.word, i.flag])
			# error as flag variable, if error, place '。' at end of targetSubstring, if no error, place '。' after 的. then, attach to output
			segmentCopy = segmentPOS[:]
			for i in range(len(segmentCopy)):
				if segmentCopy[i][0] == '的' and segmentCopy[i+1][0] == '。':
					#If has 和 before preceding noun, likely error
					if segmentCopy[i-1][1] == 'n' and segmentCopy[i-2][0] == '和':
						errorFlag = True
						#remove period, throw at end
						break
					#If no noun before period, noun following period, then error
					elif segmentCopy[i+2][0] == 'n' or segmentCopy[i+2][0] == 'l':
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
					# need to refine this
					else:
						x = 0
						temp = segmentCopy[:i]
						for j in reversed(temp):
							if j[1] == 'v':
								x+=1
							elif j[1] == 'r' or j[1] == 'n':
								break
						if x > 0:
							errorFlag = True
							break
						break
			if errorFlag:
				targetSubstring = targetSubstring.replace('。', '')
				targetSubstring += '。'
				output += targetSubstring
				input = input[1:]
			else:
				output += targetSubstring
				input = input[1:]
	else:
		return input
	return
#works for 2 unless third 的。 at end of document
#why repeating chunks?