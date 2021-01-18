from input_wrap import yn_input, min_in, bool_in
from logsimp import gic, tt_out

if __name__ == "__main__":
    input_type=yn_input('Define expression with minterms? [y/n]\n')
    if input_type == 'y':
        SOP, POS = min_in()
    else:
        SOP, POS = bool_in()

    print('SOP is {0} with cost = {1} gi'.format(SOP, gic(SOP)))
    print('POS is {0} with cost = {1} gi'.format(POS, gic(POS)))

    input_type=yn_input('Show truth table? [y/n]\n')
    if input_type == 'y':
        tt_out(str(SOP))
