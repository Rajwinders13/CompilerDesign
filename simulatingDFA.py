#input states
#input dfa and string processing
while True:
   try:
      print("Enter number of states :")
      nstates=int(input())
      break
   except:
      print("Enter integer value :")

states=[]
print("Enter name of states :")
for i in range(nstates):
    states.append(input())

initial=states[0]
print("Initial state :"+initial)

#input symbols

num_input=int(input(("\n Enter number of input symbols :")))
symbol=[]
print("Enter input alphabets :")
for i in range(num_input):
    symbol.append(input())

#transitions
transition={}
for j in range(num_input):
    for i in range(nstates):
        while True:
               print("Enter transition ("+states[i]+","+symbol[j]+"):" )
               t=input()
               if t not in states:
                   print("Enter valid state ")
               else:
                   break
        var=(states[i],symbol[j])
        #print(var)
        transition[var]=t

print(transition)

#final states

num_final=int(input("Enter number of final states"))
final=[]
print("Enter final states/state: ")
for i in range(num_final):
    final.append(input())

#transition table

print("********** Transition Table **********")
print("States    ",end='')
for i in range(num_input):
    print(symbol[i]+"     ",end='')

print("")

for i in range(nstates):
    if states[i] in final:
        print("**" + states[i] + "     ", end='')
        key = transition.keys()
        for k in key:
            if states[i] in k:
                print(transition[k] + "     ", end='')
        print("")


    elif states[i]==initial:
        print("->"+states[i] + "     ", end='')
        key = transition.keys()
        for k in key:
            if states[i] in k:
                print(transition[k] + "     ", end='')
        print("")

    else:
         print("  "+states[i]+"     ",end='')
         key = transition.keys()
         for k in key:
            if states[i] in k:
               print(transition[k]+"     ",end='')
         print("")

#string processing

def process(teststr):
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
     result=process(str)

     if result in final:
         print("ACCEPTED ")

     else:
        print("Rejected ")
     ans=input("Want to try more ?(Y/N)")
     if(ans=='y'or ans=='Y'):
         continue;
     else:
         break;



















