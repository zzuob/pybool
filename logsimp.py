from sympy import symbols, sympify
from sympy.logic import simplify_logic, POSform, SOPform
from itertools import product

global A, B, C, D, E, F, G, H, var_list
A, B, C, D, E, F, G, H = symbols('A B C D E F G H')
var_list = [A, B, C, D, E, F, G, H]
# TODO improve this
# if you have more than 8 variables do not
# just see what tt_out looks like

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


def bool_parse(expr):
    """
    Simplify SymPy bool expression from user input.
    AND = &, OR = |, NOT = ~
    Bracket your ANDs plz

    :return: tuple, contains 2 SymPy bool expressions for POS & SOP
    """
    f = sympify((expr),evaluate=False, locals={'E': E})
    SOP = simplify_logic(f,form='dnf')
    POS = simplify_logic(f,form='cnf')
    return SOP, POS

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
        sop = SOPform(v_vars,minterms,dontcares)
        pos = POSform(v_vars,minterms,dontcares)
    return sop, pos

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
        out_str = 'P' + str(term) + ': ' #add P no.
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

