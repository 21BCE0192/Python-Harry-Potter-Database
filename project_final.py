#Modules and Connections--------------------------------------------------------------------
import mysql.connector as ms
import math
import os
import csv
import random
from prettytable import PrettyTable
conn=ms.connect(host='localhost',user='root',passwd='0000',database='potter')
cursor=conn.cursor()
#Path For File Folder (CSC Project)--------------------------------------------------------
print('\nEnter file path where you have placed the \'CSC Project\' folder in your system.\nNote : (Dont add \'\\\' at the end and add \'\\\\\' between directories).')
while True:
    while True:
        path=input('\nPath : ')
        try:
            if path[-1]=='\\' or path[-1]+path[-2]=='\\\\':
                print('\nDont add \'\\\' or \'\\\\\' at the end of your path.')
                continue
            else:
                break
        except IndexError:
            print('\nThe folder \'CSC Project\' was not found in the specified path.')
            continue
    try:
        f=open(path+'\\CSC Project\\Buffer Files\\status.txt')
    except FileNotFoundError:
        print('\nThe folder \'CSC Project\' was not found in the specified path.')
        continue
    except OSError:
        print('\nThe folder \'CSC Project\' was not found in the specified path.')
        continue
    f.close()
    break
#Functions---------------------------------------------------------------------------------
def add():
    ch='y'
    while ch.lower()=='y':
        name=input('\nEnter full name : ')
        s2='select * from wiz where name=\'{}\''.format(name)
        cursor.execute(s2)
        cursor.fetchall()
        r=cursor.rowcount
        if r!=0:
            print('\nRecord with name',' ','\'',name,'\'',' ','already exists.',sep='')
            continue
        else:
            while True:
                house=input('\nEnter house : ')
                h=['Gryffindor','Hufflepuff','Ravenclaw','Slytherin']
                if house.capitalize()  not in h:
                    print('\nThere is no house categorised as',' ','\'',house,'\'',sep='')
                    print('\nCategorised houses are : ',h)
                    continue
                else:
                    break
            while True:
                blood = input('\nEnter blood : ')
                b=['Pureblood','Halfblood','Mudblood']
                if blood.capitalize() not in b:
                    print('\nThere is no blood categorised as',' ','\'',blood,'\'',sep='')
                    print('\nCategorised blood types are : ',b)
                    continue
                else:
                    break
            while True:
                gender=input('\nWizard or Witch? ')
                g=['Wizard','Witch']
                if gender.capitalize() not in g:
                    print('\nThere is no gender categorised as',' ','\'',gender,'\'',sep='')
                    print('\n Enter either wizard or witch only. . .')
                    continue
                else:
                    break
            while True:
                try:
                    dob=input('\nEnter date of birth in the format yyyy-mm-dd : ')
                    s='insert into wiz values(\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'.format(name,house,blood,gender,dob)
                    cursor .execute(s)
                except ms.errors.DataError:
                    print('\nPlease enter DOB in the format \'yyyy-mm-dd\'. . .')
                    continue
                break
            conn.commit()
            ch=input('\nAdd more records? (y/n) ')
#------------------------------------------------------------------------------------------
def read():
    x=PrettyTable()
    cursor.execute('select * from wiz order by name')
    d=cursor.fetchall()
    h=cursor.description
    r=cursor.rowcount
    t=[]
    for i in h:
        t.append(i[0])
    x.field_names=t
    for i in d:
        row=[]
        for j in i:
            row.append(j)
        x.add_row(row)
    print(x)
    print('\nNo. of records : ',r)
#------------------------------------------------------------------------------------------
def update():
    while True:
        n=input('\nEnter name whose record is to be updated : ')
        s2='select * from wiz where name like \'{}%\''.format(n)
        cursor.execute(s2)
        cursor.fetchall()
        r=cursor.rowcount
        if r==0:
            print('\nSorry, name not found. . .')
            continue
        else:
            break
    print('\nWhich field would you like to update in ',n,'\'s record?',sep='')
    while True:
        try:
            u=int(input('\n1.House | 2.Blood | 3.Gender | 4.Date of Birth\n\nChoose your option number : '))
        except ValueError:
            print('\nPlease choose a numbered option , not letters. . .')
            continue
        if u==1:
            while True:
                house=input('\nHouses : Gryffindor | Hufflepuff | Ravenclaw | Slytherin\n\nEnter new house : ')
                h=['Gryffindor','Hufflepuff','Ravenclaw','Slytherin']
                if house.capitalize() not in h:
                    print('\nInvalid Input. . .Try again. . .')
                    continue
                else:
                    break
            s='update wiz set house=\'{}\' where name like \'{}%\''.format(house,n)
            cursor.execute(s)
            conn.commit()
            print('\nUpdated successfully')
            break
        elif u==2:
            while True:
                blood=input('\nBlood Types : Pureblood | Halfblood | Mudblood\n\nEnter new blood : ')
                b=['Pureblood','Halfblood','Mudblood']
                if blood.capitalize() not in b:
                    print('\nInvalid Input. . .Try again. . .')
                    continue
                else:
                    break
            s='update wiz set blood=\'{}\' where name like \'{}%\''.format(blood,n)
            cursor.execute(s)
            conn.commit()
            print('\nUpdated successfully')
            break
        elif u==3:
            while True:
                gender=input('\nWitch or Wizard? ')
                g=['Witch','Wizard']
                if gender.capitalize() not in g:
                    print('\nInvalid Input. . .Try again. . .')
                    continue
                else:
                    break
            s='update wiz set gender=\'{}\' where name like \'{}%\''.format(gender,n)
            cursor.execute(s)
            conn.commit()
            print('\nUpdated successfully')
            break
        elif u==4:
            while True:
                try:
                    dob=input('\nEnter new DOB in the format yyyy-mm-dd : ')
                    s='update wiz set dob=\'{}\' where name like \'{}%\''.format(dob,n)
                    cursor.execute(s)
                except ms.errors.DataError:
                    print('\nPlease input DOB in the format \'yyyy-mm-dd\'. . .')
                    continue
                break
            conn.commit()
            print('\nUpdated successfully')
            break
        else:
            print('\nChoose a valid option. . .')
            continue
