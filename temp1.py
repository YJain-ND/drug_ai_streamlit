import json

f = open('medicine_salt_full.json')
med2salt = json.load(f)

com_len = []
for med in med2salt:
    com_len.append(len(med2salt[med]['composition']))

print(max(com_len))