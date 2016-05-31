#!/usr/bin/env python3

# Код НЕ оптимален с точки зрания производительности.
# Такты НЕ экономим, это программа не на C++,
# и работает она не на атомной электростанции.
# Максимум внимания расширяемости, читаемости и корректности.

import math
import re
import csv

global glob

'''CONSTANTS''' #---------------------------------

number = {	#Наборы констант для работы с числами
	'power':{
		'min':1e-3,	#Минимальное значение, которое не будет преобразовано в представление X \cdot 10^{power}
		'max':1e4,	#Максимальное значение, которое не будет преобразовано в представление X \cdot 10^{power}
		},
	'float':{
		'del':',',	#Десятичный разделитель
		'dad':3,	#Количество значащих цифр после десятичного разделителя # Digits After Delimiter
		},
}

#---------------------------------

parser = {	#Набор констант для парсера выражений
	'pair':{	#Парные знаки, требующие рекурсивной обработки выражения
	'(':')',
	'[':']',
	'{':'}',
	'\'':'\'',
	'\"':'\"',
	#'':'',
	},
	'str':['\'','\"'],	#Символы, обозначающие строку. Будем хранить их в одном месте
	'delimiters':['.',',',],	#Возможные весятичные разделители
	'opsign':['+','-','*','/','**','^',],	#Знаки арифметических операций
	'skipsign':[' ','\t','\n',],	#Пропускаемые парсером символы
}

outputfilename = 'lapy.out'

'''FUNCTIONS''' #---------------------------------

def __parse__(expr):
	return(__structurize__(__tokenize__(expr)))

def __structurize__(tokens):	#Парсер 2го уровня. Преобразует набор токенов в структуры. На нём лежит задача выделения в структуры переменных, функций, условий.
	struct = []
	return(tokens)

def __tokenize__(expr):	#Парсер 1го уровня. Преобразует набор символов в набор токенов.
	#Парсер очень наивен и совсем не переваривает ошибок. Давайте не будем его расстраивать
	expr = expr.replace('**','^')	#Костыль, исправляющий обработку возведения в степень
	expr += ' ' #Костыль, позволяющий не беспокоиться о выходе за пределы массива. По уму: try + except или отдельная обработка последнего символа
	in_len = len(expr)
	tokens = []
	prevpointer = pointer = openpairs = 0
	while (pointer < in_len):
		if (expr[pointer] in parser['pair'].keys()):	#Какой-то из парных символов
			tokens.append(expr[pointer])	#Добавим сам символ
			openpair = expr[pointer]	#Ищем пару именно этому символу, остальные игнорируем
			pointer += 1
			openpairs += 1
			prevpointer = pointer
			while ((openpairs != 0) and (pointer < in_len)):
				pointer += 1
				if (expr[pointer] == openpair):
					openpairs += 1
				elif (expr[pointer] == parser['pair'][openpair]):
					openpairs -= 1
			if (openpairs != 0):
				#pass #FIXME: Антон, придумай, как обработать такой кейс
				raise Exception("Parsing Error!")	#Придумал. Падать должно громко (и больно)
			if (openpair in parser['str']):
				tokens.append(expr[prevpointer:pointer])	#Если это строка, зачем её парсить?
			else:
				tokens.append(__parse__(expr[prevpointer:pointer]))	#We must go deepper!
			tokens.append(expr[pointer])	#И символ закрытия тоже включим
			pointer += 1
		elif (expr[pointer] in parser['opsign']):
			#FIXME: Операция возведения в степень пойдёт по 3.14'зде. Костыль: .replace('**','^')
			tokens.append(expr[pointer])
			pointer += 1
		elif (expr[pointer] in parser['skipsign']):	#Нужно для работы костыля, решающего проблему доступа к элементу вне массива
			pointer += 1	#Может, следует выполнить .replace(symbol)?
		else:	#Пытаемся разделить переменные, константы, людей, коней...
				prevpointer = pointer
				if (expr[pointer].isalpha()):	#Обнаружена переменная
					#FIXME: R[10] Тоже переменная. Кстати, возможно, всё в порядке.
					while(expr[pointer].isalnum() or expr[pointer] == '_'):		#В состав переменной могут входить буквы, цифры и нижний слэш
						pointer += 1
					tokens.append(expr[prevpointer:pointer])
				elif (expr[pointer].isdigit()):	#Обнаружено число
					while(expr[pointer].isdigit() or expr[pointer] in parser['delimiters']):
						pointer += 1
					try: tokens.append(int(expr[prevpointer:pointer]))	#Минимум строк говнокода, максимум концентрации
					except ValueError: tokens.append(float(expr[prevpointer:pointer].replace(',','.')))
				else:	#А тут у нас и не буква, и не цифра, а неведома зверушка. Добавим её, не зря же она тут
					tokens.append(expr[pointer])
					pointer += 1
	return (tokens)

