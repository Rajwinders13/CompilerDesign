import pandas as pd
import firstfollow2
from firstfollow2 import production_list, nt_list as ntl, t_list as tl
from collections import OrderedDict
nt_list, t_list = [], []

class State:
    _id = 0

    def __init__(self, closure):
        self.closure = closure
        self.no = State._id
        State._id += 1

class Item(str):
    def __new__(cls, item, lookahead=list()):
        self = str.__new__(cls, item)
        self.lookahead = lookahead
        return self

    def __str__(self):
        return super(Item, self).__str__() + ", " + '|'.join(self.lookahead)

def closure(items):
    def exists(newitem, items):

        for i in items:
            if i == newitem and sorted(set(i.lookahead)) == sorted(set(newitem.lookahead)):
                return True
        return False

    global production_list

    while True:
        flag = 0
        for i in items:

            if i.index('.') == len(i) - 1: continue

            Y = i.split('->')[1].split('.')[1][0]

            if i.index('.') + 1 < len(i) - 1:
                lastr = list(firstfollow2.compute_first(i[i.index('.') + 2]) - set(chr(1013)))

            else:
                lastr = i.lookahead

            for prod in production_list:
                head, body = prod.split('->')

                if head != Y: continue

                newitem = Item(Y + '->.' + body, lastr)

                if not exists(newitem, items):
                    items.append(newitem)
                    flag = 1
        if flag == 0: break

    return items


from collections import OrderedDict

def goto(items, symbol):
    global production_list
    initial = []

    for i in items:
        if i.index('.') == len(i) - 1: continue

        head, body = i.split('->')
        seen, unseen = body.split('.')

        if unseen[0] == symbol and len(unseen) >= 1:
            initial.append(Item(head + '->' + seen + unseen[0] + '.' + unseen[1:], i.lookahead))

    return closure(initial)


def calc_states():
    def contains(states, t):

        for s in states:
            if len(s) != len(t): continue

            if sorted(s) == sorted(t):
                for i in range(len(s)):
                    if s[i].lookahead != t[i].lookahead: break
                else:
                    return True

        return False

    global production_list, nt_list, t_list

    head, body = production_list[0].split('->')

    states = [closure([Item(head + '->.' + body, ['$'])])]

    while True:
        flag = 0
        for s in states:

            for e in nt_list + t_list:

                t = goto(s, e)
                if t == [] or contains(states, t): continue

                states.append(t)
                flag = 1

        if not flag: break

    return states


def make_table(states):
    global nt_list, t_list

    def getstateno(t):

        for s in states:
            if len(s.closure) != len(t): continue

            if sorted(s.closure) == sorted(t):
                for i in range(len(s.closure)):
                    if s.closure[i].lookahead != t[i].lookahead: break
                else:
                    return s.no

        return -1

    def getprodno(closure):

        closure = ''.join(closure).replace('.', '')
        return production_list.index(closure)

    SLR_Table = OrderedDict()

    for i in range(len(states)):
        states[i] = State(states[i])

    for s in states:
        SLR_Table[s.no] = OrderedDict()

        for item in s.closure:
            head, body = item.split('->')
            if body == '.':
                for term in item.lookahead:
                    if term not in SLR_Table[s.no].keys():
                        SLR_Table[s.no][term] = {'r' + str(getprodno(item))}
                    else:
                        SLR_Table[s.no][term] |= {'r' + str(getprodno(item))}
                continue

            nextsym = body.split('.')[1]
            if nextsym == '':
                if getprodno(item) == 0:
                    SLR_Table[s.no]['$'] = 'accept'
                else:
                    for term in item.lookahead:
                        if term not in SLR_Table[s.no].keys():
                            SLR_Table[s.no][term] = {'r' + str(getprodno(item))}
                        else:
                            SLR_Table[s.no][term] |= {'r' + str(getprodno(item))}
                continue

            nextsym = nextsym[0]
            t = goto(s.closure, nextsym)
            if t != []:
                if nextsym in t_list:
                    if nextsym not in SLR_Table[s.no].keys():
                        SLR_Table[s.no][nextsym] = {'s' + str(getstateno(t))}
                    else:
                        SLR_Table[s.no][nextsym] |= {'s' + str(getstateno(t))}

                else:
                    SLR_Table[s.no][nextsym] = str(getstateno(t))

    return SLR_Table


def augment_grammar():
    for i in range(ord('Z'), ord('A') - 1, -1):
        if chr(i) not in nt_list:
            start_prod = production_list[0]
            production_list.insert(0, chr(i) + '->' + start_prod.split('->')[0])
            return
lalrdict={}

def main():
    global production_list, ntl, nt_list, tl, t_list,table

    firstfollow2.main()

    print("\tFIRST AND FOLLOW OF NON-TERMINALS")
    for nt in ntl:
        firstfollow2.compute_first(nt)
        firstfollow2.compute_follow(nt)
        print(nt)
        print("\tFirst:\t", firstfollow2.get_first(nt))
        print("\tFollow:\t", firstfollow2.get_follow(nt), "\n")

    augment_grammar()
    nt_list = list(ntl.keys())
    t_list = list(tl.keys()) + ['$']

    j = calc_states()

    ctr = 0
    for s in j:
        t=[]

        for i in s:
            t.append(i)
        lalrdict[ctr]=t
        ctr += 1

    table = make_table(j)

    sr, rr = 0, 0
    new = {}
    for k, v in table.items():
        new[k] = dict(v)
    return


if __name__ == "__main__":
    main()

lalrdict2={}
item=[]
lookahead=[]
k=lalrdict.keys()

for i in k:
    it = []
    lo = []
    for j in range(len(lalrdict[i])):
        it.append(str(lalrdict[i][j]).split(',')[0])
        lo.append(str(lalrdict[i][j]).split(',')[1])

    item.append(it)
    lookahead.append(lo)

def findmatch(l1,index1):
    for i in range((index1+1),len(l1)):
        var=[]
        for j in range(len(l1[i])):
            var.append(l1[i][j])
        if l1[index1]==l1[i]:
            return i
same=[]
save=[]
for i in range(len(item)):
    val=findmatch(item,i)
    if val in range(len(item)):
        k=str(i)+str(val)
        var = []
        for j in range(len(item[i])):

            var.append(item[i][j]+','+lookahead[i][j]+'|'+lookahead[val][j])
        lalrdict2[k]=var
        same.append(i)
        save.append(val)
    else:
        var1 = []
        for j in range(len(item[i])):

            var1.append(item[i][j]+','+lookahead[i][j])
        lalrdict2[i]=var1

for i in save:
    del lalrdict2[i]

new = {}
for k, v in table.items():
    new[k] = dict(v)

lalrtable=[]

for i in new:
    lalrtable.append(str(i)+str(new[i]))

for j in range(len(same)):
    same1=str(same[j])
    same2=str(save[j])
    for i in range(len(lalrtable)):
        if same1 in lalrtable[i]:
            r=same1+same2
            lalrtable[i]=lalrtable[i].replace(same1,r)
        elif same2 in lalrtable[i]:
            r = same1 + same2
            lalrtable[i]=lalrtable[i].replace(same2,r)
table=[]

print("****************Items*****************")

for s in lalrdict2:
    print("Item{}:".format(s))
    for i in range(len(lalrdict2[s])):
        print("\t", lalrdict2[s][i])

for i in range(len(lalrtable)):
    if i in save:
        continue
    else: table.append(lalrtable[i])
print('***************LALR TABLE**************')
for i in range(len(table)):
    print(table[i])