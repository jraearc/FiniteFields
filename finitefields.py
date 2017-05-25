import os

def isInt(x):
	try:
		int(x)
	except ValueError:
		return False
	return True

def isCorrectInput(x):
	try:
		x = x.split(" ")
		for i in range(0, len(x)):
			if int(x[i]) != float(x[i]):
				return False
			x[i] = int(x[i])
	except ValueError:
		return False
	return True

def isComputableInput(F_x, modvalue):
	for i in range(0, len(F_x)):
		if F_x[i] >= modvalue:
			return False
	return True

#gets a list with coefficients in descending order and adds/subtract
def addPoly(p1, p2):
	res = []
	maxsize = max(len(p1), len(p2))
	p1 = [0 for i in range(0,maxsize-len(p1))] + p1
	p2 = [0 for i in range(0,maxsize-len(p2))] + p2
	for i in range(0, maxsize):
		res.append(p1[i] ^ p2[i])
	return res, (p1,p2)

def rembasic(n1, n2):
	res = n1
	#print len(bin(n1)[2:])
	#print len(bin(n2)[2:])
	for i in range(len(bin(n1)[2:])-len(bin(n2)[2:]), -1, -1):
		res ^= n2 << i
		if res < n2:
			break
	#print bin(res)
	if len(bin(res)[2:])-1 >= len(bin(n2)[2:])-1:
		res ^= n2
		#print bin(res)
	return res

def multbasic(n1, n2, P_x):
	res = 0
	sn2 = bin(n2)[2:]
	sn2 = sn2[::-1]
	for i in range(len(sn2)):
		res ^= int(sn2[i]) * (n1 << i)
	#print res
	if len(bin(res)[2:])-1 > len(bin(P_x)[2:])-2:
		res = rembasic(res, P_x)
		#print res
	return res

def multPoly(p1, p2, P_x):
	P_x = [str(P_x[i]) for i in range(len(P_x))]
	resmatrix = [[0 for i in range((len(p1)-1)+(len(p2)-1)+1)] for i in range(len(p2))]

	for i in range(len(p2)):
		for j in range(len(p1)):
			resmatrix[i][-(j+1+i)] = multbasic(p1[-(j+1)], p2[-(i+1)], int('0b' + ''.join(P_x), 2))

	res = [0 for i in range(len(resmatrix[0]))]

	#print res

	#print resmatrix

	for i in range(len(res)):
		for j in range(len(resmatrix)):
			res[i] ^= resmatrix[j][i]

	return res, resmatrix

def divPoly(n1, n2, P_x):
	P_x = [str(P_x[i]) for i in range(len(P_x))]
	quot = []
	res = n1
	rem = []
	div = n2 + [0 for i in range(len(res)-len(n2))]
	leading_co = res[0]
	rem.append(div)
	reslist = []
	#print leading_co
	for i in range(len(n1)-len(n2)+1):
		reslist.append([(multbasic(leading_co,div[j],int('0b' + ''.join(P_x), 2))) for j in range(len(res))])
		#print div
		quot.append(leading_co)
		rem.append([res[j] ^ (multbasic(leading_co,div[j],int('0b' + ''.join(P_x), 2))) for j in range(len(res))])
		res = rem[-1]
		res = res[1:]
		div = n2 + [0 for i in range(len(res)-len(n2))]
		leading_co = res[0]
		#print leading_co
	if quot == []:
		quot = [0]
	return quot, res, rem, reslist