#------------------------------------------------------------------------------------------
def display():
    ptable=PrettyTable()
    print('-'*70,'SPECIFIC FIELD REPORTS','-'*73)
    while True:
        try:
            o=int(input('\n1.Display wizards by house | 2.Display wizards by blood | 3.Search for wizards by starting or ending letters\n\nEnter your choice : '))
        except ValueError:
            print('\nPlease input a numbered option, not letters. . .')
            continue
        if o==1:
            l=['Gryffindor','Hufflepuff','Ravenclaw','Slytherin']
            while True:
                v=input('\nHouses : Gryffindor | Hufflepuff | Ravenclaw | Slytherin\n\nEnter house name to be accessed : ')
                if v.capitalize() in l:
                    print('-'*167)
                    s='select * from wiz where house=\'{}\''.format(v)
                    cursor.execute(s)
                    d=cursor.fetchall()
                    r=cursor.rowcount
                    h=cursor.description
                    l=[]
                    for i in h:
                        l.append(i[0])
                    ptable.field_names=l
                    for i in d:
                        row=[]
                        for j in i:
                            row.append(j)
                        ptable.add_row(row)
                    print(ptable)
                    print('\nNo. of wizards in',v.capitalize(),':',r)
                    break
                else:
                    print('\nInvalid Input. . .Try again . . .')
                    continue
            break
        elif o==2:
            b=['Pureblood','Halfblood','Mudblood']
            while True:
                v=input('\nBlood Types : Pureblood | Halfblood | Mudblood\n\nEnter blood type to be accessed : ')
                if v.capitalize() in b:
                    print('-'*167)
                    s='select * from wiz where blood=\'{}\''.format(v)
                    cursor.execute(s)
                    d=cursor.fetchall()
                    h=cursor.description
                    r=cursor.rowcount
                    t=[]
                    for i in h:
                        t.append(i[0])
                    ptable.field_names=t
                    for i in d:
                        row=[]
                        for j in i:
                            row.append(j)
                        ptable.add_row(row)
                    print(ptable)
                    print('\nNo. of',v,'wizards : ',r)
                    break
                else:
                    print('\nInvalid Input. . .Try again . . .')
                    continue
            break
        elif o==3:
            while True:
                a=input('\na.Starting | b.Ending\n\nChoose (a/b) : ')
                if a=='a':
                    l=input('\nEnter starting letter(s) : ')
                    s='select * from wiz where name like \'{}%\''.format(l)
                    cursor.execute(s)
                    d=cursor.fetchall()
                    r=cursor.rowcount
                    if r==0:
                        print('\nNo record found with name starting with ','\'',l,'\'',' . . .',sep='')
                        break
                    h=cursor.description
                    t=[]
                    for i in h:
                        t.append(i[0])
                    ptable.field_names=t
                    for i in d:
                        row=[]
                        for j in i:
                            row.append(j)
                        ptable.add_row(row)
                    print(ptable)
                    print('\nNumber of records found with name starting with ','\'',l,'\'',' : ',r,sep='')
                    break
                elif a=='b':
                    l=input('\nEnter ending letter(s) : ')
                    s='select * from wiz where name like \'%{}\''.format(l)
                    cursor.execute(s)
                    d=cursor.fetchall()
                    r=cursor.rowcount
                    if r==0:
                        print('\nNo record found with name ending with ','\'',l,'\'',' . . .',sep='')
                        break
                    h=cursor.description
                    t=[]
                    for i in h:
                        t.append(i[0])
                    ptable.field_names=t
                    for i in d:
                        row=[]
                        for j in i:
                            row.append(j)
                        ptable.add_row(row)
                    print(ptable)
                    print('\nNumber of records found with name ending with ','\'',l,'\'',' : ',r,sep='')
                    break
                print('\nInvalid Input. . . Try Again. . .')
        else:
            print('\nInvalid Input. . .Try Again. . .')
            continue
        break
#------------------------------------------------------------------------------------------
def delete():
    name=input('\nEnter name of wizard whose record is to be deleted : ')
    s='select * from wiz where name=\'{}\''.format(name)
    cursor.execute(s)
    cursor.fetchall()
    r=cursor.rowcount
    if r==0:
        print('\nNo record found with name',' ','\'',name,'\'',sep='')
    else:
        s2='delete from wiz where name=\'{}\''.format(name)
        cursor.execute(s2)
        conn.commit()
        print('\nDeleted record of',name,'successfully. . .')
