from random import choice

def activeCode():
    code = ''
    for num in range(6):
        code += str(choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    return code