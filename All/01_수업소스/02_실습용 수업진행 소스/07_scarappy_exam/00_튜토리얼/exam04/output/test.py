import pickle
import os
print(os.getcwd())

with open('result.pickle', 'rb') as f:
    result = pickle.load(f)

print(type(result))  
print()  