#------------------------------------------------------------------------------------------
def pdisplay():
    ptable=PrettyTable()
    print('-'*70,'SPECIFIC FIELD REPORTS','-'*73)
    while True:
        try:
            o=int(input('\n1.Display professors by house | 2.Display professors by blood | 3.Search for professors by starting or ending letters\n\nEnter your choice : '))
        except ValueError:
            print('\nPlease input a numbered option, not letters. . .')
            print('-'*167)
            continue
        if o==1:
            l=['Gryffindor','Hufflepuff','Ravenclaw','Slytherin']
            while True:
                v=input('\nHouses : Gryffindor | Hufflepuff | Ravenclaw | Slytherin\n\nEnter house name to be accessed : ')
                if v.capitalize() in l:
                    print('-'*167)
                    s='select * from prof where house=\'{}\''.format(v)
                    cursor.execute(s)
                    d=cursor.fetchall()
                    r=cursor.rowcount
                    h=cursor.description
                    l=[]
                    for i in h:
                        l.append(i[0])
                    ptable.field_names=l
                    for i in d:
                        row=[]
                        for j in i:
                            row.append(j)
                        ptable.add_row(row)
                    print(ptable)
                    print('\nNo. of professors in',v.capitalize(),':',r)
                    break
                else:
                    print('\nInvalid Input. . .Try again . . .')
                    print('-'*167)
                    continue
            break
        elif o==2:
            b=['Pureblood','Halfblood','Mudblood','Half-giant','Half-goblin']
            while True:
                v=input('\nBlood Types : Pureblood | Halfblood | Mudblood | Half-giant | Half-goblin\n\nEnter blood type to be accessed : ')
                if v.capitalize() in b:
                    print('-'*167)
                    s='select * from prof where blood=\'{}\''.format(v)
                    cursor.execute(s)
                    d=cursor.fetchall()
                    h=cursor.description
                    r=cursor.rowcount
                    t=[]
                    for i in h:
                        t.append(i[0])
                    ptable.field_names=t
                    for i in d:
                        row=[]
                        for j in i:
                            row.append(j)
                        ptable.add_row(row)
                    print(ptable)
                    print('\nNo. of',v,'professors : ',r)
                    break
                else:
                    print('\nInvalid Input. . .Try again . . .')
                    print('-'*167)
                    continue
            break
        elif o==3:
            while True:
                a=input('\na.Starting | b.Ending\n\nChoose (a/b) : ')
                if a=='a':
                    l=input('\nEnter starting letter(s) : ')
                    s='select * from prof where name like \'{}%\''.format(l)
                    cursor.execute(s)
                    d=cursor.fetchall()
                    r=cursor.rowcount
                    if r==0:
                        print('\nNo record found with name starting with ','\'',l,'\'',' . . .',sep='')
                        break
                    h=cursor.description
                    t=[]
                    for i in h:
                        t.append(i[0])
                    ptable.field_names=t
                    for i in d:
                        row=[]
                        for j in i:
                            row.append(j)
                        ptable.add_row(row)
                    print(ptable)
                    print('\nNumber of records found with name starting with ','\'',l,'\'',' : ',r,sep='')
                    break
                elif a=='b':
                    l=input('\nEnter ending letter(s) : ')
                    s='select * from prof where name like \'%{}\''.format(l)
                    cursor.execute(s)
                    d=cursor.fetchall()
                    r=cursor.rowcount
                    if r==0:
                        print('\nNo record found with name ending with ','\'',l,'\'',' . . .',sep='')
                        break
                    h=cursor.description
                    t=[]
                    for i in h:
                        t.append(i[0])
                    ptable.field_names=t
                    for i in d:
                        row=[]
                        for j in i:
                            row.append(j)
                        ptable.add_row(row)
                    print(ptable)
                    print('\nNumber of records found with name ending with ','\'',l,'\'',' : ',r,sep='')
                    break
                print('\nInvalid Input. . .Try Again. . .')
                print('-'*167)
        else:
            print('\nInvalid Input. . .Try Again. . .')
            print('-'*167)
            continue
        break
#------------------------------------------------------------------------------------------
def pread():
    x=PrettyTable()
    cursor.execute('select * from prof order by name')
    d=cursor.fetchall()
    h=cursor.description
    r=cursor.rowcount
    t=[]
    for i in h:
        t.append(i[0])
    x.field_names=t
    for i in d:
        row=[]
        for j in i:
            row.append(j)
        x.add_row(row)
    print(x)
    print('\nNo. of records : ',r)
#------------------------------------------------------------------------------------------
def quidw():
    ptable=PrettyTable()
    print('-'*74,'QUIDDITCH MENU','-'*77)
    while True:
        try:
            c=int(input('\n1.Yearwise Winners Report | 2.Statistics | 3.Tournament | 4.Archives\n\nEnter your choice : '))
        except ValueError:
            print('\nPlease input a numbered option. . .')
            print('-'*167)
            continue
        if c==1:
            print('-'*70,'YEARWISE WINNERS REPORT','-'*72)
            cursor.execute('select * from quid order by year')
            d=cursor.fetchall()
            h=cursor.description
            t=[]
            for i in h:
                t.append(i[0])
            ptable.field_names=t
            for i in d:
                row=[]
                for j in i:
                    row.append(j)
                ptable.add_row(row)
            print(ptable)
            break
        elif c==2:
            print('-'*76,'STATISTICS','-'*79)
            stats()
            break
        elif c==3:
            tournament()
            break
        elif c==4:
            archives()
            break
        else:
            print('\nInvalid Input. . .Try Again. . .')
            print('-'*167)
            continue
