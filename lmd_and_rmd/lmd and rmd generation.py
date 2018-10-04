from tkinter import*
from tkinter import filedialog

mgui=Tk()

mgui.geometry('450x450+200+200')
mgui.title('SELECT FILE')
def takeInput(filename):
    file=open(filename)
    lines=file.readlines()
    for line in lines:
        line=line.split('\n')[0]
        productions.append(line)
def select():
    mgui.fileName=filedialog.askopenfilename(filetypes=(("Python",".py"),("All files","*.*")))
    takeInput(mgui.fileName)
    mgui.destroy()

print("*******************Enter Grammar******************** ")
alphabets=[]
nonterminals=[]
terminals=[]
productions=[]
print("Choose one ")
print("1. FROM FILE")
print("2. MANUAL INPUT")
option=int(input())
if option==2:
    print("Enter Grammar ( PRODUCTION RULE )")
    while True:
        line = input()
        if line == '?':
            break
        if line:
            productions.append(line)

elif option==1:
    mybutton = Button(mgui, text='SELECT', command=select).pack()
    mgui.mainloop()
print("Production Rules :")
print(productions)
print("Enter Start symbol ")
startsymbol=input()
for production in productions:
    i=0
    while i < len(production):
        if production[i].isupper() and production[i] not in nonterminals:
            nonterminals.append(production[i])
        elif (production[i].islower() or production[i] in '()') and production[i] not in terminals:
            if production[i].islower():
                term=''
                for j in range(i,len(production)):
                    if not production[j].islower():
                        break
                    elif production[j].islower():
                        term=term+production[j]
                        i=i+1
                terminals.append(term)

            else:
                terminals.append(production[i])
        elif production[i] not in '->' and not production[i].isupper() and production[i] not in terminals:
            terminals.append(production[i])
        i=i+1
print("Non terminals  ")
print(nonterminals)
terminals.remove('~')
print("terminals" )
print(terminals)

lhs=[]
rhs=[]
for rule in productions:
    lhs.append(rule.split('->')[0])
    rhs.append(rule.split('->')[1])
print('LHS ',lhs)
print('RHS', rhs)

def splitStr(str):
    stringList=[]
    temp=''
    for i in range(len(str)):
        temp=temp+str[i]
        if temp in terminals:
            stringList.append(temp)
            temp=''
    return stringList

str=input('Input string :')
splitStr(str)


def firstFun(nonterminal):
    firstn = []
    if nonterminal[0] in terminals:
        return nonterminal
    for rule in productions:
        lh = rule.split('->')[0]
        rh = rule.split('->')[1]
        if lh == nonterminal:
            temp = ''
            for i in range(len(rh)):
                temp = temp + rh[i]
                if temp in terminals:
                    firstn.append(temp)
                    temp = ''
                    break
                elif temp == '~':
                    firstn.append('~')
                elif temp in nonterminals:
                    n = firstFun(temp)
                    firstn.extend(n)
                    if '~' in n and isupper(rh):
                        continue

    return firstn

first={}

for each in nonterminals:
    first[each]=firstFun(each)

def followFun(nonterminal):
    follown=[]
    for rule in productions:
        if nonterminal in rule.split('->')[1]:
            if nonterminal==startsymbol:
                follown.append('$')
            lh=rule.split('->')[0]
            rh=rule.split('->')[1]
            index=rh.find(nonterminal)
            if index<len(rh)-1:
                m=firstFun(rh[index+1])
                follown.extend(m)
                if '~' in m:
                    n=followFun(lh)
                    follown.extend(n)
                break
            if index==len(rh)-1:
                n=followFun(lh)
                follown.extend(n)
                break
    if '~' in follown:
        follown.remove('~')
    return follown

follow={}

for each in nonterminals:
    follow[each]=followFun(each)


def firstFun2(l, str):
    temp = ''
    firstn2 = []
    if str[0] in terminals:
        firstn2.append(str[0])
        return firstn2
    if str == '~':
        firstn2.extend(follow[l])
        return firstn2
    else:
        for i in range(len(str)):
            temp = temp + str[i]
            if temp in terminals:
                firstn2.append(temp)
                return firstn2
            if str[i] in nonterminals:
                m = first[str[i]]
                firstn2.extend(m)
                if '~' in m:
                    continue
                else:
                    break

    return firstn2

