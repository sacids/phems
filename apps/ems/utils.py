
from jellyfish import soundex, metaphone
#import fuzzy
import string
import re
from functools import reduce
import operator, json
from treebeard.mp_tree import MP_Node


# to do - put in try box and catch errors
def calc_relevance(sentence, key_map):
    chars           = re.escape(string.punctuation) #get punctuation characters
    token_sentence  = (re.sub(r'['+chars+']', '',sentence)).split()
    token_soundex   = [soundex(x) for x in token_sentence]
    
    ans = set(key_map) & set(token_soundex)
    ss = 0
    if ans:
        ss  = reduce(operator.add,map(lambda x: key_map[x],ans))
    return ss
        
    
'''
with open("../../assets/json/keywords.json", 'r') as file:
    data = file.read().rstrip()
    key_map = json.loads(data)
sample = "Moto mkubwa umewaka goba leo, ni hatari fire kama  mafua samaki"

print(calc_relevance(sample,key_map))
'''