#------------------------------------------------------------------------------------------
def stats():
    global path
    high=0
    low=10000
    for i in range(2000,2051):
        for j in range(1,7):
            try:
                f=open(path+'\\CSC Project\\Years\\'+str(i)+'\\Matches\\Match '+str(j)+'.csv',newline='\n')
                r=csv.reader(f)
                match=[]
                for k in r:
                    match.append(k)
                if math.fabs(int(match[0][3])-int(match[0][1]))>=float(high):
                    high=math.fabs(int(match[0][3])-int(match[0][1]))
                    hrec=match
                    hyear=i
                    hmatch_no=j
                elif math.fabs(int(match[0][3])-int(match[0][1]))<=float(low):
                    low=math.fabs(int(match[0][3])-int(match[0][1]))
                    lrec=match
                    lyear=i
                    lmatch_no=j
                f.close()
            except FileNotFoundError:
                continue
    htable=PrettyTable()
    ltable=PrettyTable()
    hrec,lrec,hyear,lyear=[],[],[],[]
    hmatch_no,lmatch_no=[],[]
    for i in range(2000,2051):
        for j in range(1,7):
            try:
                f=open(path+'\\CSC Project\\Years\\'+str(i)+'\\Matches\\Match '+str(j)+'.csv',newline='\n')
                r=csv.reader(f)
                match=[]
                for k in r:
                    match.append(k)
                if math.fabs(int(match[0][3])-int(match[0][1]))>=float(high):
                    high=math.fabs(int(match[0][3])-int(match[0][1]))
                    hrec.append(match)
                    hyear.append(i)
                    hmatch_no.append(j)
                elif math.fabs(int(match[0][3])-int(match[0][1]))<=float(low):
                    low=math.fabs(int(match[0][3])-int(match[0][1]))
                    lrec.append(match)
                    lyear.append(i)
                    lmatch_no.append(j)
                f.close()
            except FileNotFoundError:
                continue
    print('\nWIN BY THE HIGHEST MARGIN :')
    htable.field_names=['Year','Match Number','Match','Point Difference']
    ltable.field_names=['Year','Match Number','Match','Point Difference']
    for i in range(len(hrec)):
        htable.add_row([hyear[i],hmatch_no[i],hrec[i][0][0]+' vs '+hrec[i][0][2],int(high)])
    print(htable)
    print()
    print('\nWIN BY THE LOWEST MARGIN :')
    for i in range(len(lrec)):
        ltable.add_row([lyear[i],lmatch_no[i],lrec[i][0][0]+' vs '+lrec[i][0][2],int(low)])
    print(ltable)
    print()
    print('-'*167)
    print('HOUSE WITH HIGHEST NUMBER OF POINTS IN QUIDDITCH :')
    mptable=PrettyTable()
    mptable.field_names=['House','Points']
    lptable=PrettyTable()
    lptable.field_names=['House','Points']
    cursor.execute('select sum(gryffindor),sum(hufflepuff),sum(ravenclaw),sum(slytherin) from quid')
    d=cursor.fetchall()
    mhigh,mlow=0,10000000
    highest,lowest=[],[]
    for i in d:
        for j in i:
            if j>=mhigh:
                mhigh=j
            elif j<=mlow:
                mlow=j
    for i in d:
        if i[0]>=mhigh:
            highest.append(['Gryffindor',i[0]])
        elif i[0]<=mlow:
            lowest.append(['Gryffindor',i[0]])
        if i[1]>=mhigh:
            highest.append(['Hufflepuff',i[1]])
        elif i[1]<=mlow:
            lowest.append(['Hufflepuff',i[1]])
        if i[2]>=mhigh:
            highest.append(['Ravenclaw',i[2]])
        elif i[2]<=mlow:
            lowest.append(['Ravenclaw',i[2]])
        if i[3]>=mhigh:
            highest.append(['Slytherin',i[3]])
        elif i[3]<=mlow:
            lowest.append(['Slytherin',i[3]])
    for i in highest:
        mptable.add_row(i)
    print(mptable)
    print()
    print('\nHOUSE WITH LOWEST NUMBER OF POINTS IN QUIDDITCH :')
    for i in lowest:
        lptable.add_row(i)
    print(lptable)
    print()
    print('-'*167)
    wins()
    mwins()
    print()
#------------------------------------------------------------------------------------------
def mwins():
    global path
    gcount,hcount,rcount,scount=0,0,0,0
    high,low=0,10000
    for i in range(2000,2051):
        for j in range(1,7):
            try:
                f=open(path+'\\CSC Project\\Years\\'+str(i)+'\\Matches\\Match '+str(j)+'.csv',newline='\n')
                r=csv.reader(f)
                match=[]
                for k in r:
                    match.append(k)
                if match[0][4]=='Gryffindor':
                    gcount+=1
                if match[0][4]=='Hufflepuff':
                    hcount+=1
                if match[0][4]=='Ravenclaw':
                    rcount+=1
                if match[0][4]=='Slytherin':
                    scount+=1
            except FileNotFoundError:
                continue
    wins=[['Gryffindor',gcount],['Hufflepuff',hcount],['Ravenclaw',rcount],['Slytherin',scount]]
    for i in wins:
        if i[1]>=high:
            high=i[1]
        if i[1]<=low:
            low=i[1]
    winners,losers=[],[]
    wtable=PrettyTable()
    wtable.field_names=['House','No. of Match Wins']
    ltable=PrettyTable()
    ltable.field_names=['House','No. of Match Wins']
    for i in wins:
        if i[1]>=high:
            winners.append(i)
        if i[1]<=low:
            losers.append(i)
    for i in winners:
        wtable.add_row(i)
    for i in losers:
        ltable.add_row(i)
    print('\nHOUSE WITH HIGHEST NUMBER OF MATCH WINS :')
    print(wtable)
    print()
    print('\nHOUSE WITH LOWEST NUMBER OF MATCH WINS :')
    print(ltable)
#------------------------------------------------------------------------------------------
def wins():
    cursor.execute('select count(*) from quid where winners=\'gryffindor\'')
    d=cursor.fetchall()
    for i in d:
        gryffindor=i[0]
    cursor.execute('select count(*) from quid where winners=\'hufflepuff\'')
    d=cursor.fetchall()
    for i in d:
        hufflepuff=i[0]
    cursor.execute('select count(*) from quid where winners=\'ravenclaw\'')
    d=cursor.fetchall()
    for i in d:
        ravenclaw=i[0]
    cursor.execute('select count(*) from quid where winners=\'slytherin\'')
    d=cursor.fetchall()
    for i in d:
        slytherin=i[0]
    twins=[['Gryffindor',gryffindor],['Hufflepuff',hufflepuff],['Ravenclaw',ravenclaw],['Slytherin',slytherin]]
    high,low=0,10000
    highest,lowest=[],[]
    for i in twins:
        if i[1]>=high:
            high=i[1]
        elif i[1]<=low:
            low=i[1]
    for i in twins:
        if i[1]>=high:
            highest.append(i)
        elif i[1]<=low:
            lowest.append(i)
    print('HOUSE WITH HIGHEST NUMBER OF TOURNAMENT WINS :')
    wtable=PrettyTable()
    ltable=PrettyTable()
    wtable.field_names=['House','No. of Tournament Wins']
    ltable.field_names=['House','No. of Tournament Wins']
    for i in highest:
        wtable.add_row(i)
    print(wtable)
    print('\nHOUSE WITH LOWEST NUMBER OF TOURNAMENT WINS :')
    for i in lowest:
        ltable.add_row(i)
    print(ltable)
