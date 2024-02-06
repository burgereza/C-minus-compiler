import re
token = re.match(r'\((\w+), (\w+)\)', 'int').group(2)
print(token)