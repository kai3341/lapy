#!/usr/bin/env python3
##!/usr/bin/env python2.7	#Пока что останется памятником об окончании миграции
# -*- coding: utf-8 -*-

# Код НЕ оптимален с точки зрания производительности.
# Такты НЕ экономим, это программа не на C++,
# и работает она не на атомной электростанции.
# Максимум внимания расширяемости, читаемости и корректности.

#import math, re

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
	return (__tokenize__(expr))

def __structurize__(tokens):	#Парсер 2го уровня. Преобразует набор токенов в структуры. На нём лежит задача выделения в структуры переменных, функций, условий.
	pass

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
					while(expr[pointer].isalnum()):		#В состав переменной могут входить и цифры
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

#---------------------------------

def lapyout(obj):
	with open(outputfilename, mode='w', encoding='utf-8') as outfile:
		outfile.write(val(obj))

#---------------------------------

def val(obj):
	latex = None
#	if (type(obj) in [int, float, long]):	#Python2.7
	if (type(obj) in [int, float]):			#Python3
		power=0	# переписать этот говнокод через printf
		if (abs(obj) < number['power']['min']):
			while (abs(obj) < 1):
				obj *= 10
				power -= 1
		elif (abs(obj) > number['power']['max']):
			obj = float(obj)
			while (abs(obj) > 10):
				obj /= 10
				power += 1
		latex = str(round(obj,number['float']['dad'])).replace('.',number['float']['del'])
		if (power != 0): latex += ''' \\cdot 10^{%s}''' % (power)
	elif (type(obj) == str):
		latex = obj
	elif (type(obj) in [list, tuple, dict] or obj == None):#Тут переделать
		return ('\\textcolor{red}{ERROR}')	#Красная надпись об ошибке точно привлечёт внимание
	return (latex)

#---------------------------------

def solve(expr):
	return(__parse__(expr))

def ssolve():
	pass

def table():
	pass

#---------------------------------

if (__name__ == "__main__"):	#AUTOTEST!
	a={'l':'\\alpha'}
	b={'l':'\\mathrm{\\textrm{Б}}_{s}', 'v':1.23}
	c={'l':'\\tau', 'v':3.14}
	d={'l':'\\delta','v':5}
	e={'l':'e','v':2.7183}
#	print(val(0.000123456789))
#	print(val(9876543210))
#	print(val('sfsfrsf'))
#	print(val([]))
	print(solve("a=1.3+(b+c)/d*e+R[2][10]+sin(a**c/b)"))