#------------------------------------------------------------------------------------------
def tournament():
    global path
    ptable=PrettyTable()
    print('-'*71,'QUIDDITCH TOURNAMENT','-'*74)
    f=open(path+'\\CSC Project\\Buffer files\\status.txt')
    status=f.read()
    f.close()
    choice=''
    if status=='1':
        choice=input('\n There is no existing tournament going on. Do you want to start a new tournament? ')
        print('\n')
        if choice=='yes':
            mfile=open(path+'\\CSC Project\\Buffer files\\match.csv','w')
            mfile.close()
            ntournament()
            matches()
    elif status=='7':
        print('The previous tournament has ended.')
        f2=open(path+'\\CSC Project\\Buffer files\\status.txt','w')
        f2.write('1')
        f2.close()
        print('\n')
        print('\n| MATCHES HELD IN THIS TOURNAMENT |')
        mfile=open(path+'\\CSC Project\\Buffer files\\match.csv',newline='\n')
        me=csv.reader(mfile)
        ptable.field_names=['Match No.','Team 1','Points_1','Team 2','Points_2','Winners']
        for i in me:
            row=[]
            for j in i:
                row.append(j)
            ptable.add_row(row)
        print(ptable)
        points()
    else:
        ofile=open(path+'\\CSC Project\\Buffer files\\order.csv',newline='\n')
        ore=csv.reader(ofile)
        print('\nThere is a tournament currently going on.')
        print('\n| COMPLETED MATCHES |')
        mfile=open(path+'\\CSC Project\\Buffer files\\match.csv',newline='\n')
        mre=csv.reader(mfile)
        ptable.field_names=['Match No.','Team 1','Points_1','Team 2','Points_2','Winners']
        for i in mre:
            row=[]
            for j in i:
                row.append(j)
            ptable.add_row(row)
        print(ptable)
        pttable()
        print('\n| REMAINING MATCHES |')
        order=[]
        for i in ore:
            order.append(i)
        ofile.close()
        status=int(status)
        for i in order:
            print('\nMatch',status,':',i[0],'vs',i[1])
            status+=1
        matches()
#------------------------------------------------------------------------------------------
def ntournament():
    global path
    print('-'*74,'NEW TOURNAMENT','-'*77)
    print('\n| HOW THE TOURNAMENT WORKS |')
    print('\n1. Each tournament will consist of 6 matches between the 4 houses of Gryffindor, Hufflepuff, Ravenclaw and Slytherin.')
    print('\n2. At the end of the tournament the house with most points will be declared winner.')
    print('\n3. In the case of a tie for the winning spot, the house with more number of wins will be declared winner.')
    print('\n| POINTS SYSTEM |')
    print('\n1. Each goal scored will add 10 points to the scoreboard for the scoring team.')
    print('\n2. Catching the golden snitch will fetch 150 points for the scoring team and the match is declared over.')
    print('\n3. In the case where no team has yet caught the snitch, the first team to score 250 points is declared winner.')
    while True:
        try:
            while True:
                year=int(input('\nEnter the year : '))
                s='select * from quid where year=\'{}\''.format(year)
                cursor.execute(s)
                cursor.fetchall()
                r=cursor.rowcount
                if r==0:
                    if year>2050 or year<2000:
                        print('\nPlease input a year between 2000 and 2050.')
                        continue
                    else:
                        break
                else:
                    print('\nA tournament has already taken place in the year',year,'.')
                    continue
        except ValueError:
            print('\nPlease input a valid year, not alphabets.')
            continue
        break
    f=open(path+'\\CSC Project\\Buffer files\\year.txt','w')
    f.write(str(year))
    f.close()
    os.mkdir(path+'\\CSC Project\\Years\\'+str(year))
    os.mkdir(path+'\\CSC Project\\Years\\'+str(year)+'\\Matches')
    os.mkdir(path+'\\CSC Project\\Years\\'+str(year)+'\\Match Logs')
    print('\n| MATCHES TO BE HELD IN THIS TOURNAMENT |')
    generator()
#------------------------------------------------------------------------------------------
def generator():
    global path
    l=[['Gryffindor','Hufflepuff'],['Gryffindor','Ravenclaw'],['Gryffindor','Slytherin'],['Hufflepuff','Ravenclaw'],['Hufflepuff','Slytherin'],['Ravenclaw','Slytherin']]
    count=1
    order=[]
    for i in range(6,0,-1):
        match=random.randint(1,i)
        print('\nMatch',count,':',l[match-1][0],'vs',l[match-1][1])
        order.append(l[match-1])
        l.pop(match-1)
        count+=1
    f=open(path+'\\CSC Project\\Buffer files\\order.csv','w')
    w=csv.writer(f)
    for j in order:
        w.writerow(j)
    f.close()
