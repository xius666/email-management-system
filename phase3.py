
from bsddb3 import db
from datetime import datetime
from datetime import timedelta
import re
import sys
import time


curse_a = None
curse_b = None
curse_c = None
curse_d = None
database_a = None
database_b = None
database_c = None
database_d = None

def createDB():#open four database
    global database_a, database_b, database_c, database_d
    global curse_a, curse_b, curse_c, curse_d

    database_a = db.DB()
    database_a.open("re.idx", None, db.DB_HASH, db.DB_CREATE)
    curse_a = database_a.cursor()

    database_b = db.DB()
    database_b.set_flags(db.DB_DUP)
    database_b.open("em.idx", None, db.DB_BTREE, db.DB_CREATE)
    curse_b = database_b.cursor()

    database_c = db.DB()
    database_c.set_flags(db.DB_DUP)
    database_c.open("te.idx", None, db.DB_BTREE, db.DB_CREATE)
    curse_c = database_c.cursor()


    database_d = db.DB()
    database_d.set_flags(db.DB_DUP)
    database_d.open("da.idx", None, db.DB_BTREE, db.DB_CREATE)
    curse_d = database_d.cursor()



def closeDB():#close all the database
    global database_a, database_b, database_c, database_d
    global curse_a, curse_b, curse_c,curse_d
    curse_a.close()
    database_a.close()
    curse_b.close()
    database_b.close()
    curse_c.close()
    database_c.close()
    curse_d.close()
    database_d.close()
    
def evaluate(qs):#evaluate the querys each by each 
    row=[]
    for q in qs:
        if re.match(r"(subj|body)?(:)[0-9a-zA-Z_-]+\Z",q):#query by term 
            if len(row)==0:
                row=Querybyterm(q,False)
            else:
                row=list(set(row) & set(Querybyterm(q,False)))#get the intersection of two lists
                
        elif re.match(r"(subj|body)?(:)?[0-9a-zA-Z_-]+[%]?\Z",q) and "@" not in q and "/" not in q:#query by term partial
            if len(row)==0:
                row=Querybyterm(q,True)
            else:
                
                row=list(set(row) & set(Querybyterm(q,True)))
        elif "@" in q:#query by email
            if len(row)==0:
                row=Queryfromemail(q)
            else:
                row=list(set(row) & set(Queryfromemail(q)))
        elif "date" in q and "/" in q:#query by date
            if len(row)==0:
                row=date(q)
            else:
                row=list(set(row) & set(date(q)))
        else:
            print("there is invalid query")
            break
    return row
def printresult(rows,isfull):
    if isfull:#if user input "output=full" go to the re.idx to find the matching row id records
        iter = curse_a.first()
        while iter:
            if iter[0].decode("utf-8").lower() in rows:
                print(iter[1].decode("utf-8"))
            iter = curse_a.next()
    else:#if user input "output=brief" go to the re.idx to find the matching row id and the subject only
        iter = curse_a.first()
        while iter:
            if iter[0].decode("utf-8").lower() in rows:
                brief1=iter[1].decode("utf-8").split('</subj>')[0].split('<subj>')[1]
                brief2=iter[1].decode("utf-8").split('</row>')[0].split('<row>')[1]
                print("row id is:"+brief2)
                print("subject is: "+brief1)
            iter = curse_a.next()        	
   
def date(query):
    row_id=[]#to store the id
    special_case=0#to figure out if it is >= or <=
    date=""#the date
    iter = curse_d.first()
    list_q=list(query)
    da=query.split(list_q[4])
    if da[1][0]=='=':
        special_case=1
        da_l=da[1].split("=")
        date=da_l[1]
    else:
        date=da[1]
    if list_q[4]==':':#the case of equal
        while iter:
            if iter[0].decode("utf-8").lower() == date:
                row_id.append(iter[1].decode("utf-8"))
            iter = curse_d.next()        
    elif list_q[4]=='>':#the case of greater
        dat=date.encode("utf-8")
        iter=curse_d.first()
        while iter:
            if special_case==1:
                if time.strptime(iter[0].decode("utf-8").lower(),"%Y/%m/%d") >= time.strptime(date,"%Y/%m/%d"):
                    row_id.append(iter[1].decode("utf-8"))
            if special_case==0:
                if time.strptime(iter[0].decode("utf-8").lower(),"%Y/%m/%d") > time.strptime(date,"%Y/%m/%d"):
                    row_id.append(iter[1].decode("utf-8"))
            iter = curse_d.next()        
    elif list_q[4]=='<':#the case of smaller
        dat=date.encode("utf-8")
        iter=curse_d.first()
        while iter:
            if special_case==1:
                if time.strptime(iter[0].decode("utf-8").lower(),"%Y/%m/%d") <= time.strptime(date,"%Y/%m/%d"):
                    row_id.append(iter[1].decode("utf-8"))
            if special_case==0:
                if time.strptime(iter[0].decode("utf-8").lower(),"%Y/%m/%d") < time.strptime(date,"%Y/%m/%d"):
                    row_id.append(iter[1].decode("utf-8"))
            iter=curse_d.next()
    return row_id       
