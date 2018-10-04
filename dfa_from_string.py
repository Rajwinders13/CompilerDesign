#generate a dfa from ending with string
import itertools
#input ending with string
print("Enter ending with string :")
st=input()
#input aphabets set

symbol=['a','b']
for i in range(len(st)):
    if st[i] not in symbol:
        symbol.append(st[i])

#generating porssible strings

st1=''
for s in symbol:
    st1=st1+s
print(st1)
possiple_strings=[]
for string in map(''.join, itertools.product(st1, repeat=len(st))):
    possiple_strings.append(string.lower())
possiple_strings.remove(st)
# print(possiple_strings)

nstates=len(st)+1

#put states in states list

states=[]
for i in range(nstates):
    states.append('q'+str(i))

initial=states[0]
final=states[len(st)]

print("States used :"+str(states))

# Default transitions

transition={}
def setTrans(states,st):
    for i in range(len(st)):
        var=(states[i],st[i])
        transition[var]=states[i+1]

setTrans(states,st)

temptransition={}
temptransition=transition.copy()

#to check whether the transition on a state is valid or not
def process(teststr,transitions,startstate,i,new,sym):
    newtransitionset={}
    if teststr[0]==sym:
        newinitial = i

    else:
        newinitial=new
   # print("initial "+newinitial)
    start=startstate
    n=0
    if teststr=='':
        return
    var1=transitions.keys()
    while start < nstates:
        for k in var1:
            if states[start] in k:
                newtransitionset[k]=transitions[k]
        start+=1
   # print(newtransitionset)
    trans=(newinitial,teststr[0])
    loopcount=len(teststr)
    var2=newtransitionset.keys()

    for i in range(1,loopcount):
        if teststr[i]=='':
            return
        for k in var2:
            if k==trans:
                change=newtransitionset[k]
                trans=(newtransitionset[k],teststr[i])
                #print(change)
                #print(trans)
                n+=1
                break;

    for k in var2:
        if k==trans:
            change=newtransitionset[k]
            n+=1
            break;

    if n>=len(teststr):
       return change
    else:
        return

#Transtion function to set transitions

def Transtions(states,symbol):
    for i in range(nstates):
        newi=nstates-i-1
        count=newi+1
        for j in range(len(symbol)):
            key=transition.keys()
            var=(states[newi],symbol[j])
            if var not in key:
                if newi==0:
                    transition[var]=states[newi]
                    temptransition[var]=states[newi]
                else:
                    if var not in key:
                        for n in range(count):
                            #print(states[newi-n])
                           # if i == newi - 1 and states[newi] == states[newi - n]:
                            #    continue;
                            temptransition[var]=states[newi-n]
                            #print(temptransition)
                            value=process(st,temptransition,newi-n,states[newi],states[newi-n],symbol[j])
                            val=[]
                            for p in possiple_strings:
                                val.append(process(p,temptransition,newi-n,states[newi],states[newi-n],symbol[j]))
                                if states[newi]==states[nstates-1]:
                                    val.append(process(p, temptransition, newi - n, states[newi-1], states[newi - n], symbol[j]))
                            #print(final+","+str(value))
                            if value==final and value  not in val:
                                 transition[var]=states[newi-n]
                                 break;
                            else:
                                del temptransition[var]

Transtions(states,symbol)

sorted(transition,key=transition.__getitem__)
#print( "***********************Transitions:************************")
#print(transition)

key=transition.keys()

#transitions a and b  aplphabet
trans_A=[]
trans_B=[]
for each in key:
    if 'a' in each:
        trans_A.append(each)

    else:
        trans_B.append(each)

print("********** Transition Table **********")
print("States    ",end='')
symbol.sort()
for i in range(len(symbol)):
    print(symbol[i]+"     ",end='')

print("")

for i in range(nstates):
    if states[i] == final:
        print("**" + states[i] + "     ", end='')
        for k in trans_A:
            if states[i] in k:
                print(transition[k] + "     ", end='')

        for k in trans_B:
            if states[i] in k:
                print(transition[k] + "     ", end='')
        print("")


    elif states[i]==initial:
        print("->"+states[i] + "     ", end='')
        for k in trans_A:
            if states[i] in k:
                print(transition[k] + "     ", end='')

        for k in trans_B:
            if states[i] in k:
                print(transition[k] + "     ", end='')

        print("")

    else:
        print("  "+states[i]+"     ", end='')
        for k in trans_A:
            if states[i] in k:
                print(transition[k] + "     ", end='')

        for k in trans_B:
            if states[i] in k:
                print(transition[k] + "     ", end='')

        print("")

#string processing

def processstr(teststr):
    if teststr=='':
        return
    var1=transition.keys()
    trans=(initial,teststr[0])
    loopcount=len(teststr)
    for i in range(1,loopcount):
        for k in var1:
            if k==trans:
                change=transition[k]
                trans=(transition[k],teststr[i])
                #print(change)
                #print(trans)
                break;

    for k in var1:
        if k==trans:
            change=transition[k]
            break;
    return change

while(True):
     str=input("Enter string to process :")
     result=processstr(str)

     if result == final:
         print("ACCEPTED ")

     else:
        print("Rejected ")
     ans=input("Want to try more ?(Y/N)")
     if(ans=='y'or ans=='Y'):
         continue;

     else:
         break;













