from sympy import *
from itertools import product

global A, B, C, D, E, F, G, H, var_list
A, B, C, D, E, F, G, H = symbols('A B C D E F G H')
var_list = [A, B, C, D, E, F, G, H]
# if you have more than 8 variables do not
# just see what tt_out looks like

def tt_out(expr):
    """
    Prints a truth table for a given expression.

    :param expr: SymPy boolean expression
    """
    # convert sympy operators to python
    py_exp = ((expr.replace('&','and')).replace('|', 'or')).replace('~', 'not ')
    py_exp = py_exp.strip()
    code = compile(py_exp, '<string>', 'eval') # your string is now code
    names = code.co_names # take the variables from the code
    names= sorted(names) # sort them alphabetically
    print('\n' + ' '.join(names), ':', expr)
    for values in product(range(2), repeat=len(names)):
        env = dict(zip(names, values))
        # turn each term back into string
        # make Trues => 1 and Falses => 0
        print(' '.join(str(v) for v in values), ':', ((str(eval(code, env))).replace('True', '1')).replace('False', '0'))


def gic(function,not_cost=False):
    """
    Counts all the gate inputs for a SymPy bool expression.

    :param function: SymPy boolean expression
    :param not_cost: boolean, are do NOT operators have gic associated?
    :return: integer, count of all gate inputs in expression
    """
    cost = 0
    expr = str(function) # be string for counting
    for char in expr:
        if char == '(' or char.isalpha() or (not_cost and char=='~'):
            cost += 1
    return cost

def yn_input(msg):
    """
    Force user to type y or n (not case sensitive).

    :param msg: str, input message
    :return: str, only 'y' or 'n'
    """
    y_n = 'None'
    while y_n not in 'yn':
        y_n = (input(msg)).lower()
    return y_n

def derive_logic(var_no,minterms,dontcares):
    """
    Create SymPy bool expressions for SOP and POS for a given
    variable no., minterms and optional don't cares.

    :param var_no: integer, number of variables
    :param minterms: see Sympy.SOPform for formats allowed
    :param dontcares: as above
    :return: tuple, contains 2 SymPy bool expressions for POS & SOP
    """
    v_vars = var_list[:var_no]
    if dontcares is None:
        sop = SOPform(v_vars, minterms)
        pos = POSform(v_vars, minterms)
    else:
        sop=SOPform(v_vars,minterms,dontcares)
        pos=POSform(v_vars,minterms,dontcares)
    return sop, pos


def logic_in():
    """
    Verify and parse user input for use in SymPy.
    """
    def multi_in(msg):
        """
        Force user to only input comma separated integers.

        :param msg: str, input message
        :return: list of integer values
        """
        invalid = True
        while invalid:
            out_terms = []
            terms = (input(msg)).replace(' ', '')  # white spaces are forbidden
            invalid = False
            terms = terms.split(',')
            for term in terms:
                if not term.isnumeric():
                    invalid = True  # thats not an integer try again
                else:
                    out_terms.append(int(term))
        return out_terms
    while True:
        var_no = input('Enter number of variables:\n')
        if var_no.isnumeric():
            if 0 < int(var_no) <= 8:
                break
        print('Enter a valid number between 1 and 8')
    minterms = multi_in('Enter comma separated minterms:\n')
    dc_flag=yn_input('Are there any don\'t care values? [y/n]\n')
    if dc_flag == 'n':
        dontcares=None
    else:
        dontcares=multi_in('Enter comma separated don\'t cares:\n')

    return int(var_no), minterms, dontcares

def prime_out(v, mt):
    """
    For a given variable number and decimal minterms, will output
    the prime implicants of the expression.

    :param v: integer, number of variables in expression
    :param mt: iterable, list of decimal minterm values
    :return: str, all minterms with their corresponding variables
    """
    out_block=''
    for t in range(len(mt)):
        # for each minterm
        term = mt[t]
        out_str = 'P' + str(term + 1) + ': ' #add P no.
        value = str(bin(term)) # convert decimal to binary
        value = value.split('b') # i.e. 0bxxxxx, remove '0b'
        zeroes = v - len(value[1]) # how many bits are missing?
        byte = ''
        for bit in range(zeroes):
            byte = byte + '0'
        byte = byte + value[1] # add any missing bits back
        for i in range(v):
            if byte[i] == '0': # a zero => NOT variable
                out_str = out_str + '~'
            out_str = out_str + str(var_list[i]) + ' '
        out_block = out_block + out_str + '\n'
    return out_block

def min_in():
    v, mt, dc = logic_in()
    SOP, POS = derive_logic(v, mt, dc)
    disp_flag = yn_input('Prime implicants in full? [y/n]\n')
    if disp_flag == 'y':
        print(prime_out(v, mt))
    return SOP, POS

def bool_in():
    """
    Simplify SymPy bool expression from user input.
    AND = &, OR = |, NOT = ~
    Bracket your ANDs plz

    :return: tuple, contains 2 SymPy bool expressions for POS & SOP
    """
    while True:
        try:
            f = parse_expr((input('Input boolean expression:\n')),evaluate=False)
            SOP = to_dnf(f,simplify=True)
            POS = to_cnf(f, simplify=True)
            break
        except:
            pass

    return SOP, POS