def Queryfromemail(querys):
    row_id1=[]
    str1=""
    email=querys.split(":")
    str1+=email[0]+"-"+email[1]#change the query to the same format as in the data        
    iter = curse_b.first()
    while iter:
        if iter[0].decode("utf-8").lower() == str1:#search the matching row_id
            rowid=iter[1].decode("utf-8")
            row_id1.append(rowid)
        iter = curse_b.next()

    return row_id1
    

def strip1(str1,line):
    res = line.split(str1)
    output =""
    for i in range(len(res)):
        if i == 0:
            output += res[0]
        else:
            right = res[i].lstrip()
            output += str1 + right
    return output

def strip2(line):#get rid of the whitespace
    list1 = ["date","subj","from","to","cc","bcc","body",":","<",">",">=","<="]
    for str1 in list1:
        line2 = strip1(str1, line)
        line = line2
    output = []
    line = line.split(" ")
    for li in line:
        if li != "":
            output.append(li)
    return output
def Querybyterm(query, partialSearch):
    row_id=[]
    if partialSearch:
        if "%" in query:
            if "subj:" in query:#handle the case when do a partial search on subject
                keyword=query.replace("subj:","s-")
                keyword =keyword.strip("%")
                iter = curse_c.first()
                while iter:
                    if iter[0].decode("utf-8").startswith(keyword):
                        if iter[1].decode("utf-8") not in row_id:
                            row_id.append(iter[1].decode("utf-8"))
                    iter = curse_c.next()

            elif "body:" in query :#handle the case when do a partial search on body
                keyword=query.replace("body:","b-")
                keyword =keyword.strip("%")
                iter = curse_c.first()
                while iter:
                    if iter[0].decode("utf-8").startswith(keyword):
                        if iter[1].decode("utf-8") not in row_id:
                            row_id.append(iter[1].decode("utf-8"))
                    iter=curse_c.next()
            else:#handle the case when do a partial search on terms
                keyword = query.strip("%")
                iter = curse_c.first()
                while iter:
                    if iter[0].decode("utf-8").strip('s-').startswith(keyword) or iter[0].decode("utf-8").strip('b-').startswith(keyword):
                        if iter[1].decode("utf-8") not in row_id:
                             row_id.append(iter[1].decode("utf-8"))
                    iter = curse_c.next()
        else:#search exact terms when without the %
            iter = curse_c.first()
            while iter:
                if iter[0].decode("utf-8").strip('s-')==query or iter[0].decode("utf-8").strip('b-')==query:
                    if iter[1].decode("utf-8") not in row_id:
                         row_id.append(iter[1].decode("utf-8"))
                iter = curse_c.next()
    else:#when we need to do a exact match
        if "subj:" in query:
            query=query.replace("subj:","s-")
        elif "body:" in query :
            query=query.replace("body:","b-")
        keyword = query.encode("utf-8")
        iter = curse_c.set(keyword)
        while iter:#iterate throught the terms index 
            if iter[0].decode("utf-8") == query:
                if iter[1].decode("utf-8") not in row_id:
                    row_id.append(iter[1].decode("utf-8"))
            iter = curse_c.next()
            if iter == None:
                break
    
    return row_id

def main():
    query = input("input: ").lower()
    if query == '':
        exit("Exiting program...")
    createDB() 
    querys = strip2(query)
    row_id=evaluate(querys)#evaluate the query to get the row_id 
    while True:
        user_choice=input("brief or full or exit: ")
        if user_choice == "output=full":
            printresult(row_id,True)#pass in the bool of true when we need the full records.
        elif user_choice == "output=brief" :
            printresult(row_id,False)
        elif user_choice == "exit" :
            exit("Exiting program...")
        else:
            print("invalid option,enter again!")

    closeDB()
  
main()