#------------------------------------------------------------------------------------------
def matches():
    global path
    f=open(path+'\\CSC Project\\Buffer files\\status.txt')
    status=f.read()
    f.close()
    f2=open(path+'\\CSC Project\\Buffer files\\order.csv','r',newline='\n')
    re=csv.reader(f2)
    order=[]
    for j in re:
        order.append(j)
    f2.close()
    yf=open(path+'\\CSC Project\\Buffer files\\year.txt')
    year=yf.read()
    yf.close()
    print('\nStart Match',status,'? ',end='')
    ch=input()
    if ch=='yes':
        lf=open(path+'\\CSC Project\\Years\\'+year+'\\Match Logs\\Match'+status+'.txt','w')
        print('-'*77,'MATCH',status,'-'*81)
        print(' '*66,'|',order[0][0],'vs',order[0][1],'|')
        lf.write(order[0][0]+' vs '+order[0][1]+'\n')
        print('\n| INSTRUCTIONS TO ENTER POINTS |')
        print('\n1. To enter points, enter the first letter of the name of the house that scored.')
        print('\n2. Next, enter \'goal\' if the team has scored a goal.')
        print('\n3. Enter \'snitch\' if the team has caught the snitch.')
        pts=''
        pt1,pt2=0,0
        while pts.capitalize()!='Snitch':
            house=input('\nHouse--> ')
            lf.write('\nHouse--> '+house)
            if house.capitalize()==order[0][0][0]:
                while True:
                    pts=input('\nGoal/Snitch--> ')
                    lf.write('\nGoal/Snitch--> '+pts)
                    if pts.capitalize()=='Goal':
                        pt1+=10
                        print()
                        print(order[0][0],'has scored a goal ! Ten points to',order[0][0],'!')
                        lf.write('\n'+order[0][0]+' has scored a goal ! Ten points to '+order[0][0]+' !')
                        if pt1==250:
                            print('\n')
                            print(order[0][0],'has scored 250 points !',order[0][0],'wins !')
                            lf.write('\n'+order[0][0]+' has scored 250 points ! '+order[0][0]+' wins !')
                            win=order[0][0]
                            pts='snitch'
                            break
                        print('\nScores |',order[0][0],':',pt1,',',order[0][1],':',pt2)
                        lf.write('\nScores | '+order[0][0]+' : '+str(pt1)+' , '+order[0][1]+' : '+str(pt2))
                        break
                    elif pts.capitalize()=='Snitch':
                        pt1+=150
                        print()
                        print(order[0][0],'has caught the snitch !',order[0][0],'wins !')
                        lf.write('\n'+order[0][0]+' has caught the snitch ! '+order[0][0]+' wins !')
                        win=order[0][0]
                        break
                    else:
                        print('\nInvalid Input. . .')
                        lf.write('\nInvalid Input. . .')
                        continue
            elif house.capitalize()==order[0][1][0]:
                while True:
                    pts=input('\nGoal/Snitch--> ')
                    lf.write('\nGoal/Snitch--> '+pts)
                    if pts.capitalize()=='Goal':
                        pt2+=10
                        print('\n')
                        print(order[0][1],'has scored a goal ! Ten points to',order[0][1],'!')
                        lf.write('\n'+order[0][1]+' has scored a goal ! Ten points to '+order[0][1]+' !')
                        if pt2==250:
                            print('\n')
                            print(order[0][1],'has scored 250 points !',order[0][1],'wins !')
                            lf.write('\n'+order[0][1]+' has scored 250 points ! '+order[0][1]+' wins !')
                            win=order[0][1]
                            pts='snitch'
                            break
                        print('\nScores |',order[0][0],':',pt1,',',order[0][1],':',pt2)
                        lf.write('\nScores | '+order[0][0]+' : '+str(pt1)+' , '+order[0][1]+' : '+str(pt2))
                        break
                    elif pts.capitalize()=='Snitch':
                        pt2+=150
                        print('\n')
                        print(order[0][1],'has caught the snitch !',order[0][1],'wins !')
                        lf.write('\n'+order[0][1]+' has caught the snitch ! '+order[0][1]+' wins !')
                        win=order[0][1]
                        break
                    else:
                        print('\nInvalid Input. . .')
                        lf.write('\nInvalid Input. . .')
                        continue
            else:
                print('\nInvalid Input. . .')
                lf.write('\nInvalid Input. . .')
                continue
        print('\nTotal Points scored by',order[0][0],':',pt1)
        lf.write('\nTotal Points scored by '+order[0][0]+' : '+str(pt1))
        print('\nTotal Points scored by',order[0][1],':',pt2)
        lf.write('\nTotal Points scored by '+order[0][1]+' : '+str(pt2))
        print('\n',' '*71,'MATCH',status,'HAS ENDED')
        lf.write('\nMATCH '+status+' HAS ENDED')
        matchf=open(path+'\\CSC Project\\Years\\'+year+'\\Matches\\Match '+status+'.csv','w')
        matchw=csv.writer(matchf)
        matchw.writerow([order[0][0],pt1,order[0][1],pt2,win])
        matchf.close()
        mfile=open(path+'\\CSC Project\\Buffer files\\match.csv','a')
        mw=csv.writer(mfile)
        mrec=[status,order[0][0],pt1,order[0][1],pt2,win]
        mw.writerow(mrec)
        mfile.close()
        order.pop(0)
        f3=open(path+'\\CSC Project\\Buffer files\\order.csv','w')
        wr=csv.writer(f3)
        for k in order:
            wr.writerow(k)
        f3.close()
        f4=open(path+'\\CSC Project\\Buffer files\\status.txt','w')
        stat=int(status)
        stat+=1
        status=str(stat)
        f4.write(status)
        f4.close()
        lf.close()
