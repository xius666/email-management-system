import sys
import re
def cut(line, key):
	array=line.split('</'+key+'>')[0].split('<'+key+'>')[1]
	return array
def phase1(file,terms,emails,dates,recs):
	for x in range(2):
		file.readline()
	while True:
		line=file.readline()
		if line.strip()=='</emails>':
			break
		else:
			row=cut(line,'row')
			date=cut(line,'date')
			dates.write(date+':'+row+'\n')
			from1=cut(line,'from').lower()
			if len(from1)!=0:
				if ',' in from1:
					from1=from1.split(',')
					for i in from1:
						emails.write('from-'+i+':'+row+'\n')
				else:
					emails.write('from-'+from1+':'+row+'\n')
			to=cut(line,'to').lower()
			if len(to)!=0:
				if ',' in to:
					to=to.split(',')
					for i in to:
						emails.write('to-'+i+':'+row+'\n')
				else:
					emails.write('to-'+to+':'+row+'\n')
			cc=cut(line,'cc').lower()
			if len(cc)!=0:
				if ',' in cc:
					cc=cc.split(',')
					for i in cc:
						emails.write('cc-'+i+':'+row+'\n')
				else:
					emails.write('cc-'+cc+':'+row+'\n')

			bcc=cut(line,'bcc').lower()
			if len(bcc)!=0:
				if ',' in bcc:
					bcc=bcc.split(',')
					for i in bcc:
						emails.write('bcc-'+i+':'+row+'\n')
				else:
					emails.write('bcc-'+bcc+':'+row+'\n')

			rec=cut(line,'mail')
			recs.write(row+':'+'<mail>'+rec+'</mail>'+'\n')

			subject=cut(line,'subj')
			for s in clean(subject):
				terms.write('s-'+s+':'+row+'\n')
				
			body=cut(line,'body')
			for b in clean(body):
				terms.write('b-'+b+':'+row+'\n')
			

	return
def clean(term):

	#replace all the specail char with space
	term = term.replace('&apos;', ' ').replace('&quot;', ' ').replace('&amp;', ' ').replace('&lt;',' ').replace('&gt;',' ').replace('&#10',' ')
	term = re.sub(r'[&][#][0-9]+[;]','', term) 
	correct='0123456789abcdefghijklmnopqrstuvwxyz-_'
	term=term.lower()
	for a in term:
		if a not in correct:
			term=term.replace(a,' ')
	returnl=[]
	terms = term.split(' ')
	for b in terms:
		b=b.strip()#remove space at the beginning and the end
		if len(b)>2:
			returnl.append(b)

	return returnl
def main(path):
	path='./'+path
	file=open(path,'r')
	#open all the files with write mode
	terms = open('terms.txt', 'w')
	emails = open('emails.txt', 'w')
	dates = open('dates.txt', 'w')
	recs = open('recs.txt', 'w')
	phase1(file,terms,emails,dates,recs)
	terms.close()
	emails.close()
	dates.close()
	recs.close()
main(sys.argv[1])



