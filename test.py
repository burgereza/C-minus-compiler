stack = ['sss']


for char in reversed(['Declaration', 'DeclarationList']):
    stack.append(char)

print(stack)

['sss', 'DeclarationList', 'Declaration']