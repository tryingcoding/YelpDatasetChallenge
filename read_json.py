"""convert json files to dat file"""

from sets import Set
import sys
import json
from operator import itemgetter

f = open('yelp_academic_dataset_business.json')
g = open("categories.json",'w')
cat = []
total = 0
count = 0
items = Set()
for line in f:
    total += 1
    line = json.loads(line.strip())
    #for key in line:
        # print str(key) + '\t' + str(line[key])
        # break
    cat += line['categories']
    for one_cat in line['categories']:
        if 'food' in one_cat.lower():
            count += 1
            items.add(line['business_id'])
            break

f.close()
#print total
#print count

for count in range(0,len(cat)):
    cat[count] = cat[count].lower()
cat = list(set(cat))
out_str = json.dumps({'categories': cat})
g.write(out_str)
g.flush()
g.close()

ratings = []
f = open('yelp_academic_dataset_review.json')
for line in f:
    line = json.loads(line.strip())
    if line['business_id'] in items:
        ratings.append((line['user_id'], line['business_id'], line['stars'])) #UserID::BusinessID::Stars
f.close()

ratings = sorted(ratings, key= lambda tup: tup[0] + tup[1])
h = open("ratings.dat",'w')
for rating in ratings:
    h.write(rating[0] + '::' + rating[1] + '::' + str(rating[2]) + '\n')
    h.flush()
h.close()