def __str2data__(obj):
	try:
		return(int(obj))
	except Exception:
		try: 
			return(float(obj.replace(',','.')))
		except Exception:
			return(obj)

#---------------------------------
#турум-пум-пум APIлки!

def lapyout(obj):
	with open(outputfilename, mode='w', encoding='utf-8') as outfile:
		outfile.write(obj)

def lapystr(obj): lapyout(str(obj))

def lapyval(obj): lapyout(val(obj))

def lapytable(**obj): lapyout(table2latex(**obj))

def lapycsvtable(path): lapyout(mkcsvtable(path))

#---------------------------------

def val(obj):
	latex = None
	if (type(obj) in [int, float]):			#Python3
		#power=0	# переписать этот говнокод через printf
		#if (abs(obj) < number['power']['min']):
		#	while (abs(obj) < 1):
		#		obj *= 10
		#		power -= 1
		#elif (abs(obj) > number['power']['max']):
		#	obj = float(obj)
		#	while (abs(obj) > 10):
		#		obj /= 10
		#		power += 1
		#latex = str(round(obj,number['float']['dad'])).replace('.',number['float']['del'])
		#if (power != 0): latex += ''' \\cdot 10^{%s}''' % (power)
		tmpstr = ("%g" % (obj))
		if (tmpstr.find('e') == -1):
			latex = tmpstr.replace('.', number['float']['del'])
		else:
			value, power = tmpstr.split('e')
			value = value.replace('.', number['float']['del'])
			power = int(power)
			latex = (value + ' \\cdot 10^{%s}' % (power))
	elif (type(obj) == str):
		latex = obj
	elif (type(obj) in (list, tuple, dict) or obj == None):#Тут переделать
		return ('\\textcolor{red}{ERROR}')	#Красная надпись об ошибке точно привлечёт внимание
	return (latex)
