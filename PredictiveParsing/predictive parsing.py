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
count=[]
for i in range(len(lhs)):
    positions=firstFun2(lhs[i],rhs[i])
    for j in range(len(positions)):
        c = 1
        k = (lhs[i], positions[j])
        if k in table:
            c = c + 1
        table[k] = productions[i]
        count.append(c)

str1=splitStr(str)
str1.append('$')

stack='$E'
steps=[]
generation=[]
stringtrack=[]
i=1
j=0
str1


def generate(str1, stack, i, j):
    try:
        while True:
            if '~' in stack:
                stack = stack.replace('~', '')
            if stack[i] == str1[j] and stack[i] == '$':
                return 'Accepted'

            if stack[i] == '~':
                stack = stack.replace('~', '')

            # print(str[j])
            if stack[i] == str1[j] and stack[i] != '$':
                stack = stack[:-1]
                j = j + 1
                i = len(stack) - 1

                stringtrack.append(str[j:])
                steps.append(table[(stack[i], str1[j])])
                generation.append(stack)
            else:
                val = table[(stack[i], str1[j])].split('->')[1]
                val = val[::-1]
                new = stack.replace(stack[i], val, 1)
                steps.append(table[(stack[i], str1[j])])
                stack = new

                i = len(stack) - 1
                stringtrack.append(str[j:])

                if '~' in stack:
                    stack = stack.replace('~', '')
                    i = len(stack) - 1
                generation.append(stack)
    except:
        return 1


flag =generate(str1,stack,i,j)
for i in range(len(stringtrack)):
    stringtrack[i]=stringtrack[i]+'$'

def display():
    print('*********************Predictive parsing(LL parser) *******************')
    for x in count:
        if x!=1:
            print('The given Grammar is not LL(1)')
            return
    if flag==1:
        print(' Can not parse string  ')
    else:
        print(' * The given Grammar is LL(1)')
        print('Stack',' '*(18- len('stack')),'Input',end='')
        print(" "*16,'Operation')
        print('')
        for i in range(len(stringtrack)):
            print(generation[i]," "*(18-len(generation[i])),stringtrack[i],end='')
            print(' '*(18-len(stringtrack[i])),"[",steps[i],"]")
            print('')
    print(' Successful completion of parsing ')

display()