#------------------------------------------------------------------------------------------
def pttable():
    global path
    ptable=PrettyTable()
    f=open(path+'\\CSC Project\\Buffer files\\match.csv',newline='\n')
    fre=csv.reader(f)
    point=[]
    for i in fre:
        point.append(i)
    f.close()
    gpts,hpts,rpts,spts=0,0,0,0
    high=0
    for j in point:
        if j[1]=='Gryffindor':
            gpts+=int(j[2])
            if gpts>=high:
                high=gpts
                hteam='Gryffindor'
        if j[3]=='Gryffindor':
            gpts+=int(j[4])
            if gpts>=high:
                high=gpts
                hteam='Gryffindor'
        if j[1]=='Hufflepuff':
            hpts+=int(j[2])
            if hpts>=high:
                high=hpts
                hteam='Hufflepuff'
        if j[3]=='Hufflepuff':
            hpts+=int(j[4])
            if hpts>=high:
                high=hpts
                hteam='Hufflepuff'
        if j[1]=='Ravenclaw':
            rpts+=int(j[2])
            if rpts>=high:
                high=rpts
                hteam='Ravenclaw'
        if j[3]=='Ravenclaw':
            rpts+=int(j[4])
            if rpts>=high:
                high=rpts
                hteam='Ravenclaw'
        if j[1]=='Slytherin':
            spts+=int(j[2])
            if spts>=high:
                high=spts
                hteam='Slytherin'
        if j[3]=='Slytherin':
            spts+=int(j[4])
            if spts>=high:
                high=spts
                hteam='Slytherin'
    print('\n| POINTS TABLE |')
    yf=open(path+'\\CSC Project\\Buffer files\\year.txt')
    year=yf.read()
    yf.close()
    pf=open(path+'\\CSC Project\\Years\\'+year+'\\ptable.csv','w')
    pw=csv.writer(pf)
    pw.writerow(['Gryffindor','Hufflepuff','Ravenclaw','Slytherin'])
    pw.writerow([gpts,hpts,rpts,spts])
    pf.close()
    ptable.field_names=['Gryffindor','Hufflepuff','Ravenclaw','Slytherin']
    ptable.add_row([gpts,hpts,rpts,spts])
    print(ptable)
    print('\n')
    print(hteam,'leads with',high,'points.')
#------------------------------------------------------------------------------------------
def points():
    global path
    ptable=PrettyTable()
    f=open(path+'\\CSC Project\\Buffer files\\match.csv',newline='\n')
    fre=csv.reader(f)
    point=[]
    for i in fre:
        point.append(i)
    f.close()
    gpts,hpts,rpts,spts=0,0,0,0
    high=0
    for j in point:
        if j[1]=='Gryffindor':
            gpts+=int(j[2])
            if gpts>=high:
                high=gpts
        if j[3]=='Gryffindor':
            gpts+=int(j[4])
            if gpts>=high:
                high=gpts
        if j[1]=='Hufflepuff':
            hpts+=int(j[2])
            if hpts>=high:
                high=hpts
        if j[3]=='Hufflepuff':
            hpts+=int(j[4])
            if hpts>=high:
                high=hpts
        if j[1]=='Ravenclaw':
            rpts+=int(j[2])
            if rpts>=high:
                high=rpts
        if j[3]=='Ravenclaw':
            rpts+=int(j[4])
            if rpts>=high:
                high=rpts
        if j[1]=='Slytherin':
            spts+=int(j[2])
            if spts>=high:
                high=spts
        if j[3]=='Slytherin':
            spts+=int(j[4])
            if spts>=high:
                high=spts
    f2=open(path+'\\CSC Project\\Buffer files\\year.txt')
    year=f2.read()
    f2.close()
    year=int(year)
    if high==gpts:
        win='Gryffindor'
        teach='Minerva McGonagall'
    elif high==hpts:
        win='Hufflepuff'
        teach='Pomona Sprout'
    elif high==rpts:
        win='Ravenclaw'
        teach='Filius Flitwick'
    elif high==spts:
        win='Slytherin'
        teach='Severus Snape'
    print('\n| POINTS TABLE |')
    ptable.field_names=['Gryffindor','Hufflepuff','Ravenclaw','Slytherin']
    ptable.add_row([gpts,hpts,rpts,spts])
    print(ptable)
    print('\nWINNERS OF THE',year,'QUIDDITCH CUP :',win,'!')
    print('\nCONGRATULATIONS !')
    s='insert into quid values(\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'.format(year,gpts,hpts,rpts,spts,win,teach)
    cursor.execute(s)
    conn.commit()
