import csv
def main():
    input_string = input("Enter String ")

    input_ind = list(shlex.shlex(input_string))
    input_ind.append('$')
    master = {}
    master_list = []
    new_list = []
    non_terminals = []
    grammar = open('grammar.txt', 'r')

    for row2 in grammar:

        if '->' in row2:
            # new production
            if len(new_list) == 0:
                start_state = row2[0]
                non_terminals.append(row2[0])
                new_list = []
                new_list.append(row2.rstrip('\n'))
            else:
                master_list.append(new_list)
                del new_list
                new_list = []
                new_list.append(row2.rstrip('\n'))
                non_terminals.append(row2[0])


        elif '|' in row2:
            new_list.append(row2.rstrip('\n'))

    master_list.append(new_list)

    for x in range(len(master_list)):
        for y in range(len(master_list[x])):
            master_list[x][y] = [s.replace('|', '') for s in master_list[x][y]]
            master_list[x][y] = ''.join(master_list[x][y])
            master[master_list[x][y]] = non_terminals[x]

    for key, value in master.items():
        if '->' in key:
            length = len(key)
            for i in range(length):
                if key[i] == '-' and key[i + 1] == ">":
                    index = i + 2
                    break
                var_key = key
            new_key = key[index:]

    var = master[var_key]
    del master[var_key]
    master[new_key] = var

    order_table = []
    with open('order.csv', 'rU') as file2:
        order = csv.reader(file2)
        for row in order:
            order_table.append(row)

    operators = order_table[0]
    stack = []

    stack.append('$')
    start = "\033[1m"
    end = "\033[0;0m"
    print(start+"Stack"+end,' '*(27),start+ "Input"+end, ' '*(17), start+"Precedence relation"+end,' '*(4), start+"Action"+end)

    vlaag = 1
    while vlaag:
        if input_ind[0] == '$' and len(stack) == 2:
            vlaag = 0

        length = len(input_ind)

        buffer_inp = input_ind[0]
        temp1 = operators.index(str(buffer_inp))
        if stack[-1] in non_terminals:
            buffer_stack = stack[-2]
        else:
            buffer_stack = stack[-1]
        temp2 = operators.index(str(buffer_stack))
        # print buffer_inp, buffer_stack

        precedence = order_table[temp2][temp1]

        if precedence == '<':
            action = 'shift'
        elif precedence == '>':
            action = 'reduce'

        print(stack, ' ' * (22 - len(stack)), input_ind, ' ' * (18 - len(input_ind)), precedence,
              ' ' *9, action, "\n")

        if action == 'shift':
            stack.append(buffer_inp)
            input_ind.remove(buffer_inp)
        elif action == 'reduce':
            for key, value in master.items():
                var1 = ''.join(stack[-1:])
                var2 = ''.join(stack[-3:])
                if str(key) == str(buffer_stack):
                    stack[-1] = value
                    break
                elif key == var1 or stack[-3:] == list(var1):
                    stack[-3:] = value
                    break
                elif key == var2:
                    stack[-3:] = value
        del buffer_inp, temp1, buffer_stack, temp2, precedence

        if vlaag == 0:
            print("Accepted!!")
    return 2


import sys
import shlex

if __name__ == "__main__":
    sys.exit(main())