#------------------------------------------------------------------------------
def table2latex(**args):
	caption = None
	label = None
	tabtype = None
	latex = ''
	size = (len(args['table']), len(args['table'][0]))
	if ('weight' in args.keys()):
		userweight = args['weight']
	else:
		userweight = list(1 for i in range(size[1]))
	weight = list((userweight[i]*math.pow(sum(tuple(len(val(args['table'][j][i])) for j in range(size[0]))), 1/3)) for i in range(size[1]))	#Заменить на среднюю ширину слова
	sweight = sum(weight)
	uweight = tuple(weight[i]/sweight for i in range(size[1]))
	#print(str(uweight) + ':' + str(sum(uweight)))
	if ('caption' in args.keys()):
		caption = args['caption']
		rownum = 0
	else:	#F%king spike!
		caption = args['table'][0][0]	#Will be removed
		rownum = 1
	if ('label' in args.keys()): label = args['label']
	if ('type' in args.keys()):
		tabtype = args['type']
	else:
		if(size[0] > 12):
			tabtype = 'longtable'
		else:
			tabtype = 'table'
	match = ('.*\\multicolumn *\n*\{\d*\} *\n*\{.*\} *\n*\{.*\}', '.*\\multirow *\n*\{\d*\} *\n*\{.*\} *\n*\{.*\}')
	multi = list(list(1 for i in range(size[1])) for j in range(size[0])) #2 for col; 3 for row
	#^Чистейшая наркомания.
	colwidth = list((uweight[i] - 0.023) for i in range(size[1]))
	#head--------------------------------------------------------------
	if (tabtype == 'longtable'):
		latex += '\\begin{longtable}[h]{|'
	elif(tabtype == 'table'):
		latex += '\\begin{table}[h]\\begin{tabular}{|'
	for pwidth in colwidth:
		latex += 'p{' + str(pwidth) + '\\textwidth}|'
	latex += '}\n\\hline\n'
	#body--------------------------------------------------------------
	while (rownum < size[0]):
		colnum = 0
		while (True):
			if(args['table'][rownum][colnum] == ''):
				#print(str(rownum)+'x'+str(colnum)+":"+str(multi[rownum][colnum]))
				if(multi[rownum][colnum] % 2 == 0):
					l = 1
					#print('l'*20)
					while(multi[rownum][colnum] % 2 == 0):
						l += 1
						colnum += 1
					latex += '\\multicolumn{' + str(l) + '}{c|}{}'
				else:
					colnum += 1
			elif((re.match(match[0], val(args['table'][rownum][colnum]))) and (re.match(match[1], val(args['table'][rownum][colnum])))):
				mrowcount = int(re.sub('\}.*','',re.sub('.*\\multirow *\n*\{', '', val(args['table'][rownum][colnum]))))
				mcolcount = int(re.sub('\}.*','',re.sub('.*\\multicolumn *\n*\{', '', val(args['table'][rownum][colnum]))))
				latex += val(args['table'][rownum][colnum].replace('*',str(sum(colwidth[(colnum):(colnum + mcolcount)]))+'\\textwidth'))
				for i in range(mcolcount):
					for j in range(mrowcount-1):
						multi[rownum+j][colnum+i] *= 6
					#multi[mrowcount][colnum+i] *= 2
				colnum += mcolcount
			elif(re.match(match[0], val(args['table'][rownum][colnum]))):
				latex += val(args['table'][rownum][colnum])
				mcolcount = int(re.sub('\}.*','',re.sub('.*\\multicolumn *\n*\{', '', val(args['table'][rownum][colnum]))))
				for i in range(mcolcount-1): multi[rownum][colnum+i] *= 2
				colnum += mcolcount
			elif(re.match(match[1], val(args['table'][rownum][colnum]))):
				latex += val((args['table'][rownum][colnum]).replace('*',str(colwidth[colnum])+'\\textwidth'))
				mrowcount = int(re.sub('\}.*','',re.sub('.*\\multirow *\n*\{', '', val(args['table'][rownum][colnum]))))
				for j in range(mrowcount-1): multi[rownum+j][colnum] *= 3
				colnum += 1
			else:
				latex += val(args['table'][rownum][colnum])
				colnum += 1
			#---------------------------------------------------------
			if (colnum < size[1]):
				if(multi[rownum][colnum] % 2 != 0): latex += '&'
				#latex += '\n'
			else:
				latex += '\\\\\n'
				if (sum(1 if (i % 3 == 0) else 0 for i in multi[rownum])):
					begin = -1
					i = 0
					while (i < size[1]):
						if(multi[rownum][i] % 3 != 0):	#Нужно чертить
							if (begin == -1):	#Если ещё не чертим
								begin = i + 1
							i += 1
						elif(multi[rownum][i] % 3 == 0):	#Не нужно чертить
							if (begin != -1):	#Если вообще чертим
								latex += '\\cline{' + str(begin) + '-' + str(i) + '}'
								begin = -1
							i += 1
						#i += 1
					latex += '\n'
				else:
					latex += '\\hline\n'
				break
		rownum += 1
	#tail--------------------------------------------------------------
	if(tabtype == 'table'): latex += '\\end{tabular}\n'
	if(caption != None): latex += '\\caption{' + caption + '}'
	if(label != None): latex += '\\label{' + label + '}'
	if(tabtype == 'table'):
		latex += '\\end{table}'
	elif(tabtype == 'longtable'):
		latex += '\\end{longtable}'
	return(latex)

