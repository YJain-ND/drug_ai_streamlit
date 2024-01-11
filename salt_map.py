import json
import re

f = open('medicine_salt_full.json')
data = json.load(f)

d = {}

print("Total number of medicines",len(data.keys()))
input()
for key in data.keys():
    print(key)
    for salt in data[key]['composition']:
        print(salt)
        d[salt] = d.get(salt,list()) + [key]

out_file = open("salt_medicine_full.json", "w") 
json.dump(d, out_file, indent = 4) 
out_file.close()