def printResult(p1, p2, res, oper):
	os.system("cls")
	print "\nA(x):",
	for i in range(0, len(p1) - 1):
		if p1[i] > 0:
			if p1[i] > 1 and i < len(p1) - 2:
				print str(p1[i]) + "x^" + str(len(p1) - i - 1),
			elif i < len(p1) - 2:
				print "x^" + str(len(p1) - i - 1),
			if p1[i] > 1 and i == len(p1) - 1:
				print str(p1[i]) + "x",
			elif i == len(p1) - 2:
				print "x",
		if i < len(p1) - 1 and p1[i+1] > 0:
			print "+",
	if p1[-1] > 0:
		print str(p1[-1])
	else:
		print ""
	print "B(x):",
	for i in range(0, len(p2) - 1):
		if p2[i] > 0:
			if p2[i] > 1 and i < len(p2) - 2:
				print str(p2[i]) + "x^" + str(len(p2) - i - 1),
			elif i < len(p2) - 2:
				print "x^" + str(len(p2) - i - 1),
			if p2[i] > 1 and i == len(p2) - 2:
				print str(p2[i]) + "x",
			elif i == len(p2) - 2:
				print "x",
		if i < len(p2) - 1 and p2[i+1] > 0:
			print "+",
	if p2[-1] > 0:
		print str(p2[-1])
	else:
		print ""

	if oper == "/":
		print "A(x) " + oper + " B(x):",
		for i in range(0, len(res[0]) - 1):
			if res[0][i] > 0:
				if res[0][i] > 1 and i < len(res[0]) - 2:
					print str(res[0][i]) + "x^" + str(len(res[0]) - i - 1),
				elif i < len(res[0]) - 2:
					print "x^" + str(len(res[0]) - i - 1),
				if res[0][i] > 1 and i == len(res[0]) - 2:
					print str(res[0][i]) + "x",
				elif i == len(res[0]) - 2:
					print "x",
			if i < len(res[0]) - 1 and res[0][i+1] > 0:
				print "+",
		if res[0] == [0]:
			print "0"
		elif res[0][-1] > 0:
			print str(res[0][-1])
		else:
			print ""

		print "Remainder:",
		for i in range(0, len(res[1]) - 1):
			if res[1][i] > 0:
				if res[1][i] > 1 and i < len(res[1]) - 2:
					print str(res[1][i]) + "x^" + str(len(res[1]) - i - 1),
				elif i < len(res[1]) - 2:
					print "x^" + str(len(res[1]) - i - 1),
				if res[1][i] > 1 and i == len(res[1]) - 2:
					print str(res[1][i]) + "x",
				elif i == len(res[1]) - 2:
					print "x",
			if i < len(res[1]) - 1 and res[1][i+1] > 0:
				print "+",
		if res[1][-1] > 0:
			print str(res[1][-1])
		else:
			print ""

		print "------------------------------------------------------------------------"
		print "Solution in detail:\n"
		print "   ",
		for j in range(len(p1)-len(res[0])):
			print ' ',
		for j in res[0]:
			print j,
		print "\n-------------"
		print "   ",
		for i in p1:
			print i,
		print " = A\nXOR",
		for i in range(min(len(res[2]), len(res[3]))):
			if i > 0:
				print "   ",
				for j in range(len(p1)-len(res[2][i])):
					print 0,
				for j in res[2][i]:
					print j,
				print " = A\nXOR",
			for j in range(len(p1)-len(res[3][i])):
				print 0,
			for j in res[3][i]:
				print j,
			print " = B * " + str(res[0][i]) + "x^" + str(min(len(res[2]), len(res[3]))-i-1)
			print "-------------"
		print "   ",
		for j in range(len(p1)-len(res[1])):
			print ' ',
		for j in res[1]:
			print j,
		print " = Remainder"

	else:
		print "A(x) " + oper + " B(x):",
		for i in range(0, len(res[0]) - 1):
			if res[0][i] > 0:
				if res[0][i] > 1 and i < len(res[0]) - 2:
					print str(res[0][i]) + "x^" + str(len(res[0]) - i - 1),
				elif i < len(res[0]) - 2:
					print "x^" + str(len(res[0]) - i - 1),
				if res[0][i] > 1 and i == len(res[0]) - 2:
					print str(res[0][i]) + "x",
				elif i == len(res[0]) - 2:
					print "x",
			if i < len(res[0]) - 1 and res[0][i+1] > 0:
				print "+",
		if res[0][-1] > 0:
			print str(res[0][-1])
		else:
			print ""

		if oper == "*":
			print "------------------------------------------------------------------------"
			print "Solution in detail:\n"
			for j in range(len(res[0])-len(p1)):
				print ' ',
			for i in p1:
				print i,
			print ""
			print "x",
			for j in range(len(res[0])-len(p2)-1):
				print ' ',
			for i in p2:
				print i,
			print ""
			print "-" * (len(res[0])*2)
			hasLeading = False
			for i in res[1]:
				hasLeading = False
				for j in i:
					if j != 0:
						hasLeading = True
					if not hasLeading:
						print ' ',
					else:
						print j,
				print ""
			print "-" * (len(res[0])*2)
			for i in res[0]:
				print i,
			print ""

		if oper == "+" or oper == "-":
			print "------------------------------------------------------------------------"
			print "Solution in detail:\n"
			for j in range(len(res[0])-len(p1)+1):
				print ' ',
			for i in p1:
				print i,
			print ""
			print oper,
			for j in range(len(res[0])-len(p2)):
				print ' ',
			for i in p2:
				print i,
			print ""
			print "",
			print "-" * (len(res[0])*2)
			print " ",
			for i in res[0]:
				print i,
			print ""			

	print ""
	os.system("pause")


A_x = ""
B_x = ""
P_x = ""

while not isCorrectInput(A_x):
	os.system("cls")
	A_x = raw_input("\nEnter coefficients for A(x), separated by a space\nEx. x^4 + x + 1 -> 1 0 0 1 1\n:: ")
while not isCorrectInput(B_x):
	os.system("cls")
	B_x = raw_input("\nEnter coefficients for B(x), separated by a space\nEx. x^4 + x + 1 -> 1 0 0 1 1\n:: ")
while not isCorrectInput(P_x):
	os.system("cls")
	P_x = raw_input("\nEnter coefficients for P(x), separated by a space\nEx. x^4 + x + 1 -> 1 0 0 1 1\n:: ")

A_x = A_x.split(' ')
B_x = B_x.split(' ')
P_x = P_x.split(' ')
A_x = [int(i) for i in A_x]
B_x = [int(i) for i in B_x]
P_x = [int(i) for i in P_x]

GF_value = 2**(len(P_x)-1)

os.system("cls")
print "\nSelect an operation:\n"
print "1 - A(x) + B(x)"
print "2 - A(x) - B(x)"
print "3 - A(x) * B(x)"
print "4 - A(x) / B(x)"
print ""

selection = 0
str_inp = ""
while selection < 1 or selection > 4:
	while not isInt(str_inp):
		str_inp = raw_input(":: ")
	selection = int(str_inp)
	str_inp = ""

if isComputableInput(A_x, GF_value) and isComputableInput(B_x, GF_value):
	if selection == 1:
		printResult(A_x, B_x, addPoly(A_x, B_x), "+")
	if selection == 2:
		printResult(A_x, B_x, addPoly(A_x, B_x), "-")
	if selection == 3:
		printResult(A_x, B_x, multPoly(A_x, B_x, P_x), "*")
	if selection == 4:
		printResult(A_x, B_x, divPoly(A_x, B_x, P_x), "/")
else:
	print "\nCoefficient values for A(x) and B(x) must be less than " + str(GF_value) + "."