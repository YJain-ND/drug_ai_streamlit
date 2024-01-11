import json

f = open('medicine_salt.json')
data = json.load(f)

f = open('medicine_salt_after_35k.json')
data2 = json.load(f)

data.update(data2)

out_file = open("medicine_salt_full.json", "w") 
json.dump(data, out_file, indent = 4) 
out_file.close()