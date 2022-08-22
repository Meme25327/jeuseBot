import random
from datetime import date
import string

import numpy as np

today = date.today()

# dd/mm/YY
d1 = today.strftime("%d%m%Y")
print(d1)

uID = input("Enter the user ID: ")

rng2 = np.random.RandomState(int(d1))

print(rng2.randint(0, 100, 1))  # [8]


'''

random.seed(uID)
print(''.join(random.choices(string.ascii_lowercase, k=5)))
'''
