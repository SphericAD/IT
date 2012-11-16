
#! /usr/bin/python
import re,math,operator
def unigrammodel(file):
	f = open(file,'r')
	try: 
		content= f.read()
		letters =map(chr,range(97,123))
		unigramcounts =[]
		sizeOFcontent=len(content)
		
		for l in letters:
			unigramcounts.append(len(re.findall(l,content)))
		unigramcounts.append(sizeOFcontent-sum(unigramcounts))	
		probabilitydist=[float(x)/float(sizeOFcontent) for x in unigramcounts]
		
		H =[-x*math.log(x,2) for x in probabilitydist]
		return sum(H),probabilitydist
	except:
		print "Error in code"
	finally:
			f.close()
								
#P(w1,w2)=P(w1)*P(w2|w1) = nc/TC * bgC/nc= bgC/TC
def bigrammodel(file):
	f = open(file,'r')
	try: 
		content= f.read()
		letters =map(chr,range(97,123))
		letters.append(' ')
		bigramcounts =[]
		
		
		for l in letters:
			for l2 in letters:
				pattern=l+l2
				
				bigramcounts.append(len(re.findall(pattern,content)))
		print bigramcounts			
		sizeOFcontent= len(content)
		print sizeOFcontent		
		probabilitydist=[float(x)/float(sizeOFcontent) for x in bigramcounts]
		print probabilitydist
		print sum(probabilitydist)
		H =[-x*math.log(x,2) for x in probabilitydist if x!=0]
		return sum(H),probabilitydist
	except:
		print "Error in code"
	finally:
			f.close()	

def arithmeticCodingUnf(file):
		f =open (file,'r')
		H,prodis =unigrammodel('thesis.txt')
		letters =map(chr,range(97,123))	
		letters.append(' ')
		print prodis		
		try:
			content = f.read()
			informationcontent=float(0);
			for i in range(len(content)):
				informationcontent= informationcontent- math.log(prodis[letters.index(content[i])],2)
			
			return math.ceil(informationcontent),prodis
		finally:
				f.close()
				
def getconditiondist(size,index,joindis):
				partitions= len(joindis)/size
				return joindis[partitions*index:partitions*index+size]
				
				 
def arithmeticCodingbg(file):
		f =open (file,'r')
		H,prodis =unigrammodel('thesis.txt')#prodis= P(x) where x is a letter
		letters =map(chr,range(97,123))	
		letters.append(' ')	
		H2,bgprodis= bigrammodel(file)#bdprodis = P(x1,x2) the joint distributions
		try:
			content= f.read()
			informationcontent= math.log(prodis[letters.index(content[0])],2) #first character generated by p(xn)
			prev_l=content[0]
			content=content[1:]
			for i in range(len(content)):
				index= letters.index(content[i])
				index_prevl= letters.index(prev_l)
				joindis_letter = getconditiondist(27,index_prevl,bgprodis)
				conditional_prob =joindis_letter[index]/prodis[index_prevl]#P(xn,xn+1)/P(xn)
				information= math.log(conditional_prob,2) 
				informationcontent= informationcontent +information
				prev_l= content[i]
			return math.ceil(-informationcontent),bgprodis
		finally:
			f.close()


def compressionLPH_Unf(file):
	f =open (file,'r')
	H,prodis =unigrammodel('thesis.txt')
	prodis = [ math.ceil(pow(2,8) *x)/pow(2,8) for x in prodis]
	prodis = [ x/sum(prodis) for x in prodis]
	letters =map(chr,range(97,123))	
	letters.append(' ')
	print prodis
	print sum(prodis)		
	try:
		content = f.read()
		informationcontent=float(0);
		L=[]
		for i in range(len(content)):
			informationcontent= informationcontent- math.log(prodis[letters.index(content[i])],2)
			
		return math.ceil(informationcontent),prodis
	finally:
		f.close()


def compressionLPH_Bg(file):	
	f =open (file,'r')
	H,prodis =unigrammodel('thesis.txt')#prodis= P(x) where x is a letter
	letters =map(chr,range(97,123))	
	letters.append(' ')	
	H2,bgprodis= bigrammodel(file)#bdprodis = P(x1,x2) the joint distributions
	prodis = [ math.ceil(pow(2,8) *x)/pow(2,8) for x in prodis]
	prodis = [ x/sum(prodis) for x in prodis]
	bgprodis = [ math.ceil(pow(2,8) *x)/pow(2,8) for x in bgprodis]
	bgprodis = [ x/sum(bgprodis) for x in bgprodis]
	try:
		content= f.read()
		informationcontent= math.log(prodis[letters.index(content[0])],2) #first character generated by p(xn)
		prev_l=content[0]
		content=content[1:]
		print len(content)
		for i in range(len(content)):
			index= letters.index(content[i])
			index_prevl= letters.index(prev_l)
			joindis_letter = getconditiondist(27,index_prevl,bgprodis)
			conditional_prob =joindis_letter[index]/prodis[index_prevl]#P(xn,xn+1)/P(xn)
			information= math.log(conditional_prob,2) 
			informationcontent= informationcontent +information
			prev_l= content[i]
		return math.ceil(-informationcontent),bgprodis
	finally:
		f.close()


def kullbackdiv(probdis1,probdis2):
	informationcontent=0
	for index,item in enumerate(probdis1):
		if item!=0:
			informationcontent+= item*math.log(item/probdis2[index],2)
	return informationcontent



#compression with adaptation:

def compressionAdaptUnf(file):
	f =open (file,'r')
	Ki_counter=dict([])
	letters =map(chr,range(97,123))	
	letters.append(' ')
	for alph in letters:
		Ki_counter[alph]=0
	
	try:
		content=f.read()
		informationcontent=0
		for i in range(len(content)):
			ai= content[i]
			informationcontent+= -math.log(float(Ki_counter[ai]+1)/float(i+len(letters)),2)
			Ki_counter[ai]+=1
		return informationcontent
	finally:
		f.close()

def compressionAdaptBg(file):
	f =open (file,'r')
	Ki_counter=dict([])
	letters =map(chr,range(97,123))	
	print letters
	letters.append(' ')
	for e in letters:
		for m in letters:
			Ki_counter[e+m]=0
	prev_l=''
	try:
		content=f.read()
		informationcontent=0
		for i in range(len(content)):
			if i==0:
				informationcontent+=-math.log(float(1)/len(letters),2)
					
			else:
				nj= sum([ Ki_counter[prev_l+x]	for x in letters] )
				informationcontent+= -math.log(float(Ki_counter[prev_l+content[i]]+1)/float(nj+len(letters)),2)
				Ki_counter[prev_l+content[i]]+=1
			prev_l=content[i]
				
		return informationcontent
	finally:
		f.close()

def XOR():
	string="nutritious snacks"
	stringtoascii = [ord(c)  for c in string]
	stringtoascii=stringtoascii+ [59, 6,17 ,0,83,84,26,90,64,70,25,66,86,82,90,95,75]	
	return chr(reduce(operator.xor,stringtoascii))
