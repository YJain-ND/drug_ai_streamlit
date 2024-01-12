import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from datetime import datetime
from itertools import combinations

from itertools import chain, combinations

def filter_words(word):
    remove_words = ['tablet',
             'injection',
             'cream',
             'syrup',
             'suspension',
             'capsule',
             'infusion']
    for w in remove_words:
        word = word.replace(w,"")
    word = word.strip()
    return word


def ngrams(string,ns = [2,3]):
    ngram = []
    for n in ns:
        for i in range(len(string)-(n-1)):
            ngram.append(string[i:i+n])
    return ngram
    
def built_vectorizer(ng):
    vectorizer = TfidfVectorizer(analyzer=ngrams, min_df=1)
    X = vectorizer.fit_transform(ng)
    nbrs = NearestNeighbors(n_neighbors=1, n_jobs=1, metric='cosine').fit(X)
    return vectorizer,nbrs

def tfidf_nn(ng,me):
    vectorizer, nbrs = built_vectorizer(ng)
    input_vec = vectorizer.transform(me)
    distances, indices = nbrs.kneighbors(input_vec)
    return distances,indices

f = open('medicine_salt_full.json')
med2salt = json.load(f)

f = open('salt_medicine_full.json')
salt2med = json.load(f)

all_med = list(med2salt.keys())
all_salt = list(salt2med.keys())

all_med_cleaned = [filter_words(i) for i in all_med]

def medicine_details(med):
    dis,idx = tfidf_nn(all_med_cleaned,[med])
    medicine_used = all_med[idx[0][0]]
    type_of_med = medicine_used.split(" ")[-1]
    salts_in_match = med2salt[medicine_used]['composition']
    no_salt = len(salts_in_match)

    alter = set([])

    for salt in salts_in_match:
        if alter == set([]):
            alter = set(salt2med[salt])
        alter = alter.intersection(set(salt2med[salt]))

    full_match_alters = []
    other_alters = []

    for alt in alter:
        if len(med2salt[alt]['composition']) == no_salt:
            if type_of_med == alt.split(" ")[-1]:
                full_match_alters.append(alt)
        else:
            other_alters.append(alt)
    return medicine_used,salts_in_match,full_match_alters,other_alters

def get_subsets(lst):
    return list(chain.from_iterable(combinations(lst, r) for r in range(1,len(lst) + 1)))

def find_combinations(subsets):
    full_set = set().union(*subsets)
    
    def dfs(index, current_combination, remaining_elements):
        if not remaining_elements:
            combinations.append(current_combination)
            return

        for i in range(len(subsets)-1,index-1, -1):
            new_combination = current_combination + [subsets[i]]
            new_remaining = remaining_elements - set(subsets[i])
            dfs(i + 1, new_combination, new_remaining)

    combinations = []
    dfs(0, [], full_set)

    return combinations

def medication_optimization(meds):
    medicines = []
    salts = set([])
    matches = []
    for med in meds:
        print(med)
        medicine,salt,full_match_alters,other_alters = medicine_details(med.lower())
        medicines.append(medicine)
        salts = salts.union(set(salt))
        matches.append(set(full_match_alters))
    total_salts = len(salts)
    subsets = get_subsets(salts)
    all_combinations = find_combinations(subsets)
    
    for combination in all_combinations:
        print("Searching for combinations:", combination)
        if len(combination) >= len(meds):
            continue
        combs_match = {}
        prod = 1
        for comb in combination:
            print("Combination:",comb)
            full_match_alters = []
            meds_alter = set([])
            inital = True
            for salt in comb:
                if inital:
                    meds_alter = set(salt2med[salt])
                    inital = False
                else:
                    meds_alter = meds_alter.intersection(set(salt2med[salt]))
                print(f"Salt: {salt} | Intersections: {len(meds_alter)}")

            for alt in meds_alter:
                if len(med2salt[alt]['composition']) == len(comb):
                    full_match_alters.append(alt)

            prod *= len(full_match_alters)
            combs_match[comb] = full_match_alters
        if prod != 0:
            return combs_match,total_salts,list(salts),medicines
    return {},total_salts,list(salts),medicines