table={}

for i in range(len(lhs)):
    positions=firstFun2(lhs[i],rhs[i])
    for j in range(len(positions)):
        k=(lhs[i],positions[j])
        table[k]=productions[i]

str1=splitStr(str)
str1.append('$')

stack='E'
steps=[]
generation=[]
stepsrmd=[]
i=0
j=0

def generate(str1,stack,i,j):
    try:
       while True:
        if '~' in stack:
            stack=stack.replace('~','')
        if len(stack)==len(str1)-1 and str1[j]=='$':
            break

        if stack[i]=='~':
            stack=stack.replace('~','')

        if stack[i]==str1[j]:
            if str1[j]!='$':
                j=j+1
            i=i+1
        else:
            val=table[(stack[i],str1[j])].split('->')[1]

            new=stack.replace(stack[i],val,1)
            steps.append(table[(stack[i],str1[j])])
            stack=new
            if '~' in stack:
                stack=stack.replace('~','')
            generation.append(stack)
    except:
        return 1

flag =generate(str1,stack,i,j)

print('*********************String Generation using LMD*******************')
if flag==1:
    print('String can not be generated ')
else:
    print(startsymbol,'=>',generation[0],end='')
    print(" "*16,"[",steps[0],"]")
    print('')
    for i in range(len(steps)):
        print(' '*(len(startsymbol)),'=>',generation[i]," "*(18-len(generation[i])),end='')
        print("[",steps[i],"]")
        print('')

generation=[]
stepsrmd=[]
stack='E'
str1
steps=[]

strrmd=str1[::-1]
strrmd.remove('$')
strrmd.append('$')
i=0
j=len(stack)-1
check=''
k=table.keys()

def funrmd(st,s,i,j):
    try:
        stack=st
        while True:
            if stack==str:
                return stack
            if (stack[j],s[i]) not in k and stack[j] in terminals and s[i] in terminals:
                j-=1
            elif (stack[j],s[i]) not in k and stack[j] not in terminals:
                i+=1
            elif (stack[j],s[i]) in k:
                val=table[(stack[j],s[i])].split('->')[1]
                steps.append(table[(stack[j],s[i])])
                val=val[::-1]
                check=stack[j]
                stack=stack[::-1]
                new=stack.replace(check,val,1)
                stack=new[::-1]
                j=j+len(val)-1
                generation.append(stack)
                if stack[j]==check:
                    i+=1
                if stack[j] in terminals:
                    j=j-1
                if '~' in stack:
                    stack=stack.replace('~','')
                    j=j-1
                    i=0
    except:
        return 2


def generatermd(stack, strrmd, i, j):
    while True:
        if '~' in stack:
            stack = stack.replace('~', '')

        if stack[-1] in terminals:
            s = str1[::]
            flag = funrmd(stack, s, i, j)
            return

        elif (stack[j], strrmd[i]) not in k:
            i += 1
        elif (stack[j], strrmd[i]) in k:
            val = table[(stack[j], strrmd[i])].split('->')[1]
            steps.append(table[(stack[j], strrmd[i])])
            val = val[::-1]
            check = stack[j]
            stack = stack[::-1]
            new = stack.replace(check, val, 1)
            stack = new[::-1]
            generation.append(stack)
            j = len(stack) - 1
            if stack[-1] == check:
                i += 1
            if '~' in stack:
                stack = stack.replace('~', '')
                j = len(stack) - 1
                i = 0

generatermd(stack,strrmd,i,j)

print('*********************String Generation using RMD*******************')
if flag==2:
    print('String can not be generated ')
else:
    print(startsymbol,'=>',generation[0],end='')
    print(" "*16,"[",steps[0],"]")
    print('')
    for i in range(len(steps)):
        print(' '*(len(startsymbol)),'=>',generation[i]," "*(18-len(generation[i])),end='')
        print("[",steps[i],"]")
        print('')