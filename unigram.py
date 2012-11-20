
#! /usr/bin/python
import re,math,operator,random,numpy
def unigrammodel(file):
	f = open(file,'r')
	try: 
		content= f.read()
		letters =map(chr,range(97,123))
		unigramcounts =[]
		sizeOFcontent=len(content)
		
		for l in letters:
			unigramcounts.append(len(re.findall(l,content)))#counts the number of times each letter in the alphabet occurs in the file
		unigramcounts.append(sizeOFcontent-sum(unigramcounts))	
		probabilitydist=[float(x)/float(sizeOFcontent) for x in unigramcounts]#probability distribution of a character chosen random from the file
		
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

def LTdecode(file,file2):
	f=open(file,'r')
	g=open(file2,'r')
	encodedPackets=[]
	SourcebitsUsed=[]
	try:
		contents=f.readlines()
		for i in range(len(contents)):
			encodedPackets.append(int(contents[i].strip()))
		contentSource = g.readlines()
		for line in contentSource:
			line = line.strip().split()
			sourcebits=[int(x) for x in line]
			SourcebitsUsed.append(sourcebits)
		num_of_sourcebits=0
		for list in SourcebitsUsed:
			if max(list)>num_of_sourcebits:
				num_of_sourcebits = max(list)
		decodedS =['']*num_of_sourcebits
		PacketsU=[]
		while '' in decodedS:
			for index, list in enumerate(SourcebitsUsed):
				if len(list)==1 :
					sourcebit=list[0]
					p=SourcebitsUsed[index].pop()
					decodedS[sourcebit-1] =chr(encodedPackets[index])
					PacketsU.append(index)
					for j, lis in enumerate( SourcebitsUsed):
						if sourcebit in lis:
							lis.remove(sourcebit)
							encodedPackets[j] = operator.xor(encodedPackets[j],encodedPackets[index])
		print decodedS	,PacketsU
	finally:
		f.close()	
		g.close()


def simulation():
	number=111
	L=[]
	i=0
	p=0.1
	f=0.2
	while i<1000000:
		num="111"
		
		for j in range(len(num)):
				random.seed(random.randint(1,1000))
				if j<2:
					r=random.random()
					
					if r<p:
						if i<30:
							print r
						if j==0:
							num="011"
						else:
							num="101"
						L.append(int(num))
						break
				else:
					if random.random()<f:
						num="110"
						L.append(int(num))
						break
		i+=1
					
	
	
	return float(len(L))/1000000, L[:30]
def Encoder(sourcebits):
	R3code= sourcebits[0]*3+sourcebits[1]*3 + sourcebits[2]*3+sourcebits[3]*3
	s1=int(sourcebits[0])
	s2=int(sourcebits[1])
	s3=int(sourcebits[2])
	s4=int(sourcebits[3])
	s5 = reduce(operator.xor,[s1,s2,s3])
	s6 = reduce(operator.xor,[s2,s3,s4])
	s7= reduce(operator.xor,[s1,s3,s4])
	return R3code+str(s5)+str(s6)+str(s7)

def Decoder(ReceivedBits):
	DecodedBits=[]
	for i in range(4):
		seq= ReceivedBits[3*i:3*i+3]
		if len(re.findall('0',seq))>1:
			DecodedBits.append(0)
		else:
			DecodedBits.append(1)	
	#computing the syndrome z
	t= numpy.array([DecodedBits[0],DecodedBits[1],DecodedBits[2],DecodedBits[3],int(ReceivedBits[-3]),int(ReceivedBits[-2]),int(ReceivedBits[-1])])
	H= numpy.array([[1,1,1,0,1,0,0],[0,1,1,1,0,1,0],[1,0,1,1,0,0,1]])
	z= numpy.dot(H,t)
	z =[ 2^x for x in z]
	columnsofH = [[1,0,1],[1,1,0],[1,1,1],[0,1,1][1,0,0],[0,1,0],[0,0,1]]
	z=[1,1,0]
	if z!=[0,0,0]:
		index = columsofH.index(z)
		t[index]=(t[index]+1)^2
	return z	
		
	return		
