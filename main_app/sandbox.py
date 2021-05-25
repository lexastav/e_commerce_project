import re

email = 'testtestru'
if re.search(r'[^@]+@[^@]+\.[^@]+', email):
    print(True)