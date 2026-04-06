def f(s:str):
    blocks = s.split(' ')
    try:
        a, op, b = int(blocks[0]), blocks[1], int(blocks[2])
    except ValueError:
        raise Exception('Error: Numbers must only contain digits.')
    if not (op == '+' or op == '-'):
        raise Exception('Error: Operator must be \'+\' or \'-\'.')
    if a > 9999 or b > 9999:
        raise Exception('Error: Numbers cannot be more than four digits.')
    c = eval(s)
    max_len = len(str(max(a, b))) + 2

    r = []
    r.append(str(a).rjust(max_len, ' '))
    r.append(op + ' ' + str(b).rjust(max_len - 2, ' '))
    r.append('-' * max_len)
    r.append(str(c).rjust(max_len, ' '))
    return r


def arithmetic_arranger(problems:list, show_result=False):
    if len(problems) > 5:
        return 'Error: Too many problems.'

    arranged_problems = ''
    d = []

    for problem in problems:  # Problem is a str like: "32 + 8"
        try:
            ps = f(problem)
            d.append(ps)
        except Exception as e:
            return str(e)

    n = 3
    if show_result:
        n = 4

    for i in range(n):
        for j in range(len(d)):
            ps = d[j]
            if j == 0:
                arranged_problems = arranged_problems + ps[i]
            else:
                arranged_problems = arranged_problems + '    ' + ps[i]
        if i != n - 1:
            arranged_problems = arranged_problems + '\n'

    return arranged_problems
