from logsimp import derive_logic, prime_out, bool_parse


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

def logic_in():
    """
    Verify and parse user input for use in SymPy.

    :return: variable number, minterm list, dontcare list
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
    dc_flag = yn_input('Are there any don\'t care values? [y/n]\n')
    if dc_flag == 'n':
        dontcares=None
    else:
        dontcares=multi_in('Enter comma separated don\'t cares:\n')

    return int(var_no), minterms, dontcares

def min_in():
    v, mt, dc = logic_in()
    SOP, POS = derive_logic(v, mt, dc)
    disp_flag = yn_input('Show prime implicants in full? [y/n]\n')
    if disp_flag == 'y':
        print(prime_out(v, mt))
    return SOP, POS

def bool_in():
    """
    Run bool_parse() with user input and validation
    :return: tuple, contains 2 SymPy bool expressions for POS & SOP
    """
    while True:
        try:
            return bool_parse(input('Input boolean expression:\n'))
        except Exception as error:
            print(str(error)+'\nEnter a valid SymPy expression.')