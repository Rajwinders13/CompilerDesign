print(" Transition for NFA That you want to convert Using states(q0,q1,....) and alphabet (a.b) :")
print("Enter Number Of States :")
nstates=int(input())

symbol=['a','b']
states_nfa=[]
for i in range(nstates):
    states_nfa.append('q'+str(i))
print("STATES")
print(states_nfa)

list1_nfa=[]
for i in range(len(symbol)):
    for j in range(nstates):
        list1_nfa.append(states_nfa[j]+","+symbol[i])

#print(list1_nfa)

list2_nfa=[]
for i in range(len(list1_nfa)):
    print("Enter No. of transition for "+list1_nfa[i]+":")
    n=int(input())
    temp=[]
    if n==0:
        temp.append('#')
    for j in range(n):
        print("Enter state :")
        temp.append(input())
    list2_nfa.append(temp)

#input final and initial states
initial='q0'
print("Enter final state: ")
final=input()

#NFA to DFA
list1=list1_nfa.copy()
list2=list2_nfa.copy()

states=[]
symbol=['a','b']

listnfa1=[]
listnfa2=[]
checklist=[['q0']]
states=[['q0']]

for i in range(len(list1)):
    if 'q0' in list1[i]:
        listnfa1.append(list1[i])
        listnfa2.append(list2[i])

#print("listnfa1: ")
#print(listnfa1)
while True:
    for i in range(len(listnfa2)):
        if listnfa2[i] not in checklist:
            templist=[]
            templist=listnfa2[i].copy()
            print(templist)
            nfa1=[]
            nfa2=[]
            nfa3=[]
            nfa4=[]
            for j in range(len(templist)):
                for i in range(len(list1)):
                    var=str(templist[j]+",a")
                    var2=str(templist[j]+",b")
                    if var in list1[i]:
                        for k in range(len(list2[i])):
                            nfa1.append(list2[i][k])
                    elif var2 in list1[i]:
                        for k in range(len(list2[i])):
                            nfa3.append((list2[i][k]))
            for d in nfa1:
                if d not in nfa2 and d!='#':
                    nfa2.append(d)
            nfa1.sort()
            nfa2.sort()
            for d in nfa3:
                if d not in nfa4 and d!='#':
                    nfa4.append(d)
            nfa3.sort()
            nfa4.sort()
            listnfa1.append(str(templist)+",a")
            listnfa2.append(nfa2)
            listnfa1.append(str(templist) + ",b")
            listnfa2.append(nfa4)
            checklist.append(templist)
            if templist not in states:
                states.append(templist)

    #print("cheklist:")
    #print(checklist)
    tempchecklist=[]
    for d in listnfa2:
        if d not in tempchecklist and d != '#':
            tempchecklist.append(d)
    checklist.sort()
    tempchecklist.sort()
    #print("checklist :" + str(checklist))
    #print("tempchecklist :" + str(tempchecklist))
    if checklist==tempchecklist:
        break

#print(nfa1)
#print(nfa2)
#print(listnfa1)
#print(listnfa2)
#print(states)
print("********** Transition Table **********")
print("States"+" "*23,end='')
symbol.sort()
for i in range(len(symbol)):
    print(symbol[i]+" "*(26-(len(str(symbol[i])))),end='')

print("")
count=0
for i in range(len(states)):
    if i==0:
        print("->"+str(states[i])+" "*(23-(len(str(states[i])))),end='')
        print("  "+str(listnfa2[count])+" "*(20-(len(str(listnfa2[count])))),end='')
        print("  "+str(listnfa2[count+1]),end='')
        print("")
        count+=2
    elif final in states[i]:
        print("**" + str(states[i]) + " " * (23 - (len(str(states[i])))), end='')
        print("  " + str(listnfa2[count]) + " " * (20 - (len(str(listnfa2[count])))), end='')
        print("  " + str(listnfa2[count + 1]), end='')
        print("")
        count += 2
    else:
        print("  "+str(states[i]) + " " * (23 - (len(str(states[i])))), end='')
        print("  "+ str(listnfa2[count]) + " " * (20 - (len(str(listnfa2[count])))), end='')
        print("  "+ str(listnfa2[count + 1]), end='')
        print("")
        count += 2


