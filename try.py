x = ['a b', 'hola je', 'jejejejje']
def has_whitespace(x):
    return x.count(' ')>0

def list_has_whitespace(x):
    return sum(map(has_whitespace, x))>0

if (list_has_whitespace(x)):
    print('extio')
else:
    print(':(')    