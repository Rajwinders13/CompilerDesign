#first follow calculation
from re import *
from collections import OrderedDict

t_list = OrderedDict()
nt_list = OrderedDict()
production_list = []


# ------------------------------------------------------------------

class Terminal:

    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return self.symbol


# ------------------------------------------------------------------

class NonTerminal:

    def __init__(self, symbol):
        self.symbol = symbol
        self.first = set()
        self.follow = set()

    def __str__(self):
        return self.symbol

    def add_first(self, symbols): self.first |= set(symbols)

    def add_follow(self, symbols): self.follow |= set(symbols)


# ------------------------------------------------------------------

def compute_first(symbol):
    global production_list, nt_list, t_list

    if symbol in t_list:
        return set(symbol)

    for prod in production_list:
        head, body = prod.split('->')

        if head != symbol: continue

        if body == '':
            nt_list[symbol].add_first(chr(1013))
            continue

        if body[0] == symbol: continue

        for i, Y in enumerate(body):

            t = compute_first(Y)
            nt_list[symbol].add_first(t - set(chr(1013)))
            if chr(1013) not in t:
                break

            if i == len(body) - 1:
                nt_list[symbol].add_first(chr(1013))

    return nt_list[symbol].first


# ------------------------------------------------------------------

def get_first(symbol):
    return compute_first(symbol)


def compute_follow(symbol):
    global production_list, nt_list, t_list

    if symbol == list(nt_list.keys())[0]:
        nt_list[symbol].add_follow('$')

    for prod in production_list:
        head, body = prod.split('->')

        for i, B in enumerate(body):
            if B != symbol: continue

            if i != len(body) - 1:
                nt_list[symbol].add_follow(get_first(body[i + 1]) - set(chr(1013)))

            if i == len(body) - 1 or chr(1013) in get_first(body[i + 1]) and B != head:
                nt_list[symbol].add_follow(get_follow(head))


def get_follow(symbol):
    global nt_list, t_list

    if symbol in t_list.keys():
        return None

    return nt_list[symbol].follow
from tkinter import*
from tkinter import filedialog

mgui=Tk()

mgui.geometry('450x450+200+200')
mgui.title('SELECT FILE')
tempgrammar=[]
def takeInput(file_name):
    try:
        grammar_file = open(file_name, "r")
    except:
        print("Cannot Find File Named", file_name)
        exit(0)
    # add garmmar
    for each_grammar in grammar_file:
        tempgrammar.append(each_grammar.strip())

def select():
    mgui.fileName=filedialog.askopenfilename(filetypes=(("Python",".py"),("All files","*.*")))
    takeInput(mgui.fileName)
    mgui.destroy()

def main(pl=None):
    #print('Enter the grammar productions (enter  end to stop)')

    global production_list, t_list, nt_list
    ctr = 1
    n=0
    t_regex, nt_regex = r'[a-z\W]', r'[A-Z]'

    if pl == None:
        mybutton = Button(mgui, text='SELECT', command=select).pack()
        mgui.mainloop()

        print(tempgrammar)
        while True:
            if n<len(tempgrammar):
                production_list.append(tempgrammar[n])
                #production_list.append(input().replace(' ', ''))
                if production_list[-1].lower() in ['end', '']:
                    del production_list[-1]
                    break

                head, body = production_list[ctr - 1].split('->')

                if head not in nt_list.keys():
                    nt_list[head] = NonTerminal(head)

                # for all terminals in the body of the production
                for i in finditer(t_regex, body):
                    s = i.group()
                    if s not in t_list.keys(): t_list[s] = Terminal(s)

                    # for all non-terminals in the body of the production
                for i in finditer(nt_regex, body):
                    s = i.group()
                    if s not in nt_list.keys(): nt_list[s] = NonTerminal(s)

                ctr += 1
            n+=1
    print(production_list)
    if pl != None:

        for i, prod in enumerate(pl):

            if prod.lower() in ['end', '']:
                del pl[i:]
                break

            head, body = prod.split('->')

            if head not in nt_list.keys():
                nt_list[head] = NonTerminal(head)

            # for all terminals in the body of the production
            for i in finditer(t_regex, body):
                s = i.group()
                if s not in t_list.keys(): t_list[s] = Terminal(s)

            # for all non-terminals in the body of the production
            for i in finditer(nt_regex, body):
                s = i.group()
                if s not in nt_list.keys(): nt_list[s] = NonTerminal(s)

        return pl


# ------------------------------------------------------------------

if __name__ == '__main__':
    main()