# print(medication_optimization(["dolo","combiflame"]))
# abufen c, dolo, augmentin
# def medication_optimization(meds):
#     medicines = []
#     salts = set([])
#     matches = []
#     for med in meds:
#         print(med)
#         medicine,salt,full_match_alters,other_alters = medicine_details(med.lower())
#         medicines.append(medicine)
#         salts = salts.union(set(salt))
#         matches.append(set(full_match_alters))
#     total_salts = len(salts)
#     for i in range(len(salts),len(salts)//2,-1):
#         combs = list(combinations(salts, i))
#         print(combs)
#         combs_match = {}
#         for comb in combs:
#             prod = 1
#             full_match_alters = []
#             meds_alter = set([])
#             for salt in comb:
#                 print(salt)
#                 if meds_alter == set([]):
#                     meds_alter = set(salt2med[salt])
#                 else:
#                     meds_alter = meds_alter.intersection(set(salt2med[salt]))
#             for alt in meds_alter:
#                 if len(med2salt[alt]['composition']) == len(comb):
#                     full_match_alters.append(alt)
#             prod *= len(full_match_alters) 
#             print(len(full_match_alters))
#             combs_match[comb] = full_match_alters
#         if prod != 0:
#             break    
#     return combs_match,total_salts,list(salts),medicines

# med = input("Medicine name: ").lower()
# start = datetime.now()
# dis,idx = tfidf_nn(all_med_cleaned,[med])
# end = datetime.now()
# print("Best Match by TfIdf: ",all_med_cleaned[idx[0][0]])
# medicine_used = all_med[idx[0][0]]
# print("Best Match Medicine: ",medicine_used)
# print("Time taken by TfIdf: ",end-start)

# start = datetime.now()
# match = process.extractOne(med, all_med_cleaned)
# end = datetime.now()
# print("Best Match by Fuzzy: ",match[0])
# medicine = all_med[all_med_cleaned.index(match[0])]
# print("Best Match Medicine: ",medicine)
# print("Time taken by Fuzzy: ",end-start)


# salts_in_match = med2salt[medicine_used]['composition']
# print("Salts Composition: ",salts_in_match)

# no_salt = len(salts_in_match)

# alter = set([])

# for salt in salts_in_match:
#     if alter == set([]):
#         alter = set(salt2med[salt])
#     alter = alter.intersection(set(salt2med[salt]))

# full_match_alters = []
# other_alters = []

# for alt in alter:
#     if len(med2salt[alt]['composition']) == no_salt:
#         full_match_alters.append(alt)
#     else:
#         other_alters.append(alt)

# print("Full Match Alternatives: ",full_match_alters)
# print("Other Alternatives: ", other_alters)

# def medication_optimization(meds):
#     medicines = []
#     salts = set([])
#     matches = []
#     for med in meds:
#         print(med)
#         medicine,salt,full_match_alters,other_alters = medicine_details(med.lower())
#         medicines.append(medicine)
#         salts.append(set(salt))
#         matches.append(set(full_match_alters))
     
#     unions = {}
#     for i in range(len(salts),0,-1):
#         comb = list(combinations(salts, i))
#         for salt in comb:
#             temp = set([])
#             for s in salt:
#                 temp = temp.union(s)
#             if i in unions:
#                 unions[i].append(temp)
#             else:
#                 unions[i] = [temp]

#     for i in unions:
#         final_comb  = {}
#         salts = unions[i]
#         alter = set([])
#         for salt in salts:
#             print(salt)
#             no_salt = len(salt)
#             for s in salt:
#                 if alter == set([]):
#                     alter = set(salt2med[s])
#                 alter = alter.intersection(set(salt2med[s]))
#                 full_match_alters = []
#                 for alt in alter:
#                     if len(med2salt[alt]['composition']) == no_salt:
#                         break
#                 full_match_alters.append(alt)
#         final_comb[i] = full_match_alters
#     return final_comb

# den cz tablet

# biospaaz tablet
# oronac plus tablet