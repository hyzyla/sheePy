import string


def calc2(number2, number1, operator):
    number1 = int(number1)
    number2 = int(number2)

    if operator is '+':
        return number1 + number2
    elif operator is '-':
        return number1 - number2
    elif operator is '*':
        return number1 * number2
    elif operator is '/':
        return int(number1 / number2)
    elif operator is '^':
        return number1 ** number2
    else:
        raise SyntaxError('Error: unknown operator')

def calc1(number1, token):
    number1 = int(number1)
    if token in 'DEC':
        return number1 - 1
    elif token in 'INC':
        return number1 + 1
    else:
        raise SyntaxError('Error: unknown function {}'.format(token))

def get_coordination(reference):
    return [string.ascii_uppercase.find(reference[0]) ,int(reference[1:])]


def is_operator(token):
    return token in ['+', '-', '*', '/', '^']


def is_number(token):
    try:
        int(token)
    except:
        return False
    else:
        return True


def is_left_assoc(token):
    return token in ['+', '-', '*', '/']


def is_right_assoc(token):
    return token == '^'


def cmp_precedence(token1, token2):
    operators = {'+': 0,
                 '-': 0,
                 '*': 5,
                 '/': 5,
                 '^': 10}
    return operators[token1] - operators[token2]


def parse(x):
    letters_and_digits = string.ascii_uppercase + string.digits + '.'
    x = ''.join(x.upper().split())

    ex = []
    temp = ''

    for i in x:
        if i in letters_and_digits:
            temp += i
            continue
        else:
            if temp is not '':
                ex.append(temp)
                temp = ''
            ex.append(i)
    if temp is not '':
        ex.append(temp)

    return ex


def polish(tokens):
    out = []
    stack = []
    for token in tokens:
        if is_function(token):
            stack.append(token)
        elif is_operator(token):
            while len(stack) != 0 and is_operator(stack[-1]):
                if (is_left_assoc(token) and cmp_precedence(token, stack[-1]) <= 0) or \
                        (is_right_assoc(token) and cmp_precedence(token, stack[-1]) < 0):
                    out.append(stack.pop())
                    continue
                break
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack:
                if stack[-1] != '(':
                    out.append(stack.pop())
                else:
                    break
            else:
                raise SyntaxError('Error: Formula without left parenthesis')
            stack.pop()
        else:
            out.append(token)
    while stack:
        out.append(stack.pop())
    if '(' in out:
        raise SyntaxError('Error: Formula without right parenthesis')

    return out


def is_reference(x):
    return x[0] in string.ascii_uppercase and is_number(x[1:])

def is_function(token):
    return token in ['FOO', 'INC', 'DEC']

def calc_polish(tokens, spread_sheet=None):
    print(tokens)
    stack = []
    for token in tokens:
        if is_number(token):
            stack.append(token)
        elif is_function(token):
            try:
                num1 = stack.pop()
            except IndexError:
                raise SyntaxError('Error: Syntax error')
            result = calc1(num1, token)
            stack.append(result)
        elif is_operator(token):
            try:
                num1 = stack.pop()
                num2 = stack.pop()
            except IndexError:
                raise SyntaxError('Error: Syntax error')
            result = calc2(num1, num2, token)
            stack.append(result)
        else:
            raise SyntaxError('Error: Unknown token"{}"'.format(token))
    return stack.pop()

if __name__ == '__main__':
    inp = input('>> ')
    tokens = polish(parse(inp))
    print(tokens)
    print(calc_polish(tokens))