#------------------------------------------------------------------------------

def mkcsvtable(csvfilepath):
	from os.path import basename
	with open(csvfilepath) as f:
		#csvfile=tuple(tuple(list2data(line)) for line in csv.reader(f, delimiter='\t'))
		csvfile = tuple((lambda row: tuple(__str2data__(col) for col in row))(row) for row in csv.reader(f, delimiter='\t'))
	caption = csvfile[0][0]
	label = basename(csvfilepath.split('.')[0])
	tabtype = None
	size = (len(csvfile), len(csvfile[0]))
	if(size[0] > 12):
		tabtype = 'longtable'
	else:
		tabtype = 'table'
	weight = tuple((lambda i:(1 if csvfile[0][i] == '' else __str2data__(csvfile[0][i])))(i) for i in range(1,size[1])) #С 1го раза заработало 0_0
	#print(weight)
	match = ('.*\\multicolumn *\n*\{\d*\} *\n*\{.*\} *\n*\{.*\}', '.*\\multirow *\n*\{\d*\} *\n*\{.*\} *\n*\{.*\}')
	blockdict={}
	blockord = []
	table = []
	blkid = None
	#blockdict={'id1':[[col,col],[col,col]]],'id2':[[col,col],[col,col]]]}
	for row in csvfile[1:]:
		iterations = 1
		if (row[0] != ""):
			tmp = row[0].split(':')
			blkid = tmp[0]
			if(len(tmp) == 2):
				condition = (tmp[1])
			else:
				condition = 'False'
		if(blkid in blockdict.keys()):
			blockdict[blkid].append([row[i] for i in range(1,size[1])])
		else:
			blockord.append([blkid, iterations, condition])
			blockdict[blkid] = [[row[i] for i in range(1,size[1])]]
	#----------------------------------------------------------
	#print(blockord)
	_blknum = 0
	_sumrownum = 0
	for block in blockord:
		_blkrownum = 0
		while (block[1] > 0 or eval(block[2])):
			_rownum = 0
			for row in blockdict[block[0]]:
				_colnum = 0
				currentrow = []
				for col in row:
					tokens = col.split('`')
					currentcol = ''
					currentcol += tokens[0][:]
					#currentrow.append(tokens[0][:])
					if(len(tokens) == 2): currentcol += str(tokens[1])
					if(len(tokens) > 2):
						tokennum = 1
						while(tokennum < len(tokens)):
							try:
								#print(_blkrownum)
								currentcol += val(eval(tokens[tokennum]))
								#print(str(tokens[tokennum])+":"+str(eval(tokens[tokennum])))
								currentcol += str(tokens[tokennum+1])
								tokennum += 2
							except Exception:
								currentcol += str(tokens[tokennum])
								tokennum += 1
					currentrow.append(currentcol)
					#print(currentrow)
					_colnum += 1
				table.append(list(currentrow))
				_rownum += 1
				_blkrownum += 1
				_sumrownum += 1
				block[1] -= 1
			#_blkrownum += 1
			#_sumrownum += 1
		_blkrownum += 1
		_sumrownum += 1
		_blknum += 1
	#print(table)
	return(table2latex(table=table,caption=caption,label=label,weight=weight))

#---------------------------------

def solve(expr):
	parsedexpression = __parse__(expr)
	return(parsedexpression)

def ssolve():
	pass

def table():
	pass

#---------------------------------

#if (__name__ == "__main__"):	#AUTOTEST!
#	a={'l':'\\alpha'}
#	b={'l':'\\mathrm{\\textrm{Б}}_{s}', 'v':1.23}
#	c={'l':'\\tau', 'v':3.14}
#	d={'l':'\\delta','v':5}
#	e={'l':'e','v':2.7183}
#	print(val(0.000123456789))
#	print(val(9876543210))
#	print(val('sfsfrsf'))
#	print(val([]))
#	print(solve("a=1.3+(b+c)/d*e+R[2][10]+sin(a**c/b)"))