#------------------------------------------------------------------------------------------
def archives():
    global path
    print('-'*77,'ARCHIVES','-'*80)
    ptable=PrettyTable()
    while True:
        try:
            while True:
                try:
                    year=int(input('\nEnter the year : '))
                    f=open(path+'\\CSC Project\\Years\\'+str(year)+'\\ptable.csv',newline='\n')
                except FileNotFoundError:
                    print('\nNo tournament has taken place in the year',year,'.')
                    continue
                break
        except ValueError:
            print('\nPlease input a valid year, not alphabets.')
            continue
        break
    while True:
        try:
            while True:
                c=int(input('\n1.Points Table | 2.Match Logs | 3.Scores\n\nEnter your choice : '))
                if c==1:
                    print()
                    print('| POINTS TABLE OF THE YEAR',year,'|')
                    f=open(path+'\\CSC Project\\Years\\'+str(year)+'\\ptable.csv',newline='\n')
                    fr=csv.reader(f)
                    t=[]
                    for i in fr:
                        t.append(i)
                    ptable.field_names=t[0]
                    ptable.add_row(t[1])
                    print()
                    print(ptable)
                    f.close()
                    break
                elif c==2:
                    count=0
                    for i in range(6):
                        try:
                            f=open(path+'\\CSC Project\\Years\\'+str(year)+'\\Match Logs\\Match'+str(i+1)+'.txt')
                            line=f.readline()
                            print('\n'+'Match '+str(i+1)+' : '+line)
                            count+=1
                            f.close()
                        except FileNotFoundError:
                            continue
                    while True:
                        try:
                            while True:
                                m=int(input('\nEnter match number (1-'+str(count)+') : '))
                                if m not in range(1,count+1):
                                    print('\nPlease input a valid option (1-'+str(count)+') . . .')
                                    continue
                                else:
                                    break
                        except ValueError:
                            print('\nPlease input a numbered option (1-'+str(count)+'), not letters. . .')
                            continue
                        break
                    f=open(path+'\\CSC Project\\Years\\'+str(year)+'\\Match Logs\\Match'+str(m)+'.txt')
                    log=f.read()
                    print()
                    print('| MATCH',m,'LOG |')
                    print()
                    print(log)
                    f.close()
                    break
                elif c==3:
                    count=0
                    for i in range(6):
                        try:
                            f=open(path+'\\CSC Project\\Years\\'+str(year)+'\\Match Logs\\Match'+str(i+1)+'.txt')
                            line=f.readline()
                            print('\n'+'Match '+str(i+1)+' : '+line)
                            count+=1
                            f.close()
                        except FileNotFoundError:
                            continue
                    while True:
                        try:
                            while True:
                                m=int(input('\nEnter match number (1-'+str(count)+') : '))
                                if m not in range(1,count+1):
                                    print('\nPlease input a valid option (1-'+str(count)+') . . .')
                                    continue
                                else:
                                    break
                        except ValueError:
                            print('\nPlease input a numbered option (1-'+str(count)+'), not letters. . .')
                            continue
                        break
                    print('-'*167)
                    f=open(path+'\\CSC Project\\Years\\'+str(year)+'\\Matches\\Match '+str(m)+'.csv',newline='\n')
                    fr=csv.reader(f)
                    l=[]
                    for i in fr:
                        l=i
                    print()
                    print('| MATCH',m,'|')
                    print()
                    print(l[0],'vs',l[2])
                    print()
                    print(l[0],':',l[1],',',l[2],':',l[3],'| Winners :',l[4])
                    print()
                    break
                else:
                    print('\nInvalid Input. . .')
                    continue
        except ValueError:
            print('\nPlease enter a valid option, not letters. . .')
            continue
        print()
        break
#Main Program-----------------------------------------------------------------------------------
print('-'*167)
print(' '*55,'Welcome to Hogwarts School of Witchcraft and Wizardry\n')
print('-'*167)
print('\n')
m=1
while m==1:
    while True:
        print('-'*74,'HOUSE DATABASE','-'*77)
        try:
            print('\n1.Students database | 2.Professors database | 3.Quidditch | 4.Exit')
            k=int(input('\nEnter your choice : '))
        except ValueError:
            print('\nPlease input a numbered option, not letters. . .')
            continue
        if k==1:
            m=2
            while m==2:
                print('-'*73,'STUDENTS DATABASE','-'*75)
                print()
                while True:
                    try:
                        print('1.Display all student records | 2.Specific Field Reports | 3.Add new records | 4.Update an existing record | 5.Delete an existing record')
                        k2=int(input('\nEnter your choice : '))
                    except ValueError:
                        print('\nPlease input a numbered option, not letters. . .')
                        print('-'*167)
                        continue
                    if k2==1:
                        print('\n')
                        read()
                        break
                    elif k2==2:
                        print('\n')
                        display()
                        break
                    elif k2==3:
                        print('\n')
                        add()
                        break
                    elif k2==4:
                        print('\n')
                        update()
                        break
                    elif k2==5:
                        print('\n')
                        delete()
                        break
                    else:
                        print('\nInvalid input. . .Try again. . .')
                        print('-'*167)
                        continue
                print('-'*167)
                while True:
                    try:
                        m=int(input('Return to : 1.Main Menu | 2.Student Database Menu\n\nEnter your choice : '))
                        if m not in [1,2]:
                            print('\nPlease input either 1 or 2 . . .')
                            print('-'*167)
                            continue
                    except ValueError:
                        print('\nEnter a numbered option, not letters. . .')
                        print('-'*167)
                        continue
                    break
        elif k==2:
            print('\n')
            m=2
            while m==2:
                print('-'*72,'PROFESSORS DATABASE','-'*73)
                while True:
                    try:
                        print('\n1.Display all records | 2.Specific Field Reports')
                        k2=int(input('\nEnter your choice : '))
                    except ValueError:
                        print('\nPlease input a numbered option, not letters. . .')
                        print('-'*167)
                        continue
                    if k2==1:
                        pread()
                        break
                    elif k2==2:
                        pdisplay()
                        break
                    else:
                        print('\nInvalid input. . . Try again. . .')
                        print('-'*167)
                        continue
                print('-'*167)
                while True:
                    try:
                        m=int(input('Return to : 1.Main Menu | 2.Professor Database Menu\n\nEnter your choice : '))
                        if m not in [1,2]:
                            print('\nPlease input either 1 or 2 . . .')
                            print('-'*167)
                            continue
                    except ValueError:
                        print('\nEnter a numbered option, not letters. . .')
                        print('-'*167)
                        continue
                    break
        elif k==3:
            m=2
            while m==2:
                quidw()
                print('-'*167)
                while True:
                    try:
                        m=int(input('Return to : 1.Main Menu | 2.Quidditch Database Menu\n\nEnter your choice : '))
                        if m not in [1,2]:
                            print('\nPlease input either 1 or 2 . . .')
                            print('-'*167)
                            continue
                    except ValueError:
                        print('\nEnter a numbered option, not letters. . .')
                        print('-'*167)
                        continue
                    break
        elif k==4:
            print('-'*167)
            break
        else:
            print('\nInvalid input. . . Try again. . .')
            continue
    break
conn.close()
#============================================================== END =========================================================================
