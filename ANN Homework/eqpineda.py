from mpmath import *

mp.dps = 75

def activation(val):
	# Sigmoid function (ewan ko kung anong tawag dun, tama ba)
	return mpf( 1 / ( 1 + e**( val * -1 ) ) )


### I want everything here to be modifiable, if sumabog, sorry ;__;
inp = [1, 2, 3, 4, 5]	
hidden = 5
out = 1
target = 0.5
###

weightsith = []
weightshto = []
inputtohidden = []
hiddentoout = []
hid = []
outval = []

for i in range(0, hidden):
	tmp = []
	for j in range(0, len(inp)):
		if (i%2 == 1) and (j%2 == 1):
			tmp.insert(j, 0.2)
		elif (i%2 == 0) and (j%2 == 1):
			tmp.insert(j, 0.3)
		elif (i%2 == 1) and (j%2 == 0):
			tmp.insert(j, 0.5)
		else:
			tmp.insert(j, 0.25)
	weightsith.insert(i, tmp)

for i in range(0, out):
	tmp = []
	for j in range(0, hidden):
		if j <= 2:
			tmp.insert(j, 0.7)
		else:
			tmp.insert(j, 0.5)
	weightshto.insert(i, tmp)

### END OF INITIALIZATION OF VARIABLES ###

for i in range(0, hidden):
	tmp = []
	for j in range(0, len(inp)):
		tmp.insert(j, mpf(weightsith[i][j]*inp[j]))

	inputtohidden.insert(i, tmp)

for i in range(0, hidden):
	hid.insert(i, activation(sum(inputtohidden[i])))

for i in range(0, out):
	tmp = []
	for j in range(0, hidden):
		tmp.insert(j, mpf(weightshto[i][j]*hid[j]))
	hiddentoout.insert(i, tmp)

for i in range(0, out):
	outval.insert(i, activation(sum(hiddentoout[i])))

# HINDI PALA KAILANGAN ICODE PUTAAAAAAAAAAAAAAADSJHFAKJDHGLAKUJHFLAJSKDFHALKDSJFHALSKDJHFLAKJDSHFLJHLKJBADLJK