import re
string = '!@#$%^&45wc'
result = re.findall(r'[a-zA-Z0-9]', string)
print(result)